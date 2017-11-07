from flask_script import Manager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:lzh3101977@192.168.1.55:3306/cmdb'
    db.init_app(app)

    return app


