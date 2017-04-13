from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from werkzeug.routing import BaseConverter#自定义正则表达式
from flask_login import LoginManager#登录模块
from flask_pagedown import PageDown#markdown预览模块
from flask_moment import Moment#时钟实时刷新

from flask_admin import Admin,AdminIndexView#flask-admin
from flask_admin.contrib.sqla import ModelView #admin的模型视图
from .admin import MyView,MyHomeView,MyUserModel,MyPostModel,MyCommentModel#引用自己写的

from flask_babelex import Babel #flask-admin 中文化    db.init_app(app)



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
flask_admin = Admin(name='博客后台',template_mode='bootstrap3',index_view=MyHomeView())#实例化flask-admin
babel = Babel() #实例化babel

login_manager = LoginManager() #实例化登录模块
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'#制定系统默认的登录页面

#创建一个app
def create_app():
    app = Flask(__name__)
    app.url_map.converters['regex'] = RegexConverter  # 正则转换器
    app.config.from_pyfile('config')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:lzh3101977@localhost:3306/test' #数据库参数要使用pymysql来做数据库驱动
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    bootstrap.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)
    moment.init_app(app)
    flask_admin.init_app(app)
    flask_admin.add_view(MyView(name="统计？"))#如果加了endpoit就会覆盖类名小写的myview
    from .models import User,Post,Comment#引入写在方法内部避免交叉引用
    flask_admin.add_view(MyUserModel(User,db.session,category="数据模型",name="用户"))
    flask_admin.add_view(MyPostModel(Post,db.session, category="数据模型",name="文章"))
    flask_admin.add_view(MyCommentModel(Comment,db.session,category="数据模型",name="评论"))

    babel.init_app(app)


    app.config['BABEL_DEFAULT_LOCALE'] = 'zh_CN' #配置中文

    #注册蓝图
    from .auth import auth as auth_blueprint
    from .main import main as main_blueprint
    app.register_blueprint(auth_blueprint)#注册蓝图,url_prefix='/auth'
    app.register_blueprint(main_blueprint)#定义静态文件目空了,,static_folder='static'

    app.jinja_env.filters['date'] = date_filter #注册自己定义的过滤函数

    app.debug = True
    return app







