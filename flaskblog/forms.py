from flask_wtf import FlaskForm
# To upload and update new profile photos.
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    # Username can't be left empty so using validator DataRequired(), Set the length of field from 2 to 20
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    # Next field is Email-> validator is Email
    email = StringField('Email', validators=[DataRequired(), Email()])
    # This field is password, so it will be of PasswordField instead of StringField
    password = PasswordField('Password', validators=[DataRequired()])
    # The EqualTo() is used to check if the confirm password is same as password.
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    # Submit button
    submit = SubmitField('Sign Up')

    # These are self built functions, for validating the already existence of same username in db.
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            # Once we define the ValidationError, we'll import using
            # from wtforms.validators import ValidationError
            raise ValidationError('Username already taken, please choose a different name')

    # These are self built functions, for validating the already existence of same email in db.
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            # Once we define the ValidationError, we'll import using
            # from wtforms.validators import ValidationError
            raise ValidationError('Email is taken, please choose a different one')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    # This field is password, so it will be of PasswordField instead of StringField
    password = PasswordField('Password', validators=[DataRequired()])
    # Remember be option can be checked/un-checked, so it defined as Bool
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    # Username can't be left empty so using validator DataRequired(), Set the length of field from 2 to 20
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    # Next field is Email-> validator is Email
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    # Submit button
    submit = SubmitField('Update')

    # These are self built functions, for validating the already existence of same username in db.
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                # Once we define the ValidationError, we'll import using
                # from wtforms.validators import ValidationError
                raise ValidationError('Username already taken, please choose a different name')

    # These are self built functions, for validating the already existence of same email in db.
    def validate_email(self, email):
        # User can update form without changing the username and email, so we need to apply this condition.
        # Since it should not throw error, if the email of current user is not equal to the queried email.
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                # Once we define the ValidationError, we'll import using
                # from wtforms.validators import ValidationError
                raise ValidationError('Email is taken, please choose a different one')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators =[DataRequired()])
    submit = SubmitField('Post')
