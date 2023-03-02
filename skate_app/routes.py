from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from skate_app.models import User, Post, Comment
from flask_login import login_user, logout_user, login_required, current_user
from skate_app.forms import PostForm, SignupForm, LoginForm, CommentForm
from werkzeug.utils import secure_filename
import os

from skate_app.extensions import app, db, bcrypt

main = Blueprint("main", __name__)
auth = Blueprint("auth", __name__)

@main.route('/')
def homepage():
    posts = Post.query.all()

    posts = id_to_name_post(posts)
    
    return render_template('index.html', posts = posts)

@main.route('/add_trick', methods=['POST', 'GET'])
@login_required
def add_trick():
    form = PostForm()

    if form.validate_on_submit():
        filename = secure_filename(form.photo.data.filename)
        file = form.photo.data
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        new_post = Post(
            name=form.name.data,
            date=form.date.data,
            photo=url_for('static', filename=filename),
            poster_id=current_user.id
        )

        db.session.add(new_post)
        db.session.commit()

        flash('Posted successfully')

        return redirect(url_for('main.post_details', post_id=new_post.id))

    return render_template('add-trick.html', form=form)

@main.route('/user/<user_id>', methods=["GET"])
def user_details(user_id):
    user = User.query.get(user_id)
    tricks = db.session.query(Post).filter_by(poster_id=user_id).all()

    tricks = id_to_name_post(tricks)
    
    return render_template('your-tricks.html', user=user, tricks=tricks)

@main.route('/post/<post_id>', methods=["GET", 'POST'])
def post_details(post_id):
    post = Post.query.get(post_id)
    form = CommentForm()
    comments_data = db.session.query(Comment).filter_by(attached_to_id=post_id).all()

    comments = id_to_name_comment(comments_data)

    data = {
        'form':form,
        'post':post,
        'comments':comments
    }

    return render_template('view-trick.html', **data)

@main.route('/comments/<post_id>', methods=['POST', 'GET'])
def comment(post_id):
    form = CommentForm()

    if form.validate_on_submit():
        print('comment added')

        new_comment = Comment(
            text=form.text.data,
            created_by = current_user.id,
            attached_to_id = post_id
        )

        db.session.add(new_comment)
        db.session.commit()

        flash('comment added')
        
        return redirect(url_for('main.post_details', post_id=post_id)) 

    return redirect(url_for('main.post_details', post_id=post_id, form=form))


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

@auth.route('/logout', methods=["GET"])
def logout():
    logout_user()
    return redirect(url_for('main.homepage'))

def id_to_name_post(posts):
    results = []
    for post in posts:
        results.append({
            'id':post.id,
            'name':post.name,
            'date':post.date,
            'photo':post.photo,
            'poster':User.query.get(post.poster_id)
            })

    return results

def id_to_name_comment(comments):
    results = []
    for comment in comments:
        results.append({
            'text':comment.text,
            'created_by':User.query.get(comment.created_by)
            })

    return results