from datetime import datetime, timedelta
from flask import render_template, redirect, url_for, flash, request, current_app
from models import db, User, Equipment, BorrowRequest, RepairRequest, get_local_now
from utils import admin_required
from notifications import notify_user_approved, notify_user_rejected
from . import admin_bp

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    all_requests = BorrowRequest.query.order_by(BorrowRequest.requested_at.desc()).all()
    all_equipment = Equipment.query.all()
    repair_requests = RepairRequest.query.order_by(RepairRequest.reported_at.desc()).all()
    
    # นับรายการที่เกินกำหนด
    overdue_count = 0
    for req in all_requests:
        if req.is_overdue():
            overdue_count += 1
    
    stats = {
        'total_equipment': Equipment.query.count(),
        'available': Equipment.query.filter(Equipment.available_quantity > 0).count(),
        'borrowed': Equipment.query.filter(Equipment.available_quantity == 0).count(),
        'pending_requests': BorrowRequest.query.filter_by(status='pending').count(),
        'total_users': User.query.filter_by(role='user').count(),
        'overdue_count': overdue_count,
    }
    return render_template('dashboard_admin.html',
                           requests=all_requests,
                           equipment=all_equipment,
                           repair_requests=repair_requests,
                           stats=stats)

@admin_bp.route('/approve_borrow/<int:req_id>', methods=['POST'])
@admin_required
def approve_borrow(req_id):
    borrow_req = BorrowRequest.query.get_or_404(req_id)
    
    if borrow_req.status != 'pending':
        flash('คำขอนี้ได้รับการดำเนินการแล้ว', 'warning')
        return redirect(url_for('admin.dashboard'))
    
    eq = borrow_req.equipment
    
    if eq.is_consumable():
        # === วัสดุสิ้นเปลือง: หักสต็อกทันที, ไม่ต้องคืน ===
        qty = borrow_req.quantity
        if eq.available_quantity < qty:
            flash(f'วัสดุเหลือไม่พอ (เหลือ {eq.available_quantity}, ขอเบิก {qty})', 'danger')
            return redirect(url_for('admin.dashboard'))
        
        borrow_req.status = 'returned'  # เสร็จทันที ไม่ต้องคืน
        borrow_req.approved_at = get_local_now()
        borrow_req.returned_at = get_local_now()
        
        eq.available_quantity -= qty
        eq.total_quantity -= qty  # วัสดุสิ้นเปลือง: ลดจำนวนรวมด้วย
        if eq.available_quantity <= 0:
            eq.status = 'unavailable'
        
        db.session.commit()
        flash(f'อนุมัติเบิกวัสดุ "{eq.name}" จำนวน {qty} โดย {borrow_req.requester.full_name} (หักสต็อกแล้ว)', 'success')
        
        # 📧 ส่งอีเมลแจ้งผู้ยืม
        try:
            notify_user_approved(borrow_req)
        except Exception as e:
            current_app.logger.error(f'ส่งอีเมลแจ้งเตือนล้มเหลว: {e}')
    else:
        # === ครุภัณฑ์: ยืมแล้วต้องคืน ===
        if eq.available_quantity <= 0:
            flash('อุปกรณ์หมด ไม่สามารถอนุมัติได้', 'danger')
            return redirect(url_for('admin.dashboard'))
        
        borrow_req.status = 'approved'
        borrow_req.approved_at = get_local_now()
        
        # คำนวณวันกำหนดคืนจาก borrow_days ที่ผู้ใช้ระบุ
        days = borrow_req.borrow_days or 3
        borrow_req.return_due_datetime = borrow_req.borrow_datetime + timedelta(days=days)
        
        eq.available_quantity -= 1
        if eq.available_quantity == 0:
            eq.status = 'borrowed'
        
        db.session.commit()
        due_date = borrow_req.return_due_datetime.strftime('%d/%m/%Y')
        flash(f'อนุมัติยืม "{eq.name}" โดย {borrow_req.requester.full_name} (กำหนดคืน {due_date})', 'success')
        
        # 📧 ส่งอีเมลแจ้งผู้ยืม
        try:
            notify_user_approved(borrow_req)
        except Exception as e:
            current_app.logger.error(f'ส่งอีเมลแจ้งเตือนล้มเหลว: {e}')
    
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/reject_borrow/<int:req_id>', methods=['POST'])
@admin_required
def reject_borrow(req_id):
    borrow_req = BorrowRequest.query.get_or_404(req_id)
    if borrow_req.status != 'pending':
        flash('คำขอนี้ได้รับการดำเนินการแล้ว', 'warning')
        return redirect(url_for('admin.dashboard'))
    borrow_req.status = 'rejected'
    db.session.commit()
    flash(f'ปฏิเสธคำขอยืม "{borrow_req.equipment.name}"', 'info')
    
    # 📧 ส่งอีเมลแจ้งผู้ยืม
    try:
        notify_user_rejected(borrow_req)
    except Exception as e:
        current_app.logger.error(f'ส่งอีเมลแจ้งเตือนล้มเหลว: {e}')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/send_warning/<int:req_id>', methods=['POST'])
@admin_required
def send_warning(req_id):
    borrow_req = BorrowRequest.query.get_or_404(req_id)
    warning_msg = request.form.get('warning_message', '').strip()
    
    if borrow_req.status != 'approved':
        flash('สามารถส่งแจ้งเตือนเฉพาะรายการที่กำลังยืมเท่านั้น', 'warning')
        return redirect(url_for('admin.dashboard'))
        
    if warning_msg:
        borrow_req.warning_message = warning_msg
        db.session.commit()
        flash(f'ส่งข้อความแจ้งเตือนไปยัง {borrow_req.requester.full_name} แล้ว', 'success')
    else:
        flash('กรุณากรอกข้อความแจ้งเตือน', 'danger')
        
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/approve_return/<int:req_id>', methods=['POST'])
@admin_required
def approve_return(req_id):
    borrow_req = BorrowRequest.query.get_or_404(req_id)
    if borrow_req.status != 'return_pending':
        flash('คำขอนี้ไม่ได้อยู่ในสถานะรอรับคืน', 'warning')
        return redirect(url_for('admin.dashboard'))
        
    borrow_req.status = 'returned'
    borrow_req.returned_at = get_local_now()
    
    eq = borrow_req.equipment
    eq.available_quantity += 1
    if eq.available_quantity > 0:
        eq.status = 'available'
    
    # แจ้งสถานะความเสียหาย
    if borrow_req.damage_status == 'damaged':
        flash(f'⚠️ ยืนยันรับคืน "{eq.name}" — มีรายงานชำรุด: {borrow_req.damage_note}', 'warning')
    else:
        flash(f'✅ ยืนยันรับคืน "{eq.name}" — สภาพปกติ', 'success')
    
    db.session.commit()
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/update_repair/<int:repair_id>', methods=['POST'])
@admin_required
def update_repair(repair_id):
    repair_req = RepairRequest.query.get_or_404(repair_id)
    new_status = request.form.get('status')
    
    if new_status not in ['pending', 'in_progress', 'completed']:
        flash('สถานะไม่ถูกต้อง', 'danger')
        return redirect(url_for('admin.dashboard'))
        
    repair_req.status = new_status
    
    if new_status == 'completed':
        repair_req.resolved_at = get_local_now()
        # เปลี่ยนสถานะอุปกรณ์กลับเป็น available ถ้าซ่อมเสร็จ
        repair_req.equipment.status = 'available'
        flash(f'อัปเดตสถานะการซ่อม "{repair_req.equipment.name}" เป็น "ซ่อมเสร็จสิ้น"', 'success')
    elif new_status == 'in_progress':
        flash(f'อัปเดตสถานะการซ่อม "{repair_req.equipment.name}" เป็น "กำลังดำเนินการซ่อม"', 'info')
    
    db.session.commit()
    return redirect(url_for('admin.dashboard'))
