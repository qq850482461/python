from . import db
class User(db.Model):
    __tablename__ ='users'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username = db.Column(db.String(80),unique=True)
    password = db.Column(db.String(32),nullable=False)

    def __init__(self,username,password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '%r' % self.username



