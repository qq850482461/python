from flask import Flask,render_template,request,redirect,url_for
from werkzeug.routing import BaseConverter
from werkzeug.utils import secure_filename
from os import path

class RegexConverter(BaseConverter):#正则转换器
    def __init__(self,url_map,*items):
        super(RegexConverter,self).__init__(url_map)
        self.regex = items[0]

app = Flask(__name__)
app.url_map.converters['regex'] = RegexConverter#正则转换器

@app.route('/')#装饰起用于 根目录
def index():
    return '<h1>这是主页</h1>'


@app.route('/<name>') #hello目录
def hello(name):
    return render_template('hello.html',name=request.method)


@app.route('/user/<regex("[a-z]{3}"):user_id>')
def user(user_id):
    return 'User {0}'.format(user_id)

@app.route('/about')
def about():
    return "about"

@app.route('/projects/')
@app.route('/our-works/')#多个url匹配同一个视图函数
def projects():
    return "这是一个页面"

@app.route('/login',methods=['GET','POST'])#http方法
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
    else:
        username = request.args['username']

    return render_template('login.html',method=request.method)

@app.route('/upload',methods=['GET','POST'])#上传文件
def upload():
    if request.method=='POST':
        f = request.files['file']
        basepath = path.abspath(path.dirname(__file__))#返回path规范化的绝对路径
        upload_path = path.join(basepath, 'static/uploads/')#拼接路径
        f.save(upload_path+secure_filename(f.filename))
        return redirect(url_for('upload'))
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(port=80,debug = True)
