from . import login_manager, db
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from markdown import markdown
import bleach#清理html标签



#多对多关系中的两个表之间的一个关联表
tags = db.Table('post_tags',
    db.Column('post_id',db.Integer,db.ForeignKey('posts.id')),
    db.Column('tag_id',db.Integer,db.ForeignKey('tag.id'))
)



# 这里用户需要继承flask_login的UserMixin
# 采用一对多的数据结构
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(80))

    posts = db.relationship('Post', backref='author',lazy='dynamic')  # 关联发表文章

    def __repr__(self):  # 这里决定current_user返回的是什么
        return 'User {0}'.format(self.username)


# 这个方法是用于用户登录后返回数据库的ID到session中用来登录的
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


# 发表文章模型
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    body = db.Column(db.Text())
    body_html = db.Column(db.Text())
    created = db.Column(db.DateTime,default=datetime.utcnow)

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='post',lazy='dynamic')  # 关联评论
    tags = db.relationship('Tag',secondary=tags,backref=db.backref('posts',lazy='dynamic'),lazy='dynamic')#多对多关联

    def __repr__(self):
        return "<post_id={0}>".format(self.id)


    #注册监听函数
    @staticmethod
    def on_body_changed(target, value, oldvalue, initiator):
        # 需要转换的标签
        allowed_tags = [
            'a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
            'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
            'h1', 'h2', 'h3', 'p', 'img','toc'
        ]
        # 需要提取的标签属性，否则会被忽略掉
        attrs = {
            '*': ['class'],
            'a': ['href', 'rel'],
            'img': ['src', 'alt']
        }
        #清理html标签和markdown扩展
        target.body_html = bleach.linkify(
            bleach.clean(
                markdown(value,extensions=['markdown.extensions.extra',
                                           'markdown.extensions.codehilite',
                                           'markdown.extensions.toc',
                                           'markdown.extensions.tables'],output_format='html'),
                tags=allowed_tags,
                attributes=attrs,
                strip=True
            )
        )

#监听body变动添加到
db.event.listen(Post.body, 'set', Post.on_body_changed)

#标签
class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(255))


    def __repr__(self):
        return "{0}".format(self.title)

# 评论
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text())
    created = db.Column(db.DateTime,default=datetime.utcnow)

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    def __repr__(self):
        return "body内容是: {0}".format(self.body)



