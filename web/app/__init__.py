from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from werkzeug.routing import BaseConverter#自定义正则表达式
from flask_login import LoginManager#登录模块
from flask_pagedown import PageDown#markdown预览模块
from flask_moment import Moment#时钟实时刷新
from flask_admin import Admin #flask-flask_admin
from flask_babelex import Babel #flask-flask_admin 中文化


#重构flask-flask_admin,这两种方法都可以重写
class Flask_Admin(Admin):
    def __init__(self):
        #Admin.__init__(self)
        super(Flask_Admin, self).__init__()
        self.template_mode = 'bootstrap3'


# 正则表达式
class RegexConverter(BaseConverter):  # 正则转换器
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

#定义jinja2的过滤器函数
def date_filter(s):
    s = str(s)
    time = s[:10]
    return time



bootstrap = Bootstrap()  # 实例化Bootstrap
db = SQLAlchemy()#数据库实例化
pagedown = PageDown()#博客事实预览的pagedown
moment = Moment()#实例化时间刷新模块
admin = Flask_Admin()#实例化flask-flask_admin
babel = Babel() #实例化babel

login_manager = LoginManager() #实例化登录模块
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'#制定系统默认的登录页面


def create_app():
    app = Flask(__name__)
    app.url_map.converters['regex'] = RegexConverter  # 正则转换器
    app.config.from_pyfile('config')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:lzh3101977@localhost:3306/test' #数据库参数要使用pymysql来做数据库驱动
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)
    moment.init_app(app)
    admin.init_app(app)

    from .flask_admin.views import MyView
    admin.add_view(MyView(name='Hello 1', endpoint='test1', category='Test'))
    admin.add_view(MyView(name='Hello 2', endpoint='test2', category='Test'))
    babel.init_app(app)


    app.config['BABEL_DEFAULT_LOCALE'] = 'zh_CN' #配置中文

    #注册蓝图
    from .auth import auth as auth_blueprint
    from .main import main as main_blueprint
    from .flask_admin import flask_admin as admin_blueprint
    app.register_blueprint(auth_blueprint)#注册蓝图,url_prefix='/auth'
    app.register_blueprint(main_blueprint)#定义静态文件目空了,,static_folder='static'
    app.register_blueprint(admin_blueprint)

    app.jinja_env.filters['date'] = date_filter #注册自己定义的过滤函数

    app.debug = True
    return app







