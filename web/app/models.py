from . import db
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)

    def __init__(self, id, username):
        self.id = id
        self.username = username

    def __repr__(self):
        return '%r' % self.id


def save():
    user = User(4, '3test')
    db.session.add(user)
    db.session.commit()


def query():
    user = User.query.all()
    for u in user:
        print(u)
        print(type(u))
        print(type(user))

