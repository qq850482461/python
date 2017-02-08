from . import db,login_manager
from flask_login import UserMixin

#这里用户需要继承flask_login的UserMixin
class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(80))

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def __repr__(self):
        return '%r' % self.username

#这个方法是用于用户登录后返回数据库的ID到session中用来登录的
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
    # return User.get(user_id)