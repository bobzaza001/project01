from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

from . import auth_routes, qr_login_routes
