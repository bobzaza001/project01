from flask import Blueprint

user_bp = Blueprint('user', __name__, url_prefix='/user')

from . import view_routes, borrow_return_routes, scan_routes
