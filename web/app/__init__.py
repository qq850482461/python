from flask import Flask
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import *
from flask_sqlalchemy import SQLAlchemy
from werkzeug.routing import BaseConverter



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
    nav.register_element('top', Navbar('Flask入门', View('主页', 'main.index'), View('登录', 'auth.login'), View('注册', 'auth.register'),View('上传', 'main.upload'),View('关于', 'main.about')))
    nav.init_app(app)  # 放入flask对象中
    bootstrap.init_app(app)
    db.init_app(app)
    from .auth import auth as auth_blueprint
    from .main import main as main_blueprint
    app.register_blueprint(auth_blueprint)#注册蓝图,url_prefix='/auth'
    app.register_blueprint(main_blueprint,static_folder='static')#定义静态文件目空了
    app.debug = True
    return app







