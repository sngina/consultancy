from werkzeug.utils import redirect
from ..import auth
from ..auth.forms import LoginForm
from flask import render_template , request ,url_for ,abort
from . import main
from ..models import User ,Blog, Comment
from flask_login import login_required , current_user
from .. import db
from .forms import BlogForm , CommentForm


@main.route('/')
def index():
    blog = Blog.get_blogs()
    title = 'Home'

    return render_template('home.html' , title = title)


@main.route('/pitches/new/', methods = ['GET','POST'])
@login_required
def new_blog():
    form = BlogForm()

    if form.validate_on_submit():
        description = form.description.data
        title = form.title.data
        owner_id = current_user
        new_blog = Blog(owner_id = current_user._get_current_object().id,title = title , description = description)
        db.session.add(new_blog)
        db.session.commit()

        return redirect(url_for('main.index'))

    return render_template('blog.html' , form = form)


@main.route('/comment/new/<int:blog_id>', methods = ['GET','POST'])
@login_required
def new_comment(blog_id):
    form = CommentForm()
    blog= Blog.query.get(blog_id)
    if form.validate_on_submit():
        description = form.description.data

        new_comment = Comment(description = description, user_id = current_user._get_current_object().id,blog_id = blog_id)
        db.session.add(new_comment)
        db.session.commit()

        return redirect(url_for('.new_comment' ,blog_id = blog_id))
    all_comments = Comment.query.filter_by(blog_id = blog_id).all()
    return render_template('comments.html', form = form, comment = all_comments, blog = blog )



