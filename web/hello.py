from flask import Flask,render_template,request,redirect,url_for,make_response,abort,flash,session
from werkzeug.routing import BaseConverter
from werkzeug.utils import secure_filename
from os import path
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import *
from flask_sqlalchemy import SQLAlchemy
#登录页面过滤需要的包
from web.forms import LoginForm


#正则表达式
class RegexConverter(BaseConverter):#正则转换器
    def __init__(self,url_map,*items):
        super(RegexConverter,self).__init__(url_map)
        self.regex = items[0]

app = Flask(__name__)
app.url_map.converters['regex'] = RegexConverter#正则转换器
Bootstrap(app)#实例化Bootstrap
nav = Nav()#实例化Nav
app.config.from_pyfile('config')
#创建一个导航对象
nav.register_element('top',Navbar('Flask入门',View('主页','index'), View('登录','login'),View('上传','upload'),View('关于','about')))
nav.init_app(app)#放入flask对象中

@app.route('/')#装饰起用于根目录
def index():
    response = make_response(render_template('index.html',title='Welcome'))
    response.set_cookie('username','')#cookie
    return response


@app.route('/<name>') #hello目录
def hello(name):
    return render_template('hello.html',name=name)


@app.route('/user/<regex("[a-z]{3}"):user_id>')#正则表达式验证url
def user(user_id):
    return 'User {0}'.format(user_id)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/projects/')
@app.route('/our-works/')#多个url匹配同一个视图函数
def projects():
    return "这是一个页面"

@app.route('/login',methods=['GET','POST'])#http方法
def login():
    # if request.method == 'POST':
    #     username = request.form['username']#对应的是login的name标签获取里面的内容
    #     password = request.form['password']
    #     print(username,password)#获取前端post传过来的参数可以进行一些验证处理等
    # # else:#如果是用get方法就用这个方法获取前端穿进来的数据
    # #     username = request.args['username']
    form = LoginForm()
    username = None
    if form.validate_on_submit():#第一次访问服务器会收到一个没有表单数据的get请求所以这里会变成false，表单数据通过验证就会返回true
        session['username'] = form.username.data#
        username = session.get('username')
        flash('登录成功',username)
        print(username,type(username))
        return redirect(url_for('login'))
    return render_template('login.html',title='登录',form=form,name=username)

@app.route('/upload',methods=['GET','POST'])#上传文件的http方法
def upload():
    if request.method=='POST':
        f = request.files['file']#这里的的键值file对应upload.html的name="file"
        basepath = path.abspath(path.dirname(__file__))#返回path规范化的绝对路径
        upload_path = path.join(basepath,'static/')#拼接路径
        f.save(upload_path+secure_filename(f.filename))#检验上传文件并且保存
        return redirect(url_for('upload'))#指定为postback
    return render_template('upload.html')

@app.errorhandler(404)#自己定义一个错误页面传入错误代码
def page_not_found(error):
    return render_template('404.html'),404



if __name__ == '__main__':

    app.run(port=80,debug = True)
