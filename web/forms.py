from flask_wtf import FlaskForm
from  wtforms import PasswordField,StringField,SubmitField,BooleanField
from  wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username=StringField(label='帐号',validators=[DataRequired()])
    password=PasswordField(label='密码',validators=[DataRequired()])
    remember_me = BooleanField('记住用户名', default=False)
    submit = SubmitField(label='提交')