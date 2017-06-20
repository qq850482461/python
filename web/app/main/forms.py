from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField #表单类型
from wtforms.validators import DataRequired,Length #表单验证器

class PostForm(FlaskForm):
    title = StringField(label="标题",validators=[DataRequired()])
    tag = StringField(label="标签", validators=[DataRequired()])
    body = TextAreaField(label="正文",validators=[DataRequired()])
    submit = SubmitField(label='发表博客')

class CommentForm(FlaskForm):
    body = TextAreaField(label='评论',validators=[DataRequired()])
    submit = SubmitField(label='发表')

