from flask_wtf import FlaskForm
from wtforms import PasswordField,StringField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Length,Regexp,email,EqualTo

class LoginForm(FlaskForm):
    username=StringField(label='帐号',validators=[DataRequired()])
    password=PasswordField(label='密码',validators=[DataRequired()])
    remember_me = BooleanField('记住用户名', default=False)
    submit = SubmitField(label='提交')

class RegisterForm(FlaskForm):
    '''
    EqualTo 是等于
    用wtf表单工具验证帐号长度以及用正则表达式验证
    '''
    username = StringField(label='用户名',validators=[DataRequired(),Length(1,18,message='帐号长度在1到18位'),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',flags=0,message='用户名必须由字母数、字数、下划线或 . 组成')])
    email = StringField(label='邮箱地址',validators=[DataRequired(),email(message='邮箱地址不正确')])
    password = StringField(label='密码',validators=[DataRequired(),Length(6,15,message='密码长度在6到15位')])
    password2 = StringField(label='确认密码', validators=[DataRequired(),EqualTo('password',message='密码必须一致')])
    submit = SubmitField(label='注册')
