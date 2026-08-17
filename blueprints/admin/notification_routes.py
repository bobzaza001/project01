"""
notification_routes.py — เส้นทางหน้าตั้งค่าระบบแจ้งเตือนอีเมล (Admin)
"""
from flask import render_template, redirect, url_for, flash, request, current_app
from utils import admin_required
from . import admin_bp


@admin_bp.route('/notification-settings')
@admin_required
def notification_settings():
    """หน้าตั้งค่าระบบแจ้งเตือนอีเมล"""
    mail_configured = bool(current_app.config.get('MAIL_USERNAME'))
    return render_template('admin_notification_settings.html',
                           mail_configured=mail_configured)


@admin_bp.route('/notification-settings/toggle', methods=['POST'])
@admin_required
def toggle_notification():
    """สลับเปิด/ปิดการแจ้งเตือนแต่ละประเภท"""
    setting = request.form.get('setting')
    
    toggle_map = {
        'notify_approve': 'NOTIFY_ON_APPROVE',
        'notify_reject': 'NOTIFY_ON_REJECT',
        'notify_due': 'NOTIFY_DUE_REMINDER',
    }

    if setting in toggle_map:
        config_key = toggle_map[setting]
        current_val = current_app.config.get(config_key, True)
        current_app.config[config_key] = not current_val
        status = 'เปิด' if not current_val else 'ปิด'
        flash(f'สลับการแจ้งเตือนเป็น: {status}', 'success')
    else:
        flash('การตั้งค่าไม่ถูกต้อง', 'danger')

    return redirect(url_for('admin.notification_settings'))


@admin_bp.route('/notification-settings/test-email', methods=['POST'])
@admin_required
def test_email():
    """ทดสอบส่งอีเมลไปยังที่อยู่ที่ระบุ"""
    test_to = request.form.get('test_email', '').strip()

    if not test_to:
        flash('กรุณากรอกอีเมลปลายทางสำหรับทดสอบ', 'warning')
        return redirect(url_for('admin.notification_settings'))

    from notifications import send_email, _email_wrapper

    content = """
    <h2 style="color: #b91c1c; margin: 0 0 16px; font-size: 1.25rem; font-weight: 700;">
        🚨 แจ้งเตือนด่วน: กรุณาส่งคืนครุภัณฑ์เกินกำหนด
    </h2>
    <p style="color: #475569; line-height: 1.6; margin: 0 0 20px;">
        เรียน คุณผู้ใช้งาน,<br><br>
        ระบบตรวจสอบพบว่าคุณมีรายการครุภัณฑ์ที่ทำการยืมไว้เป็นเวลานานและ **เกินกำหนดส่งคืนแล้ว** 
        กรุณานำอุปกรณ์ดังกล่าวมาส่งคืน ณ ห้องปฏิบัติการคอมพิวเตอร์โดยด่วนที่สุด เพื่อให้เพื่อนนักศึกษาและอาจารย์ท่านอื่นสามารถใช้งานต่อไปได้
    </p>
    
    <div style="background: #fff1f2; border: 1px solid #fecdd3; border-radius: 12px; padding: 20px; margin-bottom: 20px;">
        <table style="width: 100%; border-collapse: collapse; font-size: 0.92rem; color: #334155;">
            <tr>
                <td style="padding: 6px 0; font-weight: 600; width: 140px; color: #b91c1c;">📦 ครุภัณฑ์:</td>
                <td style="padding: 6px 0; font-weight: bold;">กล้อง DSLR Canon EOS 80D (ตัวอย่างทดสอบ)</td>
            </tr>
            <tr>
                <td style="padding: 6px 0; font-weight: 600; color: #b91c1c;">🏷️ รหัสครุภัณฑ์:</td>
                <td style="padding: 6px 0;"><code style="background: #ffe4e6; padding: 2px 8px; border-radius: 4px; font-size: 0.85rem; color: #b91c1c; font-weight: bold;">EQ-CAM-001</code></td>
            </tr>
            <tr>
                <td style="padding: 6px 0; font-weight: 600; color: #b91c1c;">📅 วันที่ยืม:</td>
                <td style="padding: 6px 0;">01/08/2026</td>
            </tr>
            <tr>
                <td style="padding: 6px 0; font-weight: 600; color: #b91c1c;">⏰ กำหนดส่งคืน:</td>
                <td style="padding: 6px 0;"><strong style="color: #e11d48;">10/08/2026 (เกินกำหนดมาแล้ว 7 วัน)</strong></td>
            </tr>
        </table>
    </div>

    <div style="background: #fffbeb; border: 1px solid #fde68a; border-radius: 12px; padding: 16px; font-size: 0.88rem; color: #854d0e; line-height: 1.5;">
        ⚠️ <strong>หมายเหตุ:</strong> การค้างส่งคืนครุภัณฑ์เกินกำหนดอาจส่งผลต่อการพิจารณาอนุมัติคำขอยืมในครั้งถัดไป
    </div>
    """

    success = send_email(
        to=test_to,
        subject='⚠️ แจ้งเตือนด่วน: กรุณาส่งคืนครุภัณฑ์เกินกำหนด — LAB Equipment System',
        body_html=_email_wrapper(content)
    )

    if success:
        flash(f'✅ ส่งอีเมลทดสอบไปยัง {test_to} สำเร็จ! ตรวจสอบกล่องจดหมายได้เลย', 'success')
    else:
        flash(f'❌ ส่งอีเมลทดสอบล้มเหลว — กรุณาตรวจสอบการตั้งค่า SMTP ในไฟล์ .env', 'danger')

    return redirect(url_for('admin.notification_settings'))


@admin_bp.route('/notification-settings/run-check', methods=['POST'])
@admin_required
def run_due_check():
    """เรียกใช้ตรวจสอบรายการใกล้ครบกำหนดด้วยตนเอง (ไม่ต้องรอ Scheduler)"""
    from notifications import check_and_send_due_warnings
    try:
        check_and_send_due_warnings()
        flash('✅ ตรวจสอบรายการใกล้ครบกำหนดและส่งอีเมลเรียบร้อยแล้ว', 'success')
    except Exception as e:
        flash(f'❌ เกิดข้อผิดพลาด: {e}', 'danger')
    return redirect(url_for('admin.notification_settings'))
