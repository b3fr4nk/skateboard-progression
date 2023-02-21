from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from flask_login import login_user, logout_user, login_required, current_user
from skate_app.models import User, Post, Trick, Comment
from skate_app.forms import TrickForm, SignUpForm

from skate_app.extensions import app, db, bcrypt

main = Blueprint("main", __name__)
auth = Blueprint("auth", __name__)

@main.route('/')
def homepage():
    posts = Post.query.all()
    
    return render_template('index.html', posts = posts)

@main.route('/new_trick', methods=['POST'])
@login_required
def new_trick():
    form = TrickForm()

    #TODO validate form and add to db
    return render_template('new_trick.html', form=form)

@main.route('/user/<user_id>', methods=["GET"])
def user_details(user_id):
    user = User.query.get(user_id)
    tricks = db.session.query(User).filter_by(id=user_id).first().tricks
    
    return render_template('your-tricks.html', user=user, tricks=tricks)

@main.route('/post/<post_id>', methods=["GET"])
def post_details(post_id):
    post = Post.query.get(post_id)

    return render_template('view_trick', post=post)

@auth.route('/login', methods=["GET", "POST"])
def sign_up():
    form = SignUpForm

    #TODO validate form and add to db
