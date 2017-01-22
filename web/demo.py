
from flask_script import Manager
from flask import Flask,render_template
from markdown import markdown #自定义jinja2过滤器
from functools import reduce

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',title="<h1>Hello world!!</h1>",body="##header2##")

#自己定义一个jinja2的过滤器
@app.template_filter('md')
def markdown_to_html(txt):
    return markdown(txt)

#定义一个过滤函数
def read_md(filename):
    #重点：不管是写入还是读取出现编码错误就在open函数添加encodeing
    with open(filename,encoding='utf-8') as f:
        content = reduce(lambda x, y: x + y, f.readlines())
        return content

#上下文处理器函数
@app.context_processor
def inject_method():
    return dict(read_md=read_md)

@app.route('/test')
def test():
    return 'test'

if __name__ =="__main__":
    app.run()