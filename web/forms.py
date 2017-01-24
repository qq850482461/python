from flask_wtf import  Form
from  wtforms import SelectField,PasswordField
from  wtforms.validators import DataRequired
class LoginForm(Form):
    username=SelectField(validators=[DataRequired()])
    password=PasswordField(validators=[DataRequired()])