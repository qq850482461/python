from os import path, pardir
from flask import render_template, request, redirect, url_for, flash, session, abort, jsonify, send_from_directory
from werkzeug.utils import secure_filename  # 上传文件
from flask_login import login_required, current_user  # 登录模块
from . import main  # 导入蓝图
from .forms import CommentForm, PostForm  # 表单
from .. import db  # 引用orm
from ..models import Post, Comment, Tag  # 表单
from datetime import datetime
import os

nowtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 当前时间
basepath = path.abspath(path.join(path.dirname(__file__), pardir, pardir, 'upload'))  # 路径


# 全局模板变量,上下文处理器
@main.app_context_processor
def tag_list():
    tags = Tag.query.all()
    # 过滤没有关联的tag
    rm_repeat = []
    for i in tags:
        if i.posts:
            rm_repeat.append(i)
    return dict(tag_list=rm_repeat)


@main.route('/')  # 装饰起用于根目录
def index():
    return render_template('index.html', title='Welcome')


@main.route('/user/<regex("[a-z]{3}"):user_id>')  # 正则表达式验证url
def user(user_id):
    return 'User {0}'.format(user_id)


# 关于页面
@main.route('/about')
def about():
    return render_template('about.html')


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
    # 新增发表
    if id == 0:
        if form.validate_on_submit():
            # autchor是User模型的backref的参数，autchor存储一个User对象ORM层将会知道怎么完成author_id字段，所以这里只需要传入当前的用户对象。
            new_post = Post(
                title=form.title.data, body=form.body.data, author=current_user, created=nowtime
            )
            tag = Tag.query.filter_by(title=form.tag.data).first()  # 拿到tag对象
            # 判断是否有这个tag没有就新建一个
            if tag == None:
                tag = Tag(title=form.tag.data)
            new_post.tags = [tag]  # 关联Tag的标签
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for('main.posts', id=new_post.id))
    # 重新编辑页面
    else:
        # 查询POST模型中的id返回模型对象
        post = Post.query.get_or_404(id)

        if form.validate_on_submit():
            post.title = form.title.data
            post.body = form.body.data
            # 关联标签
            tag = Tag.query.filter_by(title=form.tag.data).first()
            if tag == None:
                tag = Tag(title=form.tag.data)
            post.tags = [tag]

            db.session.add(post)
            db.session.commit()
            return redirect(url_for('main.posts', id=post.id))

        # 给前端传入数据库保存的数据(这样就可以在原文的基础上编辑)
        form.title.data = post.title
        form.body.data = post.body
        form.tag.data = post.tags[0].title  # 得到一个tag列表

    return render_template('new.html', form=form, title="发表文章")


# 发表后的显示页面
@main.route('/posts/<int:id>', methods=['GET', 'POST'])
def posts(id):
    form = CommentForm()  # 表单对象
    # 获取文章的ID对象没有就返回404
    post = Post.query.get_or_404(id)

    # 提交评论表单
    if form.validate_on_submit():
        # 这里的post=post是关联文章的Post数据库模型的backref的post对象==当前文章的变量post存放的文章id对象
        comment = Comment(body=form.body.data, post=post, created=nowtime)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('main.posts', id=post.id))

    # form对象传到前端模版，post对象传到前端模版(前端使用的变量名字 = views中定义的对象)
    return render_template('post.html', form=form, post=post, time=nowtime)


# 显示博客文章列表页面
@main.route('/blog', methods=['GET', 'POST'])
def blog():
    search = request.args.get('search')
    page_idnex = request.args.get("page", 1, type=int)  #获取url中get请求的参数
    if search:
        value = "%{0}%".format(search)
        query = Post.query.filter(Post.title.like(value))
        pagination = query.paginate(page_idnex, per_page=2, error_out=False)
        post = pagination.items
        count = len(query.all())
        return render_template('blog_search.html', posts=post, pagination=pagination, display_search=True,num=count)
    else:
        query = Post.query.order_by(Post.created.desc())  # order_by是升序 .desc()是降序，这里做一个反向排序
        pagination = query.paginate(page_idnex, per_page=5, error_out=False)
        post = pagination.items
        return render_template('blog.html', posts=post, pagination=pagination, display_search=True)




# 文章的标签页面
@main.route('/tag/<tag>', methods=['GET', 'POST'])
def tag(tag):
    page_idnex = request.args.get("page", 1, type=int)
    tag = Tag.query.filter_by(title=tag).first_or_404()
    query = tag.posts  # backref拿到post的所有对象
    pagination = query.paginate(page_idnex, per_page=5, error_out=False)
    post = pagination.items

    search_post = tag.posts.all()
    count = len(search_post)
    return render_template('tag.html', num=count, tag=tag, posts=post, pagination=pagination)


# 实现博客的管理编辑删除页面
@main.route('/bloglists', methods=['GET', 'POST'])
@login_required
def bloglists():
    page_idnex = request.args.get("page", 1, type=int)
    query = Post.query.order_by(Post.created.desc())  # 先升序再降序
    pagination = query.paginate(page_idnex, per_page=10, error_out=False)
    post = pagination.items
    return render_template('bloglists.html', posts=post, pagination=pagination)


# 实现文章删除功能
@main.route('/posts/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def post_delete(id):
    # 创建一个res的json对象
    response = {
        'status': 200,
        'message': 'success'
    }
    # 查询文章ID拿到数据对象
    post = Post.query.filter_by(id=id).first()
    # 如果数据库没有这个文章ID,post就是空列表
    if not post:
        response['status'] = 404
        response['message'] = 'Post Not Found'
        return jsonify(response)
    else:
        # 提交删除
        db.session.delete(post)
        db.session.commit()
        return jsonify(response)


# 编辑器上传图片
@main.route('/upload/', methods=["POST"])
def upload():
    if request.method == "POST":
        file = request.files.get("editormd-image-file")  # 拿到前端编辑器上传name标签
        if not file:
            res = {
                'success': 0,
                'message': "上传失败"
            }
            return jsonify(res)
        else:
            ex = path.splitext(file.filename)[1]  # 把文件名分成文件名称和扩展名，拿到后缀
            filename = datetime.now().strftime('%Y%m%d%H%M%S') + ex
            try:
                file.save(path.join(basepath, filename))
            except:
                res = {
                    'success': 0,
                    'message': "upload路径出错或者保存不了图片"
                }
            else:
                res = {
                    'success': 1,
                    'mess    age': "上传成功",
                    'url': url_for('.image', filename=filename)
                }
            return jsonify(res)


# 上传文件访问服务
@main.route('/image/<filename>')
def image(filename):
    return send_from_directory(basepath, filename)
