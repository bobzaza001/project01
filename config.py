import os
from dotenv import load_dotenv

# โหลดค่าจากไฟล์ .env
load_dotenv()

# === ไฟล์ตั้งค่าหลักของระบบ ===
# ไฟล์นี้เก็บค่าคอนฟิกต่างๆ เช่น SECRET_KEY สำหรับจัดการ session
# และที่อยู่ฐานข้อมูล SQLite

class Config:
    # คีย์ลับสำหรับเข้ารหัส session (ควรเปลี่ยนเป็นค่าที่ซับซ้อนกว่านี้ในระบบจริง)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'lab-equipment-secret-key-2024'
    
    # กำหนดที่อยู่ฐานข้อมูล SQLite (เก็บไฟล์ app.db ไว้ในโฟลเดอร์เดียวกับโปรเจกต์)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.db')
    
    # ปิดการแจ้งเตือนการเปลี่ยนแปลงของ SQLAlchemy (ไม่จำเป็นและกินทรัพยากร)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Google OAuth
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')

    # Security settings for Session Cookies
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'False').lower() in ('true', '1')
    SESSION_COOKIE_SAMESITE = 'Lax'

    # === Flask-Mail (Gmail SMTP) ===
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', os.environ.get('MAIL_USERNAME', ''))

    # === Notification Toggles (default: enabled) ===
    NOTIFY_ON_APPROVE = True
    NOTIFY_ON_REJECT = True
    NOTIFY_DUE_REMINDER = True

    # === APScheduler ===
    SCHEDULER_API_ENABLED = False
