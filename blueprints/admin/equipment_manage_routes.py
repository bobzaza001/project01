import os
from datetime import datetime
from flask import render_template, redirect, url_for, flash, request, current_app
from werkzeug.utils import secure_filename
from models import db, Equipment, BorrowRequest, Building
from utils import allowed_file, admin_required
from . import admin_bp

@admin_bp.route('/add-equipment', methods=['GET', 'POST'])
@admin_required
def add_equipment():
    """หน้าเพิ่มอุปกรณ์ใหม่ พร้อมอัปโหลดรูปภาพ"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        equipment_code = request.form.get('equipment_code', '').strip()
        description = request.form.get('description', '').strip()
        total_quantity = request.form.get('total_quantity', '1')
        
        if not name or not equipment_code:
            flash('กรุณากรอกชื่อและรหัสอุปกรณ์', 'danger')
            return redirect(url_for('admin.add_equipment'))
        
        if Equipment.query.filter_by(equipment_code=equipment_code).first():
            flash('รหัสอุปกรณ์นี้มีอยู่ในระบบแล้ว', 'danger')
            return redirect(url_for('admin.add_equipment'))
        
        image_filename = ''
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                ext = file.filename.rsplit('.', 1)[1].lower()
                safe_name = secure_filename(f"{equipment_code}_{int(datetime.utcnow().timestamp())}.{ext}")
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], safe_name))
                image_filename = safe_name
        
        try:
            qty = max(1, int(total_quantity))
        except ValueError:
            qty = 1
        is_borrowable_val = request.form.get('is_borrowable')
        is_borrowable = True if is_borrowable_val == 'yes' else False
        
        room_id = request.form.get('room_id')
        if room_id and room_id.isdigit():
            room_id = int(room_id)
        else:
            room_id = None
        
        new_eq = Equipment(
            name=name,
            equipment_code=equipment_code,
            description=description,
            image_filename=image_filename,
            total_quantity=qty,
            available_quantity=qty,
            status='available',
            is_borrowable=is_borrowable,
            room_id=room_id
        )
        db.session.add(new_eq)
        db.session.commit()
        
        flash(f'เพิ่มอุปกรณ์ "{name}" เรียบร้อยแล้ว', 'success')
        return redirect(url_for('admin.dashboard'))
    
    buildings = Building.query.all()
    return render_template('add_equipment.html', buildings=buildings)

@admin_bp.route('/edit-equipment/<int:eq_id>', methods=['GET', 'POST'])
@admin_required
def edit_equipment(eq_id):
    """หน้าแก้ไขข้อมูลอุปกรณ์"""
    eq = Equipment.query.get_or_404(eq_id)
    
    if request.method == 'POST':
        eq.name = request.form.get('name', eq.name).strip()
        eq.description = request.form.get('description', eq.description).strip()
        
        is_borrowable_val = request.form.get('is_borrowable')
        eq.is_borrowable = True if is_borrowable_val == 'yes' else False
        
        room_id = request.form.get('room_id')
        if room_id and room_id.isdigit():
            eq.room_id = int(room_id)
        else:
            eq.room_id = None
        
        try:
            new_total = max(1, int(request.form.get('total_quantity', eq.total_quantity)))
            diff = new_total - eq.total_quantity
            eq.total_quantity = new_total
            eq.available_quantity = max(0, eq.available_quantity + diff)
        except ValueError:
            pass
        
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                if eq.image_filename:
                    old_path = os.path.join(current_app.config['UPLOAD_FOLDER'], eq.image_filename)
                    if os.path.exists(old_path):
                        os.remove(old_path)
                
                ext = file.filename.rsplit('.', 1)[1].lower()
                safe_name = secure_filename(f"{eq.equipment_code}_{int(datetime.utcnow().timestamp())}.{ext}")
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], safe_name))
                eq.image_filename = safe_name
        
        db.session.commit()
        flash(f'อัปเดตข้อมูล "{eq.name}" เรียบร้อยแล้ว', 'success')
        return redirect(url_for('admin.dashboard'))
    
    buildings = Building.query.all()
    return render_template('edit_equipment.html', equipment=eq, buildings=buildings)

@admin_bp.route('/delete-equipment/<int:eq_id>', methods=['POST'])
@admin_required
def delete_equipment(eq_id):
    """ลบอุปกรณ์ออกจากระบบ"""
    eq = Equipment.query.get_or_404(eq_id)
    
    if eq.image_filename:
        img_path = os.path.join(current_app.config['UPLOAD_FOLDER'], eq.image_filename)
        if os.path.exists(img_path):
            os.remove(img_path)
    
    BorrowRequest.query.filter_by(equipment_id=eq_id).delete()
    db.session.delete(eq)
    db.session.commit()
    flash(f'ลบอุปกรณ์ "{eq.name}" เรียบร้อยแล้ว', 'info')
    return redirect(url_for('admin.dashboard'))
