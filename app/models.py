from sqlalchemy.orm import session
from . import db
from sqlalchemy.sql import func
from . import login_manager
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash,check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

    # function of the user

class User(UserMixin ,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    pass_secure = db.Column(db.String(255))
    blog = db.relationship('Blog', backref='user', lazy='dynamic')
    comment = db.relationship('Comment', backref = 'user', lazy = 'dynamic')

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    def __repr__(self):
        return f'{self.username}'

# the blog function
class Blog(db.Model):
    __tablename__ = 'blog'
    id = db.Column(db.Integer, primary_key = True)
    owner_id = db.Column(db.Integer ,db.ForeignKey('users.id'))
    name = db.Column(db.String(),index = True)
    content = db.Column(db.String())
    comment = db.relationship('Comment', backref = 'blog', lazy = 'dynamic')

   # the saving function
    def save_blog(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_blogs(cls, id):
        blogs = Blog.query.order_by(blog_id=id).desc().all()
        return blogs

    def __repr__(self):
        return f'Blog {self.description}'
# added class comment
class Comment(db.Model):
    __tablename__='comments'
    
    id = db.Column(db.Integer,primary_key=True)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable= False)
    comment = db.Column(db.String(2000))

    # saving comments
    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    
    def __repr__(self):
        return f"Comment : id: {self.id} comment: {self.description}"

class  Quotes():
   def __init__(self,author,quotes):
       self.author = author
       self.quotes = quotes

