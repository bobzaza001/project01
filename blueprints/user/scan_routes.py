from flask import jsonify, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Equipment, BorrowRequest
from . import user_bp

def extract_equipment_code(raw_input):
    if not raw_input:
        return ""
    raw_input = raw_input.strip()
    # If it is a full URL like https://domain.com/user/scan/EQ-123 or https://domain.com/scan/EQ-123
    if "/" in raw_input:
        raw_input = raw_input.rstrip("/").split("/")[-1]
    return raw_input.strip()


@user_bp.route('/api/scan-lookup')
@login_required
def scan_lookup():
    """API ตรวจสอบรหัส QR/Barcode จากกล้องสแกน เพื่อระบุข้อมูลอุปกรณ์และ Action (ยืม/คืน) ทันที"""
    raw_code = request.args.get('code', '').strip()
    code = extract_equipment_code(raw_code)
    
    if not code:
        return jsonify({'success': False, 'message': 'กรุณาระบุรหัสครุภัณฑ์หรือสแกนใหม่อีกครั้ง'}), 400
        
    # ค้นหาอุปกรณ์จาก equipment_code หรือ id
    eq = Equipment.query.filter(
        (Equipment.equipment_code.ilike(code)) |
        (Equipment.id == int(code) if code.isdigit() else False)
    ).first()
    
    if not eq:
        return jsonify({'success': False, 'message': f'ไม่พบอุปกรณ์รหัส "{code}" ในระบบคลัง'}), 404
        
    # ตรวจสอบว่าผู้ใช้กำลังยืมอุปกรณ์นี้อยู่หรือไม่
    active_borrow = BorrowRequest.query.filter_by(
        user_id=current_user.id,
        equipment_id=eq.id,
        status='approved'
    ).first()
    
    loc = "-"
    if eq.room_ref:
        room = eq.room_ref
        floor_name = room.floor.name if room.floor else ""
        bldg_name = room.floor.building.name if room.floor and room.floor.building else ""
        loc = f"{bldg_name} {floor_name} ({room.name})".strip()
        
    action = 'unavailable'
    action_message = ''
    
    if active_borrow:
        action = 'return'
        action_message = 'คุณกำลังยืมอุปกรณ์ชิ้นนี้อยู่ — กดปุ่มด้านล่างเพื่อแจ้งส่งคืนพร้อมแนบรูปถ่าย'
    elif eq.status != 'available' and eq.available_quantity <= 0:
        action = 'unavailable'
        action_message = 'อุปกรณ์นี้ไม่พร้อมให้ยืมในขณะนี้ (ของหมดคลัง หรืออยู่ระหว่างซ่อมบำรุง)'
    elif not eq.is_borrowable:
        action = 'unavailable'
        action_message = 'อุปกรณ์นี้ถูกกำหนดให้ใช้งานประจำห้องเท่านั้น (ไม่อนุญาตให้ยืมพกพา)'
    elif eq.item_type == 'consumable':
        action = 'consumable'
        action_message = 'วัสดุสิ้นเปลืองพร้อมให้ขอเบิก'
    else:
        action = 'borrow'
        action_message = 'ครุภัณฑ์พร้อมให้ยืมใช้งาน'
        
    return jsonify({
        'success': True,
        'equipment': {
            'id': eq.id,
            'code': eq.equipment_code,
            'name': eq.name,
            'category': eq.category or 'ทั่วไป',
            'item_type': eq.item_type,
            'available_quantity': eq.available_quantity,
            'total_quantity': eq.total_quantity,
            'status': eq.status,
            'is_borrowable': eq.is_borrowable,
            'image_filename': eq.image_filename,
            'location': loc
        },
        'action': action,
        'action_message': action_message,
        'active_borrow_id': active_borrow.id if active_borrow else None
    })


@user_bp.route('/scan/<path:eq_code>')
@login_required
def direct_scan(eq_code):
    """Direct URL เมื่อผู้ใช้ใช้กล้องมือถือทั่วไปสแกนสติ๊กเกอร์ QR Code แล้วเปิดเว็บโดยตรง"""
    code = extract_equipment_code(eq_code)
    eq = Equipment.query.filter(
        (Equipment.equipment_code.ilike(code)) |
        (Equipment.id == int(code) if code.isdigit() else False)
    ).first()
    
    if not eq:
        flash(f'ไม่พบข้อมูลครุภัณฑ์รหัส "{code}" ในระบบ', 'danger')
        return redirect(url_for('user.equipment_list'))
        
    # ตรวจสอบว่ากำลังยืมอยู่หรือไม่
    active_borrow = BorrowRequest.query.filter_by(
        user_id=current_user.id,
        equipment_id=eq.id,
        status='approved'
    ).first()
    
    if active_borrow:
        flash(f'พบรายการยืม "{eq.name}" — กรุณาแจ้งส่งคืน', 'info')
        return redirect(url_for('user.dashboard', action='return', req_id=active_borrow.id, eq_name=eq.name))
    else:
        flash(f'พบครุภัณฑ์ "{eq.name}" ({eq.equipment_code})', 'success')
        return redirect(url_for('user.equipment_list', action='borrow', eq_id=eq.id, eq_name=eq.name, item_type=eq.item_type, is_consumable='1' if eq.item_type == 'consumable' else '0'))
