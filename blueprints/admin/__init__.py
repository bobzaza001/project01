from flask import Blueprint

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

from . import equipment_manage_routes, request_manage_routes, location_routes, notification_routes, report_routes, audit_log_routes
