from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
# The secret key is used to protect to modifying forms and forgery from hackers once deployed.
app.config['SECRET_KEY'] = '44b504f855931d5d8bec3800d32a4287'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # three /// are used to represent the relative path from the current directory

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

login_manager.login_view = 'login' # name of the login route
login_manager.login_message_category = 'info'

# importing routes here to avoid circular imports problem.
from flaskblog import routes
