import time
import uuid
import hmac
import hashlib
from datetime import datetime, timedelta
from flask import render_template, request, jsonify, redirect, url_for, flash, session, current_app
from flask_login import login_user, login_required, current_user
from models import db, User, get_local_now
from . import auth_bp

# In-memory store for active Web QR Login sessions
# Format: {token: {'user_id': None, 'created_at': float, 'status': 'pending'|'scanned'|'authenticated'|'expired'}}
QR_LOGIN_SESSIONS = {}
QR_EXPIRATION_SECONDS = 120  # 2 minutes countdown


def cleanup_expired_tokens():
    now = time.time()
    expired_keys = [k for k, v in QR_LOGIN_SESSIONS.items() if now - v['created_at'] > QR_EXPIRATION_SECONDS + 60]
    for k in expired_keys:
        QR_LOGIN_SESSIONS.pop(k, None)


def generate_personal_badge_token(user_id):
    """สร้าง Signed Token ประจำตัวผู้ใช้ที่ปลอดภัยและไม่สามารถปลอมแปลงได้"""
    secret = current_app.config.get('SECRET_KEY', 'default-equipment-secret-key-2026')
    raw = f"ATCC-BADGE:{user_id}"
    sig = hmac.new(secret.encode('utf-8'), raw.encode('utf-8'), hashlib.sha256).hexdigest()[:16]
    return f"{raw}:{sig}"


def verify_personal_badge_token(badge_token):
    """ตรวจสอบ Signed Token จากบัตรประจำตัว และคืนค่า user_id ถ้าถูกต้อง"""
    if not badge_token or not badge_token.startswith("ATCC-BADGE:"):
        return None
    try:
        parts = badge_token.strip().split(":")
        if len(parts) != 3:
            return None
        prefix, user_id_str, sig = parts
        user_id = int(user_id_str)
        expected_token = generate_personal_badge_token(user_id)
        if hmac.compare_digest(badge_token.strip(), expected_token):
            return user_id
    except Exception:
        return None
    return None


# ==========================================
# 1. API: สร้าง QR Code เข้าสู่ระบบบนหน้าจอคอมพิวเตอร์
# ==========================================
@auth_bp.route('/api/qr-login/generate')
def qr_login_generate():
    cleanup_expired_tokens()
    token = str(uuid.uuid4())
    QR_LOGIN_SESSIONS[token] = {
        'user_id': None,
        'created_at': time.time(),
        'status': 'pending'
    }
    
    # URL ที่ QR Code จะเข้ารหัส เพื่อให้มือถือสแกนแล้วเปิดหน้าเว็บยืนยันได้ทันที
    auth_url = url_for('auth.qr_auth_page', token=token, _external=True)
    
    return jsonify({
        'success': True,
        'token': token,
        'auth_url': auth_url,
        'expires_in': QR_EXPIRATION_SECONDS
    })


# ==========================================
# 2. API: ตรวจสอบสถานะการล็อกอิน (สำหรับหน้าจอคอมพิวเตอร์ Polling)
# ==========================================
@auth_bp.route('/api/qr-login/status')
def qr_login_status():
    token = request.args.get('token')
    if not token or token not in QR_LOGIN_SESSIONS:
        return jsonify({'status': 'expired', 'message': 'QR Code หมดอายุหรือไม่มีอยู่ในระบบ'})
        
    sess_data = QR_LOGIN_SESSIONS[token]
    
    # เช็กหมดอายุ (2 นาที)
    if time.time() - sess_data['created_at'] > QR_EXPIRATION_SECONDS:
        sess_data['status'] = 'expired'
        return jsonify({'status': 'expired', 'message': 'QR Code หมดอายุ กรุณากดรีเฟรช'})
        
    if sess_data['status'] == 'authenticated' and sess_data['user_id']:
        user = db.session.get(User, sess_data['user_id'])
        if user:
            login_user(user, remember=True)
            session['show_login_intro'] = True
            
            # ลบ token ออกเพื่อความปลอดภัย
            QR_LOGIN_SESSIONS.pop(token, None)
            
            redirect_target = url_for('admin.dashboard') if user.is_admin() else url_for('user.dashboard')
            return jsonify({
                'status': 'authenticated',
                'redirect_url': redirect_target,
                'user_name': user.full_name
            })
            
    return jsonify({'status': sess_data['status']})


# ==========================================
# 3. API: มือถือกดยืนยันการเข้าสู่ระบบบนคอมพิวเตอร์
# ==========================================
@auth_bp.route('/api/qr-login/authorize', methods=['POST'])
@login_required
def qr_login_authorize():
    data = request.get_json() or {}
    token = data.get('token') or request.form.get('token')
    
    # หาก token มาในรูป URL ให้สกัดเอาเฉพาะ token
    if token and "/" in token:
        token = token.rstrip("/").split("/")[-1]
        
    if not token or token not in QR_LOGIN_SESSIONS:
        return jsonify({'success': False, 'message': 'QR Code นี้หมดอายุแล้วหรือไม่ถูกต้อง'}), 400
        
    sess_data = QR_LOGIN_SESSIONS[token]
    if time.time() - sess_data['created_at'] > QR_EXPIRATION_SECONDS:
        sess_data['status'] = 'expired'
        return jsonify({'success': False, 'message': 'QR Code นี้หมดอายุแล้ว กรุณารีเฟรชที่หน้าจอคอมพิวเตอร์'}), 400
        
    sess_data['user_id'] = current_user.id
    sess_data['status'] = 'authenticated'
    
    return jsonify({
        'success': True,
        'message': f'ยืนยันการเข้าสู่ระบบสำหรับ {current_user.full_name} สำเร็จ! หน้าจอคอมพิวเตอร์จะเข้าสู่ระบบทันที',
        'user_name': current_user.full_name
    })


# ==========================================
# 4. WEB PAGE: หน้ายืนยันการเข้าสู่ระบบเมื่อสแกนด้วยกล้องมือถือทั่วไป
# ==========================================
@auth_bp.route('/qr-auth/<token>', methods=['GET', 'POST'])
def qr_auth_page(token):
    # หากยังไม่ได้ Login ในมือถือ -> ให้ Login ก่อนแล้วเด้งกลับมาหน้านี้
    if not current_user.is_authenticated:
        flash('กรุณาเข้าสู่ระบบในมือถือเพื่อยืนยันการเข้าใช้งานบนคอมพิวเตอร์', 'info')
        return redirect(url_for('auth.login', next=url_for('auth.qr_auth_page', token=token)))
        
    if token not in QR_LOGIN_SESSIONS or (time.time() - QR_LOGIN_SESSIONS[token]['created_at'] > QR_EXPIRATION_SECONDS):
        flash('QR Code นี้หมดอายุแล้ว กรุณากดรีเฟรชที่หน้าจอคอมพิวเตอร์และสแกนใหม่', 'danger')
        return redirect(url_for('user.dashboard'))
        
    if request.method == 'POST':
        sess_data = QR_LOGIN_SESSIONS[token]
        sess_data['user_id'] = current_user.id
        sess_data['status'] = 'authenticated'
        flash(f'เข้าสู่ระบบบนหน้าจอคอมพิวเตอร์สำเร็จในชื่อ "{current_user.full_name}" เรียบร้อยแล้ว!', 'success')
        return render_template('qr_auth_success.html', user=current_user)
        
    return render_template('qr_auth_confirm.html', token=token, user=current_user)


# ==========================================
# 5. API: ล็อกอินผ่านการสแกนบัตรนักศึกษา / บัตรอาจารย์ QR Code ประจำตัว
# ==========================================
@auth_bp.route('/api/qr-badge-login', methods=['POST'])
def qr_badge_login():
    data = request.get_json() or {}
    badge_token = data.get('badge_token', '').strip()
    
    user_id = verify_personal_badge_token(badge_token)
    if not user_id:
        return jsonify({'success': False, 'message': 'บัตร QR Code ไม่ถูกต้องหรือข้อมูลไม่สมบูรณ์'}), 400
        
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'success': False, 'message': 'ไม่พบบัญชีผู้ใช้งานนี้ในระบบ'}), 404
        
    login_user(user, remember=True)
    session['show_login_intro'] = True
    
    redirect_target = url_for('admin.dashboard') if user.is_admin() else url_for('user.dashboard')
    
    return jsonify({
        'success': True,
        'message': f'ยินดีต้อนรับ {user.full_name} เข้าสู่ระบบสำเร็จ!',
        'redirect_url': redirect_target,
        'user': {
            'name': user.full_name,
            'role': user.role
        }
    })


# ==========================================
# 6. PRINTABLE BADGE: หน้าพิมพ์บัตรนักศึกษา / บุคลากร QR Code สำหรับใช้งานจริง
# ==========================================
@auth_bp.route('/print-badge/<int:user_id>')
@login_required
def print_badge(user_id):
    # สิทธิ์: ผู้ใช้พิมพ์ของตัวเอง หรือ Admin พิมพ์ของทุกคนได้
    if current_user.id != user_id and not current_user.is_admin():
        flash('คุณไม่มีสิทธิ์เข้าถึงบัตรของผู้ใช้งานท่านอื่น', 'danger')
        return redirect(url_for('user.dashboard'))
        
    target_user = db.session.get(User, user_id)
    if not target_user:
        flash('ไม่พบผู้ใช้งาน', 'danger')
        return redirect(url_for('user.dashboard'))
        
    badge_token = generate_personal_badge_token(target_user.id)
    
    return render_template('badge_print.html',
                           user=target_user,
                           badge_token=badge_token,
                           generated_date=get_local_now().strftime('%d/%m/%Y'))


# ==========================================
# 7. PRINTABLE POSTER: ป้ายโปสเตอร์ QR Code ประชาสัมพันธ์เข้าสู่เว็บไซต์จากภายนอก
# ==========================================
@auth_bp.route('/qr-poster')
def qr_poster():
    site_url = request.host_url.rstrip('/')
    return render_template('qr_poster_print.html', site_url=site_url)
