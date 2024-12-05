from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from app.models import CountryCode
from app import app

class PostForm(FlaskForm):
    '''
    This class creates a form for users to submit posts.
    '''
    # Fetch all country codes from the database
    with app.app_context():
        country_codes = CountryCode.query.all()
    country_code = SelectField('Country Code', choices=[(code.code, code.name) for code in country_codes], validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(min=7, max=15)])
    title = StringField('Title', validators=[DataRequired(), Length(max=150)])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class UserForm(FlaskForm):
    '''
    This class creates a form for users to update their information.
    '''
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Update')

class LoginForm(FlaskForm):
    '''
    This class creates a form for users to log in.
    '''
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    '''
    This class creates a form for users to sign up.
    '''
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Signup')
