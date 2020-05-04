from flask import Flask, request, jsonify 
from flask_sqlalchemy import SQLAlchemy  
from flask_cors import CORS 
from flask_marshmallow import Marshmallow 
from flask_heroku import Heroku

import os 

app = Flask(__name__)
CORS(app)
heroku = Heroku(app) 

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app) 
ma = Marshmallow(app) 


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)  
  first_name = db.Column(db.String(24), nullable=False)
  last_name = db.Column(db.String(24), nullable=False)
  username = db.Column(db.String(24), nullable=False)
  email = db.Column(db.String(48), nullable=False)  
  password = db.Column(db.String(24), nullable=False)
  can_post = db.Column(db.Boolean(True))

  def __init__(self, first_name, last_name, username, email, password, can_post):
    self.first_name = first_name
    self.last_name = last_name
    self.username = username
    self.email = email
    self.password = password
    self.can_post = can_post


class BlogShare(db.Model):
  __tablename__ = "Shared Content"
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(24), nullable=False)
  content = db.Column(db.String(250), nullable=False)
  blog_image_url = db.Column(db.String(600), nullable=True)

  def __init__(self, title, content, blog_image_url):
    self.title = title
    self.content = content
    self.blog_image_url = blog_image_url

class UserSchema(ma.Schema):
  class Meta: 
    fields = ("id", "first_name", "last_name", "username", "email", "password", "can_post")


class BlogShareSchema(ma.Schema):
  class Meta:
    fields = ("id", "title", "content", "blog_image_url")

user_schema = UserSchema()
users_schema = UserSchema(many=True)

blog_share_schema = BlogShareSchema()
blogs_share_schema = BlogShareSchema(many=True)

@app.route("/")
def home():
  return "<h2>Capstone API, can you see this text, Tyson?</h2>"

  






