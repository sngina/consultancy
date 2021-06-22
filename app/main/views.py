from email.utils import quote
from werkzeug.utils import redirect
from ..import auth
from ..auth.forms import LoginForm
from flask import render_template , request ,url_for ,abort
from . import main
from ..models import User ,Blog, Comment
from flask_login import login_required , current_user
from .. import db
from .forms import BlogForm , CommentForm
from app.main import forms
from ..request import get_quotes

@main.route('/')
def index():
    blog = Blog.query.all()

    title = 'Home'
    quotes = get_quotes()
    
    return render_template('home.html' , title = title ,quotes = quotes,blogs = blog )


@main.route('/pitches/new/', methods = ['GET','POST'])
@login_required
def new_blog():
    form = BlogForm()

    if form.validate_on_submit():
        content = form.content.data
        name = form.name.data
        
        new_blog = Blog(name = name , content = content ,owner_id = current_user.id)
        db.session.add(new_blog)
        db.session.commit()

        return redirect(url_for('main.index'))

    return render_template('blog.html' , form = form)


@main.route('/comment/new/<int:blog_id>', methods = ['GET','POST'])
@login_required
def new_comment(blog_id):
    commentform = CommentForm()
    blog= Blog.query.get(blog_id)
    if commentform.validate_on_submit():
        comment = commentform.description.data

        new_comment = Comment(comment = comment, user_id = current_user.id,blog_id = blog_id)
        new_comment.save_comment()

        db.session.add(new_comment)
        db.session.commit()

        return redirect(url_for('.new_comment' ,blog_id = blog_id))
    all_comments = Comment.query.filter_by(blog_id = blog_id).all()
    return render_template('comments.html', form = commentform, comment = all_comments, blog = blog )
@main.route('/delete/new/<int:id>', methods = ['GET','POST'])
@login_required
def deleteComment(id):
    todele = Comment.query.filter_by(id = id).first()
    db.session.delete(todele)
    db.session.commit()
    return redirect(url_for('main.index'))





