from . import login_manager,db
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from markdown import markdown





# 这里用户需要继承flask_login的UserMixin
# 采用一对多的数据结构
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(80))

    posts = db.relationship('Post', backref='author')  # 关联发表文章

    # def __init__(self, username, password, email):
    #     self.username = username
    #     self.password = password
    #     self.email = email

    def __repr__(self):  # 这里决定current_user返回的是什么
        return 'User %r' % self.username


# 这个方法是用于用户登录后返回数据库的ID到session中用来登录的
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


# 发表文章模型
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255))
    tag = db.Column(db.String(255))
    body = db.Column(db.Text())
    body_html = db.Column(db.Text())
    created = db.Column(db.DateTime)  # , index=True, default=datetime.utcnow

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='post')# 关联用户数据库

    def __repr__(self):  # 这里决定current_user返回的是什么
        return 'posts_id %r' % self.id

    @staticmethod
    def on_body_changed(targer, value, oldvalue, initiator):
        if value is None or (value is ''):
            targer.body_html = ''
        else:
            targer.body_html = markdown(value)
    # @staticmethod
    # def on_body_changed(target, value, oldvalue, initiator):
    #     # 需要转换的标签
    #     allowed_tags = [
    #         'a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
    #         'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
    #         'h1', 'h2', 'h3', 'p', 'img'
    #     ]
    #     # 需要提取的标签属性，否则会被忽略掉
    #     attrs = {
    #         '*': ['class'],
    #         'a': ['href', 'rel'],
    #         'img': ['src', 'alt']
    #     }
    #     target.content_html = bleach.linkify(
    #         bleach.clean(
    #             markdown(value, output_format='html'),
    #             tags=allowed_tags,
    #             attributes=attrs,
    #             strip=True
    #         )
    #     )
db.event.listen(Post.body, 'set', Post.on_body_changed)


# 评论
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    body = db.Column(db.Text())
    created = db.Column(db.DateTime)

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    def __repr__(self):
        return "body内容是: {0}".format(self.body)
