import os
import logging
from flask import Flask
from flask_login import LoginManager
from config import Config
from models import db, User
from extensions import mail

# === สร้าง Flask Application ===
app = Flask(__name__)
app.config.from_object(Config)

# === ตั้งค่าการอัปโหลดไฟล์ ===
UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # จำกัดขนาดไฟล์ 16MB

# สร้างโฟลเดอร์ uploads ถ้ายังไม่มี
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# === เชื่อมต่อฐานข้อมูล ===
db.init_app(app)

# === ตั้งค่า Flask-Mail ===
mail.init_app(app)

# === ตั้งค่า OAuth ===
from oauth_setup import oauth
oauth.init_app(app)
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

# === ตั้งค่า Flask-Login ===
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'กรุณาเข้าสู่ระบบก่อนใช้งาน'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# === นำเข้าและลงทะเบียน Blueprints โครงสร้างใหม่ ===
from blueprints.auth import auth_bp
from blueprints.admin import admin_bp
from blueprints.user import user_bp

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(user_bp)

# === ตั้งค่า APScheduler — ตรวจสอบรายการใกล้ครบกำหนดทุกวัน 08:00 น. ===
from flask_apscheduler import APScheduler

scheduler = APScheduler()
scheduler.init_app(app)

@scheduler.task('cron', id='due_reminder_job', hour=8, minute=0,
                misfire_grace_time=3600)
def scheduled_due_reminder():
    """ตรวจสอบรายการยืมที่ใกล้ครบกำหนดคืนและส่งอีเมลแจ้งเตือนผู้ยืม"""
    with app.app_context():
        from notifications import check_and_send_due_warnings
        check_and_send_due_warnings()

# ป้องกัน Scheduler รันซ้ำ 2 ครั้งใน debug mode (Flask reloader สร้าง 2 process)
if os.environ.get('WERKZEUG_RUN_MAIN') == 'true' or not app.debug:
    scheduler.start()

# === Custom Error Handlers ===
from flask import render_template as _rt

@app.errorhandler(404)
def page_not_found(e):
    return _rt('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    logging.error(f'Internal Server Error: {e}')
    return _rt('errors/500.html'), 500

# ==================== จุดเริ่มต้นโปรแกรม ====================
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    is_debug = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 'yes')
    app.run(debug=is_debug, port=5000)
