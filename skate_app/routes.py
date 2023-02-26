from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from skate_app.models import User, Post, Comment
from flask_login import login_user, logout_user, login_required, current_user
from skate_app.forms import PostForm, SignupForm, LoginForm, CommentForm

from skate_app.extensions import app, db, bcrypt

main = Blueprint("main", __name__)
auth = Blueprint("auth", __name__)

@main.route('/')
def homepage():
    posts = Post.query.all()
    
    return render_template('index.html', posts = posts)

@main.route('/add_trick', methods=['POST', 'GET'])
@login_required
def add_trick():
    form = PostForm()

    if form.validate_on_submit():
        new_post = Post(
            name=form.name.data,
            date=form.date.data,
            photo=form.photo.data
        )

        db.session.add(new_post)
        db.session.commit()

        flash('Posted successfully')

        return redirect(url_for('main.post_details', post_id=new_post.id))

    return render_template('add-trick.html', form=form)

@main.route('/user/<user_id>', methods=["GET"])
def user_details(user_id):
    user = User.query.get(user_id)
    tricks = db.session.query(User).filter_by(id=user_id).first().tricks
    
    return render_template('your-tricks.html', user=user, tricks=tricks)

@main.route('/post/<post_id>', methods=["GET"])
def post_details(post_id):
    post = Post.query.get(post_id)

    return render_template('view_trick', post=post)

@main.route('/comment/<post_id>', methods=['POST', 'GET'])
def comments(post_id):
    post = Post.query.get(post_id)
    form = CommentForm()

    #TODO validate and add to db

    return render_template('/comments.html', form=form)


@auth.route('/signup', methods=["GET", "POST"])
def sign_up():
    form = SignupForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(
            username=form.username.data,
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()

        flash('Account created')
        return redirect(url_for('auth.login'))

    return render_template('signup.html', form=form)

@auth.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user, remember=True)
        
        return redirect(url_for('main.homepage'))

    return render_template('login.html', form=form)