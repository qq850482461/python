from . import db
from flask_sqlalchemy import SQLAlchemy

class Test(db.Model):
    __tablename__ = 'test'
    id = db.Column(db.Integer(), primary_key=True)
    test = db.Column(db.String(80))