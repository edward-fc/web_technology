from app import db

class Comment(db.Model):
    '''
    Create a new class called Comment to store comments on posts
    '''
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)

    # Establish relationship with Post model
    post = db.relationship('Post', back_populates='comments')
    user = db.relationship('User', back_populates='comments')

class Post(db.Model):
    '''
    Create a new class called Post to store posts
    '''
    id = db.Column(db.Integer, primary_key=True)
    country_code = db.Column(db.String(10), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)

    upvotes = db.Column(db.Integer, default=0)
    downvotes = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    votes = db.relationship('Vote', back_populates='post', lazy=True)
    comments = db.relationship('Comment', back_populates='post', lazy=True)

class User(db.Model):
    '''
    Create a new class called User to store user information
    '''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)

    votes = db.relationship('Vote', back_populates='user', lazy=True)
    comments = db.relationship('Comment', back_populates='user', lazy=True)


class Vote(db.Model):
    '''
    Create a new class called Vote to store votes on posts
    '''
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    vote_type = db.Column(db.String(10), nullable=False)

    user = db.relationship('User', back_populates='votes')
    post = db.relationship('Post', back_populates='votes')

class CountryCode(db.Model):
    '''
    Create a new class called CountryCode to store country codes
    '''
    __tablename__ = 'country_codes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(10), nullable=False)
