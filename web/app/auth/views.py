from flask import render_template, request, redirect, url_for, make_response, flash, session
from . import auth  # 这里用.代表当前包的__init__ #导入蓝图
from .forms import LoginForm, RegisterForm
from .. import db  # 引用包最外面的__init__
from ..models import User
from flask_login import login_user,logout_user

#登录页面
@auth.route('/login', methods=['GET', 'POST'])  # http方法
def login():
    # if request.method == 'POST':
    #     username = request.form['username']#对应的是login的name标签获取里面的内容
    #     password = request.form['password']
    #     print(username,password)#获取前端post传过来的参数可以进行一些验证处理等
    # # else:#如果是用get方法就用这个方法获取前端穿进来的数据
    # #     username = request.args['username']
    form = LoginForm()
    if form.validate_on_submit():  # 第一次访问服务器会收到一个没有表单数据的get请求所以这里会变成false，表单数据通过验证就会返回true
        user = User.query.filter_by(username=form.username.data,password=form.password.data).first()
        username = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            login_user(user)
            return redirect(url_for('main.blog'))
        elif username is None:
            flash('{0}账户不存在'.format(form.username.data))
        else:
            flash("您输入的密码不正确")
    return render_template('login.html', title='登录', form=form)

#登出页面
@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))



# 注册页面
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():  # 表单验证通过为true
        user = User(username=form.username.data, password=form.password2.data, email=form.email.data)
        try:
            db.session.add(user)
            db.session.commit()
            flash('{0}注册成功！！'.format(form.username.data))
            return redirect(url_for('main.blog'))
        except:
            db.session.rollback()
            flash('{0}注册失败或帐号已经被注册'.format(form.username.data))
            return redirect(url_for('auth.register'))
    return render_template('register.html', title='注册', form=form)
