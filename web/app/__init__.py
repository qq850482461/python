from flask import Flask
from werkzeug.routing import BaseConverter
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import *
from flask_sqlalchemy import SQLAlchemy
# 登录页面过滤需要的包

from .views import init_views

# 正则表达式
class RegexConverter(BaseConverter):  # 正则转换器
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


bootstrap = Bootstrap()  # 实例化Bootstrap
nav = Nav()  # 实例化Nav
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.url_map.converters['regex'] = RegexConverter  # 正则转换器
    app.config.from_pyfile('config')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:lzh3101977@localhost:3306/test'
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    # 创建一个导航对象
    nav.register_element('top', Navbar('Flask入门', View('主页', 'index'), View('登录', 'login'), View('上传', 'upload'),View('关于', 'about')))
    nav.init_app(app)  # 放入flask对象中
    bootstrap.init_app(app)
    db.init_app(app)
    init_views(app)
    return app







