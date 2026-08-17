"""
extensions.py — Flask extensions สร้าง instance แยกเพื่อป้องกัน circular import
"""
from flask_mail import Mail

mail = Mail()
