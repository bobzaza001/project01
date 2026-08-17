from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from models import Equipment, BorrowRequest, RepairRequest, Building
from . import user_bp

@user_bp.route('/dashboard')
@login_required
def dashboard():
    # If it's an admin, redirect them to the admin dashboard instead of showing the user one
    if current_user.is_admin():
        return redirect(url_for('admin.dashboard'))
        
    my_requests = BorrowRequest.query.filter_by(user_id=current_user.id) \
        .order_by(BorrowRequest.requested_at.desc()).all()
    my_repair_requests = RepairRequest.query.filter_by(user_id=current_user.id) \
        .order_by(RepairRequest.reported_at.desc()).all()
    available_equipment = Equipment.query.filter(Equipment.available_quantity > 0).all()
    
    return render_template('dashboard_user.html',
                           my_requests=my_requests,
                           my_repair_requests=my_repair_requests,
                           available_equipment=available_equipment)

@user_bp.route('/equipment')
@login_required
def equipment_list():
    """หน้าแสดงคลังอุปกรณ์ทั้งหมด แบบการ์ดพร้อมรูปภาพ"""
    all_equipment = Equipment.query.all()
    buildings = Building.query.all()
    return render_template('equipment_list.html', equipment=all_equipment, buildings=buildings)

@user_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    import os, time
    from flask import request, flash, current_app
    from werkzeug.utils import secure_filename
    from models import db, User
    from utils import allowed_file

    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip()
        
        old_password = request.form.get('old_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        if email and email != current_user.email:
            if User.query.filter_by(email=email).first():
                flash('อีเมลนี้ถูกใช้งานโดยผู้ใช้อื่นแล้ว', 'danger')
                return redirect(url_for('user.profile'))
            if not email.endswith('.ac.th'):
                flash('กรุณาใช้อีเมลของสถาบัน (.ac.th) เท่านั้น', 'danger')
                return redirect(url_for('user.profile'))
            current_user.email = email
            
        if full_name:
            current_user.full_name = full_name
            
        if new_password:
            if not current_user.check_password(old_password):
                flash('รหัสผ่านเดิมไม่ถูกต้อง', 'danger')
                return redirect(url_for('user.profile'))
            if len(new_password) < 8:
                flash('รหัสผ่านใหม่ต้องมีอย่างน้อย 8 ตัวอักษร', 'danger')
                return redirect(url_for('user.profile'))
            if new_password != confirm_password:
                flash('รหัสผ่านใหม่และยืนยันรหัสผ่านไม่ตรงกัน', 'danger')
                return redirect(url_for('user.profile'))
            current_user.set_password(new_password)
            flash('เปลี่ยนรหัสผ่านสำเร็จแล้ว', 'info')

        file = request.files.get('profile_image')
        if file and file.filename != '' and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            _, ext = os.path.splitext(filename)
            new_filename = f"profile_{current_user.id}_{int(time.time())}{ext}"
            uploads_dir = os.path.join(current_app.static_folder, 'uploads')
            os.makedirs(uploads_dir, exist_ok=True)
            upload_path = os.path.join(uploads_dir, new_filename)
            file.save(upload_path)
            current_user.profile_image = new_filename

        db.session.commit()
        flash('อัปเดตข้อมูลส่วนตัวเรียบร้อยแล้ว!', 'success')
        return redirect(url_for('user.profile'))

    total_borrowed = BorrowRequest.query.filter_by(user_id=current_user.id).count()
    active_borrows = BorrowRequest.query.filter_by(user_id=current_user.id, status='approved').count()

    return render_template('profile.html', total_borrowed=total_borrowed, active_borrows=active_borrows)

@user_bp.route('/contact')
@login_required
def contact():
    """หน้าติดต่อด่วนสำหรับนักเรียนและอาจารย์"""
    return render_template('contact.html')
