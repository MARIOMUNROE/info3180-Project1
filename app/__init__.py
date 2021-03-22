from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

#app.config['SECRET_KEY'] = "somesecretkey"
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://project1:pr1@localhost/project1'

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True 
app.config['UPLOAD_FOLDER'] = './app/static/uploads'

app.config.from_object(Config)
from app import views