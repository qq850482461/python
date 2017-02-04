from flask import render_template, request, redirect, url_for, make_response, flash, session
from . import auth #这里用.代表当前包的__init__
from .forms import LoginForm


@auth.route('/login', methods=['GET', 'POST'])  # http方法
def login():
    # if request.method == 'POST':
    #     username = request.form['username']#对应的是login的name标签获取里面的内容
    #     password = request.form['password']
    #     print(username,password)#获取前端post传过来的参数可以进行一些验证处理等
    # # else:#如果是用get方法就用这个方法获取前端穿进来的数据
    # #     username = request.args['username']
    form = LoginForm()
    username = None
    if form.validate_on_submit():  # 第一次访问服务器会收到一个没有表单数据的get请求所以这里会变成false，表单数据通过验证就会返回true
        session['username'] = form.username.data
        username = session.get('username')
        session['password'] = form.password.data
        password = session.get('password')
        flash('登录成功')
        print(username, password, type(username))

        return redirect(url_for('login'))
    return render_template('login.html', title='登录', form=form, name=username)
