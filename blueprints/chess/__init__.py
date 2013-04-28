from flask import Blueprint
from views import init

chess = Blueprint('chess', __name__, template_folder='templates', static_folder='static')
init(chess)
