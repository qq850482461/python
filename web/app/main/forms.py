from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,Length
from flask_pagedown.fields import PageDownField

class PostForm(FlaskForm):
    title = StringField(label="标题",validators=[DataRequired()])
    tag = StringField(label="标签", validators=[DataRequired()])
    body = PageDownField(label="正文",validators=[DataRequired()])
    submit = SubmitField(label='发表博客')

class CommentForm(FlaskForm):
    body = TextAreaField(label='评论',validators=[DataRequired()])
    submit = SubmitField(label='发表')