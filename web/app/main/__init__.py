#功能模块
from flask import Blueprint

main = Blueprint('main',__name__)
from . import views
