from flask import render_template, flash, redirect, session, jsonify, g, request
from app.models import Post, User, Vote, Comment, CountryCode
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from .forms import PostForm, UserForm, LoginForm, SignupForm
import requests

# The home route will display all posts in the database
@app.route('/', methods=['GET', 'POST'])
def view_posts():
    """
    Home page route.
    Displays all posts in the database.
    """
    # Fetch the user's votes from the database
    voted_posts = {}
    user_id = session.get('user_id')
    if user_id:
        user_votes = Vote.query.filter_by(user_id=user_id).all()
        voted_posts = {vote.post_id: vote.vote_type for vote in user_votes}

    # Fetch all posts from the database
    posts = Post.query.all()
    if not posts:
        flash("No posts are in the database right now. Please create some!")
        posts = []

    # For each post, fetch the first three comments
    post_comments = {}
    for post in posts:
        post_comments[post.id] = Comment.query.filter_by(post_id=post.id).limit(3).all()

    # Get the country code from the query string
    country_code = CountryCode.query.all()

    return render_template('view_posts.html',
                        search=True,
                        session=session,
                        posts=posts,
                        voted_posts=voted_posts,
                        post_comments=post_comments,
                        country_code=country_code,
                        title='All Posts')

@app.route('/comments/<int:post_id>', methods=['GET'])
def get_comments(post_id):
    """
    Get comments route.
    Fetches comments for a specific post.
    """
    # Fetch comments for the specified post
    limit = request.args.get('limit', None)
    if limit:
        comments = Comment.query.filter_by(post_id=post_id).limit(int(limit)).all()
    else:
        comments = Comment.query.filter_by(post_id=post_id).all()

    # Prepare the comments data to be sent as a response
    comments_data = []
    for comment in comments:
        comments_data.append(
            {
                'id': comment.id,
                'title': comment.title,
                'description': comment.description,
                'username': comment.user.username,
                'user_id': comment.user.id
            })
    return jsonify({'comments': comments_data})

@app.route('/create', methods=['GET', 'POST'])
def create_post():
    """
    Create post route.
    Allows users to add a new post or add a comment if the post already exists.
    """
    # Create a new PostForm instance and validate the form data then add the post to the database
    form = PostForm()
    if form.validate_on_submit():
        existing_post = Post.query.filter_by(
            country_code=form.country_code.data,
            phone_number=form.phone_number.data
        ).first()
        # Check if the user is logged in
        user_id = session.get('user_id')
        if not user_id:
            flash('You must be logged in to create a post', 'danger')
            return redirect('/login')

        if existing_post:
            # Post already exists, add a comment to it
            new_comment = Comment(
                post_id=existing_post.id,
                user_id=user_id,
                title=form.title.data,
                description=form.description.data
            )
            db.session.add(new_comment)
            db.session.commit()
            flash('Comment added to existing post successfully', 'success')
        else:
            # Create a new post
            new_post = Post(
                country_code=form.country_code.data,
                phone_number=form.phone_number.data,
                upvotes=0,
                downvotes=0,
                user_id=user_id
            )
            db.session.add(new_post)
            db.session.commit()

            # Add the first comment to the new post
            new_comment = Comment(
                post_id=new_post.id,
                user_id=user_id,
                title=form.title.data,
                description=form.description.data
            )
            db.session.add(new_comment)
            db.session.commit()

            flash('New post added successfully', 'success')

        # Redirect to the home page
        return redirect('/')
    return render_template("create_post.html", title='Create Post',
                        form=form)

# The my_posts route will display posts created by a specific user
@app.route('/my_posts', methods=['GET'])
def my_posts():
    """
    My posts route.
    Displays posts created by the logged-in user.
    """
    # Fetch the user's votes from the database
    voted_posts = {}
    user_id = session.get('user_id')
    if user_id:
        user_votes = Vote.query.filter_by(user_id=user_id).all()
        voted_posts = {vote.post_id: vote.vote_type for vote in user_votes}
    # Fetch all posts from the database
    posts = Post.query.all()
    post_comments = {}
    posts_copy = posts.copy()
    for post in posts_copy:
        comments = Comment.query.filter_by(post_id=post.id).limit(3).all()
        # Check in all the comment if there is a comment by the user then add it to the post_comments otherwise remove the post
        comments = [comment for comment in comments if comment.user_id == user_id]
        if comments != []:
            post_comments[post.id] = comments
        else:
            posts.remove(post)
    # Check if there are no posts
    if not posts:
        flash("No posts found")
        posts = []

    return render_template('view_posts.html',
                            search=False,
                            posts=posts,
                            post_comments=post_comments,
                            voted_posts=voted_posts,
                            title='My Posts')

@app.route('/my_account', methods=['GET', 'POST'])
def my_account():
    """
    My account route.
    Displays and allows editing of user account information.
    """
    # Fetch the user's information from the database
    user_id = session.get('user_id')
    if not user_id:
        flash('You must be logged in to view your account', 'danger')
        return redirect('/login')
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)
    # Check if the form data is valid then update the user's information
    if form.validate_on_submit():
        # Check if the username or email already exists
        existing_user = User.query.filter((User.username == form.username.data) | (User.email == form.email.data)).first()
        if existing_user and existing_user.id != user_id:
            flash('An account with that username or email already exists.', 'danger')
            return redirect('/my_account')
        # Update the user's information
        user.username = form.username.data
        user.email = form.email.data
        db.session.commit()
        flash('Account updated successfully', 'success')
        return redirect('/my_account')
    return render_template('my_account.html', title='My Account', form=form)

@app.route('/vote/<int:id>/<string:vote_type>', methods=['POST'])
def vote_post(id, vote_type):
    """
    Vote post route.
    Allows users to vote on a post.
    """
    # Check if the user is logged in
    user_id = session.get('user_id')
    if not user_id:
        print('User not logged in')
        return jsonify({'success': False, 'message': 'You must be logged in to vote.'})

    # Fetch the post from the database
    post = Post.query.get_or_404(id)
    existing_vote = Vote.query.filter_by(post_id=id, user_id=user_id).first()

    if existing_vote:
        # User has already voted on this post, so remove the vote
        db.session.delete(existing_vote)
        if existing_vote.vote_type == 'upvote':
            post.upvotes -= 1
            if vote_type == 'downvote':
                # Add a new vote
                new_vote = Vote(post_id=id, user_id=user_id, vote_type=vote_type)
                db.session.add(new_vote)
                post.downvotes += 1
        else:
            post.downvotes -= 1
            if vote_type == 'upvote':
                # Add a new vote
                new_vote = Vote(post_id=id, user_id=user_id, vote_type=vote_type)
                db.session.add(new_vote)
                post.upvotes += 1

    else:
        # Add a new vote
        new_vote = Vote(post_id=id, user_id=user_id, vote_type=vote_type)
        db.session.add(new_vote)
        if vote_type == 'upvote':
            post.upvotes += 1
        elif vote_type == 'downvote':
            post.downvotes += 1
        else:
            print('Invalid vote type')
            return jsonify({'success': False, 'message': 'Invalid vote type.'})

    db.session.commit()

    # Return the updated vote counts in the response
    return jsonify({
        'success': True,
        'upvotes': post.upvotes,
        'downvotes': post.downvotes
    })

@app.route('/search', methods=['GET'])
def search_posts():
    """
    Search posts route.
    Allows users to search for posts based on country code and phone number.
    """
    # Fetch the search query parameters
    country_code = request.args.get('country_code', '').strip()
    phone_number = request.args.get('phone_number', '').strip()
    search_query = Post.query

    # Apply filters if country_code or phone_number is provided
    if country_code or phone_number:
        if country_code:
            search_query = search_query.filter(Post.country_code == country_code)
        if phone_number:
            search_query = search_query.filter(Post.phone_number == phone_number)

    # Fetch the search results
    search_results = search_query.all()
    current_user_id = session.get('user_id')

    # Prepare the search results data to be sent as a response
    results_data = []
    for post in search_results:
        comments = []
        for comment in post.comments:
            comments.append({
                'id': comment.id,
                'user_id': comment.user_id,
                'username': comment.user.username,
                'title': comment.title,
                'description': comment.description
            })
        results_data.append({
            'id': post.id,
            'country_code': post.country_code,
            'phone_number': post.phone_number,
            'upvotes': post.upvotes,
            'downvotes': post.downvotes,
            'comments': comments
        })

    return jsonify({'success': True, 'posts': results_data, 'current_user_id': current_user_id})

@app.route('/filter_country_codes', methods=['GET'])
def filter_country_codes():
    '''
    Filter country codes route.
    Allows users to filter country codes based on the query string.
    '''
    # Fetch the query string
    query = request.args.get('query', '').strip().lower()
    country_codes = CountryCode.query.filter(CountryCode.name.ilike(f'%{query}%') | CountryCode.code.ilike(f'%{query}%')).all()
    results = [{'code': country.code, 'name': country.name} for country in country_codes]
    return jsonify({'success': True, 'country_codes': results})

# The delete_post route will allow users to delete an existing post
@app.route('/delete_post/<int:id>', methods=['POST'])
def delete_post(id):
    """
    Delete post route.
    Allows users to delete an existing post from the database.
    """
    # Fetch the post from the database and delete it
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully', 'success')
    return redirect('/')

@app.route('/edit_post/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    """
    Edit post route.
    Allows users to edit an existing post in the database.
    """
    # Fetch the post from the database
    comment = Comment.query.get_or_404(id)
    if comment is None:
        flash('Comment not found', 'danger')
        return redirect('/')

    # Create a new PostForm instance and validate the form data then update the post in the database
    form = PostForm(obj=comment)
    post = Post.query.get(comment.post_id)

    # Check if the form data is valid then update the post
    if form.validate_on_submit():
        comment.title = form.title.data
        comment.description = form.description.data

        # Commit the updates to the database
        db.session.commit()
        flash('Post updated successfully', 'success')
        return redirect('/')

    return render_template('edit_post.html', form=form, post=post)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login route.
    Allows users to log in to their accounts.
    """
    # Create a new LoginForm instance and validate the form data then log the user in
    form = LoginForm()
    if form.validate_on_submit():
        # Check if the user exists and the password is correct
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            session['user_id'] = user.id
            flash('Login successful', 'success')
            return redirect('/')
        else:
            flash('Invalid email or password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Signup route.
    Allows new users to create an account.
    """
    # Create a new SignupForm instance and validate the form data then create a new user account
    form = SignupForm()
    if form.validate_on_submit():
        # Check if the username or email already exists
        existing_user = User.query.filter((User.username == form.username.data) | (User.email == form.email.data)).first()
        if existing_user:
            flash('An account with that username or email already exists.', 'danger')
            return redirect('/signup')
        # Create a new user account
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully. Please log in.', 'success')
        return redirect('/login')
    print('Form errors:', form.errors)
    return render_template('signup.html', title='Signup', form=form)

@app.route('/logout')
def logout():
    """
    Logout route.
    Logs the user out of their account.
    """
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect('/login')

# The error handler for 404 errors
@app.errorhandler(404)
def page_not_found(e):
    """
    404 error handler.
    Displays a custom 404 error page.
    """
    return render_template('404.html'), 404
