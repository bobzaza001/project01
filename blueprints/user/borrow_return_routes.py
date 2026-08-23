from datetime import datetime, timedelta
from flask import redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Equipment, BorrowRequest, RepairRequest, get_local_now
from . import user_bp

@user_bp.route('/request_borrow/<int:eq_id>', methods=['POST'])
@login_required
def request_borrow(eq_id):
    """ยื่นคำขอยืมครุภัณฑ์ (durable) — ผู้ใช้ระบุวัน/เวลายืม + จำนวนวันยืม"""
    if current_user.is_student():
        flash('นักเรียนไม่มีสิทธิ์ในการยืมครุภัณฑ์', 'danger')
        return redirect(url_for('user.equipment_list'))
    equipment = Equipment.query.get_or_404(eq_id)
    
    # ตรวจสอบว่าอุปกรณ์เปิดให้ยืมหรือไม่
    if not equipment.is_borrowable:
        flash('อุปกรณ์นี้ไม่เปิดให้ยืม', 'warning')
        return redirect(url_for('user.equipment_list'))
    
    # ตรวจสอบสถานะอุปกรณ์
    if equipment.status not in ('available', 'borrowed'):
        flash('อุปกรณ์นี้ไม่พร้อมให้ยืมในขณะนี้ (อยู่ระหว่างซ่อมบำรุง)', 'warning')
        return redirect(url_for('user.equipment_list'))
    
    # ตรวจสอบคำขอซ้ำ
    existing = BorrowRequest.query.filter_by(
        user_id=current_user.id,
        equipment_id=eq_id,
        status='pending'
    ).first()
    if existing:
        flash('คุณมีคำขอยืมอุปกรณ์ชิ้นนี้ที่รอการอนุมัติอยู่แล้ว', 'warning')
        return redirect(url_for('user.equipment_list'))
    
    borrow_datetime_str = request.form.get('borrow_datetime')
    borrow_days = request.form.get('borrow_days', 3, type=int)
    
    if not borrow_datetime_str:
        flash('กรุณาระบุวันและเวลาที่ต้องการยืม', 'warning')
        return redirect(url_for('user.equipment_list'))
    
    # จำกัดจำนวนวันยืม 1-30 วัน
    borrow_days = max(1, min(30, borrow_days))
        
    try:
        borrow_dt = datetime.strptime(borrow_datetime_str, '%Y-%m-%dT%H:%M')
    except ValueError:
        borrow_dt = get_local_now()
    
    if equipment.available_quantity <= 0:
        flash('ครุภัณฑ์ชิ้นนี้ไม่ว่างในขณะนี้', 'warning')
        return redirect(url_for('user.equipment_list'))
    
    new_request = BorrowRequest(
        user_id=current_user.id,
        equipment_id=eq_id,
        borrow_datetime=borrow_dt,
        borrow_days=borrow_days,
        status='pending'
    )
    db.session.add(new_request)
    db.session.commit()
    
    flash(f'ยื่นคำขอยืม "{equipment.name}" ({borrow_days} วัน) เรียบร้อยแล้ว รอการอนุมัติ', 'success')
    return redirect(url_for('user.dashboard'))


@user_bp.route('/request_consumable/<int:eq_id>', methods=['POST'])
@login_required
def request_consumable(eq_id):
    """ยื่นคำขอเบิกวัสดุสิ้นเปลือง (consumable) — ระบุจำนวน, ไม่ต้องคืน"""
    if current_user.is_student():
        flash('นักเรียนไม่มีสิทธิ์ในการเบิกวัสดุสิ้นเปลือง', 'danger')
        return redirect(url_for('user.equipment_list'))
    equipment = Equipment.query.get_or_404(eq_id)
    qty = request.form.get('quantity', 1, type=int)
    
    if not equipment.is_consumable():
        flash('อุปกรณ์นี้ไม่ใช่วัสดุสิ้นเปลือง', 'danger')
        return redirect(url_for('user.equipment_list'))
    
    # ตรวจสอบว่าอุปกรณ์เปิดให้เบิกหรือไม่
    if not equipment.is_borrowable:
        flash('วัสดุนี้ไม่เปิดให้เบิก', 'warning')
        return redirect(url_for('user.equipment_list'))
    
    # ตรวจสอบคำขอซ้ำ
    existing = BorrowRequest.query.filter_by(
        user_id=current_user.id,
        equipment_id=eq_id,
        status='pending'
    ).first()
    if existing:
        flash('คุณมีคำขอเบิกวัสดุนี้ที่รอการอนุมัติอยู่แล้ว', 'warning')
        return redirect(url_for('user.equipment_list'))
    
    qty = max(1, min(qty, equipment.available_quantity))
    
    if equipment.available_quantity <= 0:
        flash('วัสดุนี้หมดคลังแล้ว', 'warning')
        return redirect(url_for('user.equipment_list'))
    
    new_request = BorrowRequest(
        user_id=current_user.id,
        equipment_id=eq_id,
        borrow_datetime=get_local_now(),
        quantity=qty,
        status='pending'
    )
    db.session.add(new_request)
    db.session.commit()
    
    flash(f'ยื่นคำขอเบิก "{equipment.name}" จำนวน {qty} เรียบร้อยแล้ว รอการอนุมัติ', 'success')
    return redirect(url_for('user.dashboard'))


@user_bp.route('/return_equipment/<int:req_id>', methods=['GET', 'POST'])
@login_required
def return_equipment(req_id):
    """แจ้งส่งคืนครุภัณฑ์ — ระบุสภาพ (ปกติ/เสียหาย) + หมายเหตุ"""
    if current_user.is_student():
        flash('คุณไม่มีสิทธิ์ดำเนินการคืนครุภัณฑ์', 'danger')
        return redirect(url_for('user.dashboard'))
    borrow_req = BorrowRequest.query.get_or_404(req_id)
    
    if borrow_req.user_id != current_user.id and not current_user.is_admin():
        flash('คุณไม่มีสิทธิ์คืนครุภัณฑ์ของผู้อื่น', 'danger')
        return redirect(url_for('user.dashboard'))
        
    if borrow_req.status != 'approved':
        flash('ไม่สามารถคืนครุภัณฑ์ได้', 'warning')
        return redirect(url_for('user.dashboard'))
    
    if request.method == 'POST':
        damage_status = request.form.get('damage_status', 'normal')
        damage_note = request.form.get('damage_note', '').strip()
        
        # จัดการอัปโหลดรูปภาพตอนส่งคืน
        import os, time
        from werkzeug.utils import secure_filename
        from utils import allowed_file
        from flask import current_app
        
        file = request.files.get('return_image')
        if file and file.filename != '' and allowed_file(file.filename):
            import base64
            file_bytes = file.read()
            if file_bytes:
                ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else 'jpg'
                mime = 'image/jpeg' if ext in ('jpg', 'jpeg') else f'image/{ext}'
                try:
                    from PIL import Image
                    import io
                    img = Image.open(io.BytesIO(file_bytes))
                    img.thumbnail((600, 600))
                    if img.mode in ("RGBA", "P") and ext in ('jpg', 'jpeg'):
                        img = img.convert("RGB")
                    buf = io.BytesIO()
                    img.save(buf, format="JPEG" if ext in ('jpg', 'jpeg') else "PNG", quality=85)
                    b64_str = base64.b64encode(buf.getvalue()).decode('utf-8')
                    borrow_req.return_image_filename = f"data:{mime};base64,{b64_str}"
                except Exception:
                    b64_str = base64.b64encode(file_bytes).decode('utf-8')
                    borrow_req.return_image_filename = f"data:{mime};base64,{b64_str}"
            
        borrow_req.status = 'return_pending'
        borrow_req.damage_status = damage_status
        borrow_req.damage_note = damage_note
        
        db.session.commit()
        
        status_text = '⚠️ ชำรุด' if damage_status == 'damaged' else '✅ ปกติ'
        flash(f'แจ้งส่งคืน "{borrow_req.equipment.name}" (สภาพ: {status_text}) แล้ว รอแอดมินตรวจสอบ', 'info')
        
        if current_user.is_admin():
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('user.dashboard'))
    
    # GET — ถ้าไม่ได้มาจากฟอร์ม ให้ redirect กลับ
    return redirect(url_for('user.dashboard'))

@user_bp.route('/report_repair/<int:eq_id>', methods=['POST'])
@login_required
def report_repair(eq_id):
    """แจ้งซ่อมครุภัณฑ์ (Durable) จากหน้าคลังอุปกรณ์"""
    equipment = Equipment.query.get_or_404(eq_id)
    
    if not equipment.is_durable():
        flash('สามารถแจ้งซ่อมได้เฉพาะครุภัณฑ์ยืม-คืนเท่านั้น', 'danger')
        return redirect(url_for('user.equipment_list'))
        
    issue_desc = request.form.get('issue_description', '').strip()
    if not issue_desc:
        flash('กรุณาระบุรายละเอียดปัญหาหรืออาการชำรุด', 'warning')
        return redirect(url_for('user.equipment_list'))
        
    new_repair = RepairRequest(
        equipment_id=equipment.id,
        user_id=current_user.id,
        issue_description=issue_desc,
        status='pending'
    )
    
    # เปลี่ยนสถานะอุปกรณ์เป็น maintenance เพื่อไม่ให้คนอื่นยืมต่อได้
    equipment.status = 'maintenance'
    
    db.session.add(new_repair)
    db.session.commit()
    
    flash(f'ส่งเรื่องแจ้งซ่อม "{equipment.name}" เรียบร้อยแล้ว', 'success')
    return redirect(url_for('user.dashboard'))


@user_bp.route('/delete-history/<int:req_id>', methods=['POST'])
@login_required
def delete_history(req_id):
    """ผู้ใช้ลบประวัติการยืมของตนเองออกจาก Dashboard (เฉพาะรายการที่สิ้นสุดแล้ว เช่น คืนแล้ว หรือ ปฏิเสธ)"""
    borrow_req = BorrowRequest.query.get_or_404(req_id)
    
    if borrow_req.user_id != current_user.id and not current_user.is_admin():
        flash('คุณไม่มีสิทธิ์ลบประวัติของผู้อื่น', 'danger')
        return redirect(url_for('user.dashboard'))
        
    if borrow_req.status not in ('returned', 'rejected'):
        flash('สามารถลบได้เฉพาะรายการที่คืนแล้วหรือถูกปฏิเสธเท่านั้น', 'warning')
        return redirect(url_for('user.dashboard'))
        
    borrow_req.hidden_by_user = True
    db.session.commit()
    flash('ลบรายการประวัติออกจากแดชบอร์ดของคุณเรียบร้อยแล้ว', 'success')
    return redirect(url_for('user.dashboard'))

