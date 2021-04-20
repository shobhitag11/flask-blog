################################################
# To remove any repetitive code in HTML files
################################################

# We'll use in a common layhout.html files
{% block content %}{% endblock %}

# To use the above block in other HTML files, we'll extend it using.
{% extends "layout.html" %}
{% block content %}
Different html blocks
{% endblock %}

################################################
# Flash message in HTML page
################################################

=> from flask import flash
# to flash a message in html page
=> flash(f'msg_string', 'success'/'danger')

################################################
# To Create forms in Flask
################################################

#install package called wtforms in python
=> pip install flask-wtf
=> we'll create a separate forms.py file

#to create a form for Registration
=>
class RegistrationForm(FlaskForm):
    # Username can't be left empty so using validator DataRequired(), Set the length of field from 2 to 25
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    # Next field is Email-> validator is Email
    email = StringField('Email', validators=[DataRequired(), Email()])
    # This field is password, so it will be of PasswordField instead of StringField
    password = PasswordField('Password', validators=[DataRequired()])
    # The EqualTo() is used to check if the confirm password is same as password.
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    # Submit button
    submit = SubmitField('Sign Up')

#to create a form for Login
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    # This field is password, so it will be of PasswordField instead of StringField
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

#To validate form fields:
=> use wtforms.validators

#Form attributes
=> form.validate_on_submit()- Checks the validity(email entered is correct, and check the other
  form fields that are defined) of the form when the form is filled and the user clicks on the submit button in HTML page.
=> Get the data of a form field: form.email.data(here, email is the form field)

################################################
# What is ORM?  Object relational mapping
################################################

#1.) It allows us to access database in object oriented manner.
#2.) Can be connected with various kind of databases.

##How to create a SQL Alchemy database model in Flask python(Concept of ORM)

#Install below package
=> pip install flask-sqlalchemy

#One the above package is installed, we'll import in main app(i.e. here flaskblog.py)
=> from flask_sqlalchemy import SQLAlchemy

#Set, /// represents the current directory of the flaskblog.py file.
=> app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

#Create SQLAlchemy object for the main application, using the following command:
=> db = SQLAlchemy(app)

#Create the ORM model, where the class name represents the table name,
#and we can set the attributes of the table in classes
#Here the class Name defined will the name of the table defined in the database
=>
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # unique is True becasue no two values for username and password can't be same.
    username = db.Column(db.String(20), unique=True, nullable=False)
    # nullable is False because, user must enter some value for each attribute.
    email = db.Column(db.String(120), unique=True, nullable=False)
    # image file for user profile picture.
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    # author of the post will be the user!-> one to many relationship
    posts= db.relationship('Post', backref= 'author', lazy=True)

    # repr does how our object is printed out, similar to __str__()
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
=>
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # unique is True becasue no two values for username and password can't be same.
    title = db.Column(db.String(100), nullable=False)
    # nullable is False because, user must enter some value for each attribute.
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # image file for user profile picture.
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # repr does how our object is printed out, similar to __str__()
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

#Once the classes are built in main flask app
#then we can call the db object on the python command line to build the database tables.

# Create db table in SQLAlchemy, where flaskblog is the main file of the web application
=> from flaskblog import db
=> db.create_all()

#import classes object, which acts as tables in SQLAlchemy, this is called ORM
=> from flaskblog import User, Post

# create object of classes with following information
=> user_1 = User(username='Mayank', email='mayank@gmail.com', password='password')
#The user_1 is added in the user table
=> db.session.add(user_1)
#But to reflect those changes in the database, we'll commit the db session.
=> db.session.commit()
#Displays all the rows present in User table
=> User.query.all()
#Displays first row of the column
=> User.query.first()

#To drop all the tables in databse.
=> db.drop_all()
