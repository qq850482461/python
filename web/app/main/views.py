from os import path ,pardir
from flask import render_template, request, redirect, url_for,flash, session,abort,jsonify,send_from_directory
from werkzeug.utils import secure_filename #上传文件
from flask_login import login_required, current_user #登录模块
from . import main  # 导入蓝图
from .forms import CommentForm, PostForm  # 表单
from .. import db #引用orm
from ..models import Post, Comment #表单
from datetime import datetime
import os

nowtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #当前时间
basepath = path.abspath(path.join(path.dirname(__file__),pardir,pardir,'upload')) #路径

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

#上传文件
# @main.route('/upload/', methods=['GET', 'POST'])  # 上传文件的http方法
# def upload():
#     if request.method == 'POST':
#         f = request.files['file']  # 这里的的键值file对应upload.html的name="file"
#         basepath = path.abspath(path.dirname(__file__))  # 返回path规范化的绝对路径
#         upload_path = path.join(basepath, 'static/')  # 拼接路径
#         f.save(upload_path + secure_filename(f.filename))  # 检验上传文件并且保存
#         return redirect(url_for('upload'))  # 指定为postback
#     return render_template('upload.html')


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
            #autchor是User模型的backref的参数，autchor存储一个User对象ORM层将会知道怎么完成author_id字段，所以这里只需要传入当前的用户对象。
            new_post = Post(title=form.title.data,tag=form.tag.data,body=form.body.data,author=current_user, created=nowtime)
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for('main.posts', id=new_post.id))
    #重新编辑页面
    else:
        #查询POST模型中的id返回对象
        post = Post.query.get_or_404(id)
        if form.validate_on_submit():
            post.title = form.title.data
            post.body = form.body.data
            post.tag = form.tag.data

            db.session.add(post)
            db.session.commit()
            return redirect(url_for('main.posts', id=post.id))

        #给前端传入数据库保存的数据(这样就可以在原文的基础上编辑)
        form.title.data = post.title
        form.body.data = post.body
        form.tag.data = post.tag

    return render_template('new.html',form=form,title="发表文章")


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
        return redirect(url_for('main.posts', id=post.id))

    # form对象传到前端模版，post对象传到前端模版(前端使用的变量名字 = views中定义的对象)
    return render_template('post.html', form=form, post=post, time=nowtime)


# 显示博客文章列表页面
@main.route('/blog', methods=['GET', 'POST'])
def blog():

    page_idnex = request.args.get("page", 1, type=int)  # 获取url中get请求的参数
    query = Post.query.order_by(Post.created.desc())#order_by是升序 .desc()是降序，这里做一个反向排序
    pagination = query.paginate(page_idnex,per_page=5,error_out=False)#SQLAlchemy的分页方法
    post = pagination.items

    # all_query = Post.query.filter(Post.tag!=None).all()#查询所有不是None的tag数据
    # tag_list = [i.tag for i in all_query]#所有数据的tag列表
    # rm_duplication = list(set(tag_list))#去重后的列表

    return render_template('blog.html',posts=post,pagination=pagination)

#文章的标签页面
@main.route('/tag/<tag>',methods=['GET','POST'])
def tag(tag):
    tagname = str(tag)#转换URL得到tag变成str

    page_idnex = request.args.get("page", 1, type=int)
    # query = Post.query.order_by(Post.tag.desc())#查询的结果all
    # pagination = query.paginate(page_idnex,per_page=5,error_out=False)
    pagination = Post.query.filter_by(author_id=tagname).all().paginate(page, per_page=5, error_out = False)
    print(type(pagination))
    post = pagination.items

    #num = len(query)#tag个数

    all_query = Post.query.filter(Post.tag!=None).all()#查询所有不是None的tag数据
    tag_list = [i.tag for i in all_query]#所有数据的tag列表
    rm_duplication = list(set(tag_list))#去重后的列表

    # if not query:
    #     abort(404)

    # return render_template('tag.html',posts=post,tagname=tagname,tag_list=rm_duplication,pagination=pagination)



# 实现博客的管理编辑删除页面
@main.route('/bloglists',methods=['GET', 'POST'])
@login_required
def bloglists():
    post = Post.query.order_by(Post.created.desc()) #先升序再降序
    return render_template('bloglists.html',posts=post)


#实现文章删除功能
@main.route('/posts/<int:id>/delete',methods=['GET','POST'])
@login_required
def post_delete(id):
    #创建一个res的json对象
    response = {
        'status':200,
        'message':'success'
    }
    #查询文章ID拿到数据对象
    post = Post.query.filter_by(id=id).first()
    #如果数据库没有这个文章ID,post就是空列表
    if not post:
        response['status'] = 404
        response['message'] = 'Post Not Found'
        return jsonify(response)
    else:
        #提交删除
        db.session.delete(post)
        db.session.commit()
        return jsonify(response)


#编辑器上传图片
@main.route('/upload/',methods=["POST"])
def upload():
    if request.method == "POST":
        file = request.files.get("editormd-image-file")#拿到前端编辑器上传name标签
        if not file:
            res = {
                'success' : 0,
                'message' : "上传失败"
            }
        else:
            ex = path.splitext(file.filename)[1]#把文件名分成文件名称和扩展名，拿到后缀
            filename = datetime.now().strftime('%Y%m%d%H%M%S') + ex
            file.save(path.join(basepath,filename))
            res = {
                'success' : 1,
                'message' : "上传成功",
                'url' : url_for('.image',filename = filename)
            }
        return jsonify(res)



#上传文件访问服务
@main.route('/image/<filename>')
def image(filename):
    return send_from_directory(basepath,filename)
