import os
from datetime import datetime
from flask import render_template, redirect, url_for, flash, request, current_app
from werkzeug.utils import secure_filename
from models import db, Equipment, BorrowRequest, Building, Room
from utils import allowed_file, admin_required, log_audit
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
        room_obj = None
        if room_id and room_id.isdigit():
            room_id = int(room_id)
            room_obj = Room.query.get(room_id)
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
        
        # บันทึก Audit Log
        room_desc = f"ห้อง {room_obj.name}" if room_obj else "ไม่ได้ระบุห้อง"
        log_audit(
            action='ADD_EQUIPMENT',
            category='equipment',
            target_type='ครุภัณฑ์/อุปกรณ์',
            target_name=f"{name} ({equipment_code})",
            details=f"เพิ่มครุภัณฑ์ใหม่ จำนวน {qty} ชิ้น, ติดตั้งที่ {room_desc}, {'เปิดให้ยืม' if is_borrowable else 'ปิดการยืม'}",
            target_id=new_eq.id
        )
        
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
        changes = []
        new_name = request.form.get('name', eq.name).strip()
        if new_name != eq.name:
            changes.append(f"ชื่อ: '{eq.name}' -> '{new_name}'")
            eq.name = new_name
            
        new_desc = request.form.get('description', eq.description).strip()
        if new_desc != (eq.description or ''):
            changes.append("แก้ไขรายละเอียดคำอธิบาย")
            eq.description = new_desc
        
        is_borrowable_val = request.form.get('is_borrowable')
        new_is_borrowable = True if is_borrowable_val == 'yes' else False
        if new_is_borrowable != eq.is_borrowable:
            changes.append(f"สถานะการยืม: '{'เปิดให้ยืม' if eq.is_borrowable else 'ปิดการยืม'}' -> '{'เปิดให้ยืม' if new_is_borrowable else 'ปิดการยืม'}'")
            eq.is_borrowable = new_is_borrowable
        
        room_id = request.form.get('room_id')
        new_room_id = int(room_id) if room_id and room_id.isdigit() else None
        if new_room_id != eq.room_id:
            old_r = eq.room.name if eq.room else 'ไม่ได้ระบุห้อง'
            new_r = Room.query.get(new_room_id).name if new_room_id else 'ไม่ได้ระบุห้อง'
            changes.append(f"สถานที่จัดวาง: '{old_r}' -> '{new_r}'")
            eq.room_id = new_room_id
        
        try:
            new_total = max(1, int(request.form.get('total_quantity', eq.total_quantity)))
            if new_total != eq.total_quantity:
                diff = new_total - eq.total_quantity
                changes.append(f"จำนวนทั้งหมด: {eq.total_quantity} -> {new_total} ชิ้น")
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
                changes.append("อัปโหลดรูปภาพใหม่")
        
        db.session.commit()
        
        # บันทึก Audit Log
        detail_text = ", ".join(changes) if changes else "บันทึกข้อมูลโดยไม่มีการเปลี่ยนแปลงค่าสำคัญ"
        log_audit(
            action='EDIT_EQUIPMENT',
            category='equipment',
            target_type='ครุภัณฑ์/อุปกรณ์',
            target_name=f"{eq.name} ({eq.equipment_code})",
            details=detail_text,
            target_id=eq.id
        )
        
        flash(f'อัปเดตข้อมูล "{eq.name}" เรียบร้อยแล้ว', 'success')
        return redirect(url_for('admin.dashboard'))
    
    buildings = Building.query.all()
    return render_template('edit_equipment.html', equipment=eq, buildings=buildings)

@admin_bp.route('/delete-equipment/<int:eq_id>', methods=['POST'])
@admin_required
def delete_equipment(eq_id):
    """ลบอุปกรณ์ออกจากระบบ"""
    eq = Equipment.query.get_or_404(eq_id)
    eq_name = eq.name
    eq_code = eq.equipment_code
    eq_qty = eq.total_quantity
    
    if eq.image_filename:
        img_path = os.path.join(current_app.config['UPLOAD_FOLDER'], eq.image_filename)
        if os.path.exists(img_path):
            os.remove(img_path)
    
    BorrowRequest.query.filter_by(equipment_id=eq_id).delete()
    db.session.delete(eq)
    db.session.commit()
    
    # บันทึก Audit Log
    log_audit(
        action='DELETE_EQUIPMENT',
        category='equipment',
        target_type='ครุภัณฑ์/อุปกรณ์',
        target_name=f"{eq_name} ({eq_code})",
        details=f"ลบครุภัณฑ์ออกจากระบบอย่างถาวร (ยอดคงคลังก่อนลบ: {eq_qty} ชิ้น)",
        target_id=eq_id
    )
    
    flash(f'ลบอุปกรณ์ "{eq_name}" เรียบร้อยแล้ว', 'info')
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/dispose-equipment/<int:eq_id>', methods=['POST'])
@admin_required
def dispose_equipment(eq_id):
    """ตัดจำหน่าย / ปรับลดยอดครุภัณฑ์หรือวัสดุออกบางส่วน"""
    eq = Equipment.query.get_or_404(eq_id)
    
    try:
        dispose_qty = int(request.form.get('dispose_quantity', '0'))
    except ValueError:
        flash('กรุณาระบุจำนวนที่ถูกต้องสำหรับการตัดจำหน่าย', 'danger')
        return redirect(request.referrer or url_for('admin.dashboard'))
    
    reason = request.form.get('reason', 'เสื่อมสภาพตามอายุการใช้งาน').strip()
    note = request.form.get('note', '').strip()
    
    if dispose_qty <= 0:
        flash('จำนวนที่ตัดจำหน่ายต้องมากกว่า 0', 'warning')
        return redirect(request.referrer or url_for('admin.dashboard'))
    
    if dispose_qty > eq.available_quantity:
        flash(f'ไม่สามารถตัดจำหน่าย {dispose_qty} ชิ้นได้ เนื่องจากมีของว่างในคลังเพียง {eq.available_quantity} ชิ้น (อาจมีรายการถูกยืมใช้งานอยู่)', 'danger')
        return redirect(request.referrer or url_for('admin.dashboard'))
    
    old_total = eq.total_quantity
    
    # หักลดยอดจำนวนทั้งหมดและจำนวนที่ว่างอยู่
    eq.total_quantity -= dispose_qty
    eq.available_quantity -= dispose_qty
    
    # หากจำนวนทั้งหมดเหลือ 0 ให้ปรับสถานะ
    if eq.total_quantity <= 0:
        eq.total_quantity = 0
        eq.available_quantity = 0
        eq.status = 'disposed'
        eq.is_borrowable = False
    
    # บันทึกรายละเอียดลง description หรือ log เพื่อเก็บประวัติ
    timestamp_str = datetime.now().strftime('%d/%m/%Y %H:%M')
    log_entry = f"\n[ตัดจำหน่าย {dispose_qty} ชิ้น เมื่อ {timestamp_str} | สาเหตุ: {reason}"
    if note:
        log_entry += f" | หมายเหตุ: {note}"
    log_entry += "]"
    
    eq.description = (eq.description or '') + log_entry
    db.session.commit()
    
    # บันทึก Audit Log
    detail_str = f"ตัดจำหน่าย {dispose_qty} ชิ้น (ยอดคงเหลือ {eq.total_quantity}/{old_total}) | สาเหตุ: {reason}"
    if note:
        detail_str += f" | หมายเหตุ: {note}"
        
    log_audit(
        action='DISPOSE_EQUIPMENT',
        category='equipment',
        target_type='ครุภัณฑ์/อุปกรณ์',
        target_name=f"{eq.name} ({eq.equipment_code})",
        details=detail_str,
        target_id=eq.id
    )
    
    flash(f'ตัดจำหน่าย "{eq.name}" จำนวน {dispose_qty} ชิ้น เรียบร้อยแล้ว (คงเหลือ {eq.total_quantity} ชิ้น)', 'success')
    return redirect(request.referrer or url_for('admin.dashboard'))
