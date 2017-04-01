from flask import Blueprint
flask_admin = Blueprint('flask_admin',__name__)
from . import views

# from flask_admin import BaseView,expose
# from flask_login import login_required,current_user
#
#
# class MyView(BaseView):
#     @expose('/')
#     def index(self):
#         return self.render('index.html')
