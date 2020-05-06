from flask import Flask, request, jsonify 
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy  
from flask_marshmallow import Marshmallow 
from flask_heroku import Heroku
import os

app = Flask(__name__)
CORS(app)
heroku = Heroku(app) 

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")

db = SQLAlchemy(app) 
ma = Marshmallow(app)

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)  
  first_name = db.Column(db.String(24), nullable=False)
  last_name = db.Column(db.String(24), nullable=False)
  username = db.Column(db.String(24), nullable=False)
  email = db.Column(db.String(48), nullable=False)  
  password = db.Column(db.String(24), nullable=False)
  children = db.relationship("Blog", backref="user")

  def __init__(self, first_name, last_name, username, email, password):#children go in the parans
    self.first_name = first_name
    self.last_name = last_name
    self.username = username
    self.email = email
    self.password = password
    self.children = children


class Blog(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(24), nullable=False)
  content = db.Column(db.String(250), nullable=False)
  blog_image_url = db.Column(db.String(600), nullable=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

  def __init__(self, title, content, blog_image_url, user_id):
    self.title = title
    self.content = content
    self.blog_image_url = blog_image_url
    self.user = user_id


class UserSchema(ma.Schema):
  class Meta: 
    fields = ("id", "first_name", "last_name", "username", "email", "password", "children")#Children may need to go in these parans here.


class BlogSchema(ma.Schema):
  class Meta:
    fields = ("id", "title", "content", "blog_image_url", "user_id")


user_schema = UserSchema()
users_schema = UserSchema(many=True)

blog_schema = BlogSchema()
blogs_schema = BlogSchema(many=True)

# *** PLEASE KEEP IN MIND, THERE IS NO 'PUT' ROUTE FOR THE USER MODEL/SCHEMAS BECAUSE I 
# *** HAVE NO PURPOSE FOR IT, A USER SHOULD ONLY BE ABLE TO MODIFY CERTAIN INFORMATION OF 
# *** THEIRS, OR REMOVE THEIR ACCOUNT. MANIPULATING AN ACCOUNT TO SHOW A COMPLETELY DIFFERENT 
# *** PERSON'S INFORMATION WOULD JUST ENCOURAGE AND ENALBE POOR BEHAVIOR OF 'TROLL' USERS.

# Routes are listed below! This first set of routes listed is purely for the user table.
# TABLE ORDER: User table first. Blog table second. User table routes you see below:

# GET ALL USERS
# GET ONE USER BY THEIR ID
# POST A USER
# PATCH A USER
# DELETE A USER

# Route to query for ALL USERS.
@app.route("/display_users", methods=["GET"])
def display_users():
  user_all = User.query.all()
  result = users_schema.dump(user_all)
  
  return jsonify(result)

# Route to query for A SINGULAR USER, by Id.
@app.route("/display_user/<id>", methods=["GET"])
def display_user(id):
  user = User.query.get(id)
  result = users_schema.dump(user_all)
  
  return jsonify(result)

# Route to create a user
@app.route("/create_user", methods=["POST"])
def create_user():
  first_name = request.json["first_name"]
  last_name = request.json["last_name"]
  username = request.json["username"]
  email = request.json["email"]
  password = request.json["password"]
  children = request.json["children"] #########

  new_user = User(first_name, last_name, username, email, password, children) #(children)

  db.session.add(new_user)
  db.session.commit()

  user = User.query.get(new_user.id)
  return user_schema.jsonify(user)

# The below will only be an available option to a user, for their own user information.
# So for example, if Tyson made a user, and Ryan made a user,
# they wouldn't be able to edit each other's user-information.

@app.route("/edit_user/<id>", methods=["PATCH"])
def edit_user(id):
  user = User.query.get(id)

  new_first_name = request.json["first_name"]
  new_last_name = request.json["last_name"]
  new_username = request.json["username"]
  new_password = request.json["password"]
  new_email = request.json["email"]

  user.first_name = new_first_name
  user.last_name = new_last_name
  user.username = new_first_name
  user.email = new_email
  user.password = new_password

  db.session.commit()

  return user_schema.jsonify(user)

# Route for completely removing a USER from the database.
@app.route("/remove_user/<id>", methods=["DELETE"])
def remove_user(id):
  blog_records = Blog.query.all()
  record = User.query.get(id)
  
  db.session.delete(blog_records)
  db.session.delete(record)
  db.session.commit()

  return jsonify("Your user information has been successfully removed.\nYour blog posts have all been removed as well.")

# Above is a complete list of all routes for the User Table.
# Below, is a complete list of all routes for the Blog Table.

# GET ALL BLOG ENTRIES
# GET AN ENTRY BY ID
# POST AN ENTRY
# PATCH AN ENTRY
# DELETE AN ENTRY
# DELETE ALL ENTRIES

# Route to GET all blog posts.
@app.route("/display_entries", methods=["GET"])
def get_entries():
  all_entries = Blog.query.all()
  result = blogs_schema.dump(all_entries)

  return jsonify(result)

# Route to GET one blog entry by it's Id.
@app.route("/display_entry/<id>", methods=["GET"])
def get_entry(id):
  entry = Blog.query.get(id)
  result = blog_schema.dump(entry)

  return jsonify(result)

# Route to POST a blog entry.
@app.route("/create_entry", methods=["POST"])
def create_entry():
  title = request.json["title"]
  content = request.json["content"]
  blog_image_url = request.json["blog_image_url"]
  user_id = request.json["user_id"]

  new_entry = Blog(title, content, blog_image_url, user_id)

  db.session.add(new_entry)
  db.session.commit()
  
  entry = Blog.query.get(new_entry.id)
  return blog_schema.jsonify(new_entry)

# Route to PATCH a blog entry.
@app.route("/edit_entry/<id>", methods=["PATCH"])
def edit_entry(id):
  entry = Blog.query.get(id)

  new_title = request.json["title"]
  new_content = request.json["content"]
  new_blog_image_url = request.json["blog_image_url"]

  entry.title = new_title
  entry.content = new_content
  entry.blog_image_url = new_blog_image_url

  db.session.commit()
  return blog_schema.jsonify(entry)
  
# Route to DELETE ONE entry.
@app.route("/remove_entry/<id>", methods=["DELETE"])
def remove_entry(id):
  record = Blog.query.get(id)

  db.session.delete(record)
  db.session.commit()
  
  return jsonify("Your blog entry has been successfully deleted.")

# Route to DELETE ALL BLOG ENTRIES
@app.route("/remove_entries", methods=["DELETE"])
def remove_all_entries():
  all_blog_records = Blog.query.all()
  
  db.session.delete(all_blog_records)
  db.session.commit()

  return jsonify("All of your blog entries have been successfully deleted.")


if __name__ == "__main__":
  app.run(debug=True)