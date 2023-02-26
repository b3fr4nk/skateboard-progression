from skate_app.extensions import db
from flask_login import UserMixin

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)
    photo = db.Column(db.String, nullable=False)
    poster_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    poster = db.relationship('User')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_comment = db.relationship('User')
    attached_to_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post_comment = db.relationship('Post')

class Tutorial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    instructions = db.Column(db.String)
    video = db.Column(db.String, nullable=False)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
