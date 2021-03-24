from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager
from .config import Config



app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True 
app.config['UPLOAD_FOLDER'] = './app/static/uploads'
app.config['SECRET_KEY'] = "somesecretkey"
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://project1:project1@localhost/project1'

# # Flask-Login login manager
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'

app.config.from_object(Config)
from app import views