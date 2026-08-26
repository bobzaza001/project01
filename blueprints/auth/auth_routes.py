from flask import render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User, get_local_now
from . import auth_bp
import collections
from datetime import datetime, timedelta

# Simple IP-based rate limiting for login
login_attempts = collections.defaultdict(list)

def is_ip_blocked(ip):
    now = get_local_now()
    # Keep only failed attempts from the last 5 minutes
    login_attempts[ip] = [t for t in login_attempts[ip] if now - t < timedelta(minutes=5)]
    return len(login_attempts[ip]) >= 5

def record_failed_attempt(ip):
    login_attempts[ip].append(get_local_now())

@auth_bp.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('user.dashboard'))
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('user.dashboard'))
    
    if request.method == 'POST':
        ip = request.remote_addr
        if is_ip_blocked(ip):
            flash('คุณพยายามเข้าสู่ระบบผิดพลาดหลายครั้งเกินไป กรุณารอ 5 นาที', 'danger')
            return redirect(url_for('auth.login'))

        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember', False)
        
        user = User.query.filter(
            (User.username == username) | (User.full_name == username) | (User.email == username)
        ).first()
        
        if user is None or not user.check_password(password):
            record_failed_attempt(ip)
            flash('ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง', 'danger')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=bool(remember))
        session['show_login_intro'] = True
        flash(f'ยินดีต้อนรับ {user.full_name}!', 'success')
        
        next_page = request.args.get('next')
        if next_page and next_page.startswith('/'):
            return redirect(next_page)
            
        if user.is_admin():
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('user.dashboard'))
    
    return render_template('login.html')

@auth_bp.route('/login/google')
def login_google():
    from oauth_setup import oauth
    redirect_uri = url_for('auth.auth_callback', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@auth_bp.route('/auth/callback')
def auth_callback():
    from oauth_setup import oauth
    token = oauth.google.authorize_access_token()
    user_info = token.get('userinfo')
    
    if not user_info:
        flash('ไม่สามารถดึงข้อมูลจาก Google ได้', 'danger')
        return redirect(url_for('auth.login'))
        
    email = user_info.get('email', '')
    full_name = user_info.get('name', '')
    
    # ตรวจสอบโดเมน .ac.th
    if not email.endswith('.ac.th'):
        flash('กรุณาใช้อีเมลของสถาบัน (.ac.th) ในการเข้าสู่ระบบเท่านั้น', 'danger')
        return redirect(url_for('auth.login'))
        
    user = User.query.filter_by(email=email).first()
    
    if not user:
        username = email.split('@')[0]
        suffix = 1
        original_username = username
        while User.query.filter_by(username=username).first():
            username = f"{original_username}{suffix}"
            suffix += 1
            
        user = User(username=username, email=email, full_name=full_name, role='user')
        import secrets
        user.set_password(secrets.token_urlsafe(16))
        db.session.add(user)
        db.session.commit()
        flash('สร้างบัญชีผู้ใช้ใหม่ด้วย Google สำเร็จ!', 'success')
    
    login_user(user)
    flash(f'ยินดีต้อนรับ {user.full_name}!', 'success')
    
    if user.is_admin():
        return redirect(url_for('admin.dashboard'))
    return redirect(url_for('user.dashboard'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('user.dashboard'))
    
    if request.method == 'POST':
        account_type = request.form.get('account_type', 'student')
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        errors = []
        if account_type == 'student':
            student_id = request.form.get('student_id', '').strip()
            if not student_id:
                errors.append('กรุณากรอกรหัสนักศึกษา')
            username = student_id
            full_name = f"นักศึกษา ({student_id})"
        else:
            teacher_name = request.form.get('teacher_name', '').strip()
            teacher_username = request.form.get('teacher_username', '').strip()
            if not teacher_name or not teacher_username:
                errors.append('กรุณากรอกชื่อ-นามสกุลและชื่อผู้ใช้งานของอาจารย์')
            username = teacher_username
            full_name = teacher_name
        
        if not email or not password:
            errors.append('กรุณากรอกอีเมลและรหัสผ่านให้ครบถ้วน')
        if not email.endswith('.ac.th'):
            errors.append('กรุณาใช้อีเมลของสถาบัน (.ac.th) เท่านั้น')
        if len(password) < 8:
            errors.append('รหัสผ่านต้องมีอย่างน้อย 8 ตัวอักษร')
        if password != confirm_password:
            errors.append('รหัสผ่านและยืนยันรหัสผ่านไม่ตรงกัน')
        if User.query.filter_by(email=email).first():
            errors.append('อีเมลนี้ถูกใช้งานในระบบแล้ว')
        if User.query.filter_by(username=username).first():
            errors.append(f'ชื่อผู้ใช้ / รหัสนักศึกษา "{username}" มีอยู่ในระบบแล้ว')
        
        if errors:
            for error in errors:
                flash(error, 'danger')
            return redirect(url_for('auth.register'))
        
        new_user = User(username=username, email=email, full_name=full_name, role='user')
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        if account_type == 'student':
            flash(f'สมัครสมาชิกสำเร็จด้วยรหัสนักศึกษา {username}! กรุณาเข้าสู่ระบบและไปตั้งชื่อ-นามสกุลจริงที่หน้าโปรไฟล์', 'success')
        else:
            flash(f'สมัครสมาชิกสำเร็จ! ยินดีต้อนรับ {full_name}', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('ออกจากระบบเรียบร้อยแล้ว', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        action_type = request.form.get('action_type', 'find_user')
        email = request.form.get('email', '').strip()
        
        if not email:
            flash('กรุณาระบุอีเมลสถาบัน', 'warning')
            return redirect(url_for('auth.forgot_password'))
            
        user = User.query.filter_by(email=email).first()
        
        if not user:
            flash(f'ไม่พบบัญชีผู้ใช้ที่ผูกกับอีเมล "{email}" ในระบบ', 'danger')
            return redirect(url_for('auth.forgot_password'))
            
        if action_type == 'find_user':
            flash(f'🔍 พบบัญชีของคุณ! ชื่อผู้ใช้ (Username/รหัสนักศึกษา) คือ: "{user.username}" (ชื่อบัญชี: {user.full_name})', 'success')
            return redirect(url_for('auth.login'))
            
        elif action_type == 'reset_password':
            new_password = request.form.get('new_password', '')
            confirm_new_password = request.form.get('confirm_new_password', '')
            
            if len(new_password) < 8:
                flash('รหัสผ่านใหม่ต้องมีอย่างน้อย 8 ตัวอักษร', 'danger')
                return redirect(url_for('auth.forgot_password'))
                
            if new_password != confirm_new_password:
                flash('รหัสผ่านใหม่และยืนยันรหัสผ่านไม่ตรงกัน', 'danger')
                return redirect(url_for('auth.forgot_password'))
                
            user.set_password(new_password)
            db.session.commit()
            flash('🎉 ตั้งรหัสผ่านใหม่สำเร็จเรียบร้อยแล้ว! กรุณาเข้าสู่ระบบด้วยรหัสผ่านใหม่', 'success')
            return redirect(url_for('auth.login'))
            
    return render_template('forgot_password.html')
