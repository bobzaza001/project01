from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user, login_required

# นามสกุลไฟล์ที่อนุญาตให้อัปโหลด
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    """ตรวจสอบว่าไฟล์เป็นนามสกุลรูปภาพที่อนุญาตหรือไม่"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def admin_required(f):
    """Decorator สำหรับหน้าที่ admin เท่านั้นเข้าถึงได้"""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        # ตรวจสอบว่าเป็นแอดมินหรือไม่
        if not current_user.is_admin():
            flash('คุณไม่มีสิทธิ์เข้าถึงหน้านี้', 'danger')
            # จะ redirect กลับไปหน้าแดชบอร์ด (ซึ่งเราจะตั้งชื่อ route ใน blueprint เป็น user.dashboard หรือ admin.dashboard)
            # เราใช้เพียง 'user.dashboard' หรืออาจจะ redirect ไปหน้า index ก็ได้
            # เปลี่ยน url_for('dashboard') เป็นชื่อ Blueprint ถ้าจำเป็น หรือสร้าง fallback 
            return redirect(url_for('user.dashboard'))
        return f(*args, **kwargs)
    return decorated_function
