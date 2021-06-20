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
