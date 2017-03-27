from os import path
from flask import render_template, request, redirect, url_for, make_response, flash, session
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from . import main  # 导入蓝图
from .forms import CommentForm, PostForm  # 表单
from .. import db
from ..models import Post, Comment
from datetime import datetime

nowtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@main.route('/')  # 装饰起用于根目录
def index():
    return render_template('index.html', title='Welcome',time=datetime.utcnow())


@main.route('/user/<regex("[a-z]{3}"):user_id>')  # 正则表达式验证url
def user(user_id):
    return 'User {0}'.format(user_id)


# 关于页面
@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/upload', methods=['GET', 'POST'])  # 上传文件的http方法
def upload():
    if request.method == 'POST':
        f = request.files['file']  # 这里的的键值file对应upload.html的name="file"
        basepath = path.abspath(path.dirname(__file__))  # 返回path规范化的绝对路径
        upload_path = path.join(basepath, 'static/')  # 拼接路径
        f.save(upload_path + secure_filename(f.filename))  # 检验上传文件并且保存
        return redirect(url_for('upload'))  # 指定为postback
    return render_template('upload.html')


# 自己定义一个错误页面传入错误代码,如果不是蓝图就是用errorhandler
@main.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title='404'), 404



# 发表页面
@main.route('/edit', methods=['GET', 'POST'])
@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id=0):
    form = PostForm()
    #新增发表
    if id == 0:
        if form.validate_on_submit():
            print(current_user, type(current_user), nowtime)
            #autchor是User模型的backref的参数，autchor存储一个User对象ORM层将会知道怎么完成author_id字段，所以这里只需要传入当前的用户对象。
            new_post = Post(title=form.title.data, body=form.body.data, author=current_user, created=nowtime)
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for('main.posts', id=new_post.id))
    #重新编辑页面
    else:
        #查询POST模型中的id返回对象
        post = Post.query.get_or_404(id)
        print(post.id,nowtime)
        if form.validate_on_submit():
            post.title = form.title.data
            post.body = form.body.data

            db.session.add(post)
            db.session.commit()
            return redirect(url_for('main.posts', id=post.id))

        #给前端传入数据库保存的数据
        form.title.data = post.title
        form.body.data = post.body

    return render_template('new.html', form=form)


# 发表后的显示页面
@main.route('/posts/<int:id>', methods=['GET', 'POST'])
def posts(id):
    form = CommentForm()#表单对象
    # 获取文章的ID对象没有就返回404
    post = Post.query.get_or_404(id)
    # 提交评论表单
    if form.validate_on_submit():
        # 这里的post=post是关联文章的Post数据库模型的backref的post对象==当前文章的变量post存放的文章id对象
        comment = Comment(body=form.body.data, post=post, created=nowtime)
        db.session.add(comment)
        db.session.commit()

    # form对象传到前端模版，post对象传到前端模版(前端使用的变量名字 = views中定义的对象)
    return render_template('detail.html', form=form, post=post, time=nowtime)


# 显示博客文章列表页面
@main.route('/blog', methods=['GET', 'POST'])
def blog():
    #查询所有文章对象
    #post = Post.query.all()
    page_idnex = request.args.get("page", 1, type=int)  # 获取url中get请求的参数
    query = Post.query.order_by(Post.created.desc())#order_by是升序 .desc()是降序，这里做一个反向排序
    pagination = query.paginate(page_idnex,per_page=5,error_out=False)#SQLAlchemy的分页方法
    post = pagination.items

    return render_template('blog.html',posts=post,pagination=pagination)

# 实现博客的管理编辑删除页面
@main.route('/bloglists',methods=['GET', 'POST'])
@login_required
def bloglists():
    #post = Post.query.all()
    post = Post.query.order_by(Post.created.desc()) #先升序再降序
    return render_template('bloglists.html',posts=post)

