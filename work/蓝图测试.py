from flask import Flask,Blueprint

test = Blueprint('test',__name__)
app = Flask(__name__)
app.register_blueprint(test)

@app.route('/')
def index():
    return 'index test'

@app.route('/test')
def test():
    return 'test'


if __name__ =="__main__":
    app.run()