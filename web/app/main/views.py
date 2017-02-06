from os import path
from flask import render_template, request, redirect, url_for, make_response, flash, session
from werkzeug.utils import secure_filename
from . import main

@main.route('/')  # 装饰起用于根目录
def index():
    return render_template('index.html', title='Welcome')
    # return '测试'

# @main.route('/<name>')  # hello目录
# def hello(name):
#     return render_template('hello.html', name=name)


@main.route('/user/<regex("[a-z]{3}"):user_id>')  # 正则表达式验证url
def user(user_id):
    return 'User {0}'.format(user_id)


@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/projects/')
@main.route('/our-works/')  # 多个url匹配同一个视图函数
def projects():
    return "这是一个页面"


@main.route('/upload', methods=['GET', 'POST'])  # 上传文件的http方法
def upload():
    if request.method == 'POST':
        f = request.files['file']  # 这里的的键值file对应upload.html的name="file"
        basepath = path.abspath(path.dirname(__file__))  # 返回path规范化的绝对路径
        upload_path = path.join(basepath, 'static/')  # 拼接路径
        f.save(upload_path + secure_filename(f.filename))  # 检验上传文件并且保存
        return redirect(url_for('upload'))  # 指定为postback
    return render_template('upload.html')


@main.errorhandler(404)  # 自己定义一个错误页面传入错误代码
def page_not_found(error):
    return render_template('404.html'), 404
