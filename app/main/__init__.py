from flask import Blueprint

main = Blueprint('main', __name__, template_folder='templates', static_folder='static')

# from .. import main
from . import views
from ..models import TaskEncoder

main.json_encoder = TaskEncoder
