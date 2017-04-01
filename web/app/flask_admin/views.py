from . import flask_admin
from flask_admin import BaseView,expose
from flask_login import login_required,current_user


class MyView(BaseView):
    @expose('/')
    def index(self):
        #路由的用法和renter_template一样
        return self.render('admin/index.html')