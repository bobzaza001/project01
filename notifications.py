"""
notifications.py — โมดูลระบบแจ้งเตือนผ่านอีเมล
ใช้สำหรับส่งอีเมลแจ้งเตือนผู้ยืมครุภัณฑ์เมื่อคำขอได้รับการอนุมัติ/ปฏิเสธ
และส่งอีเมลเตือนเมื่อครุภัณฑ์ใกล้ถึงกำหนดส่งคืน
"""

import logging
from datetime import datetime, timedelta
from flask import current_app
from flask_mail import Message

logger = logging.getLogger(__name__)


def get_mail():
    """ดึง Flask-Mail instance จาก extensions"""
    from extensions import mail
    return mail


def send_email(to, subject, body_html):
    """
    ส่งอีเมลพื้นฐาน — รับผู้รับ, หัวข้อ, และเนื้อหา HTML
    จะ log ข้อผิดพลาดแทนการ raise exception เพื่อไม่ให้ระบบหลักหยุดทำงาน
    """
    try:
        mail = get_mail()
        sender = current_app.config.get('MAIL_DEFAULT_SENDER', '')
        if not sender:
            logger.warning("MAIL_DEFAULT_SENDER ไม่ได้ตั้งค่า — ข้ามการส่งอีเมล")
            return False

        msg = Message(
            subject=subject,
            sender=sender,
            recipients=[to] if isinstance(to, str) else to,
            html=body_html
        )
        mail.send(msg)
        logger.info(f"📧 ส่งอีเมลสำเร็จ → {to} | หัวข้อ: {subject}")
        return True
    except Exception as e:
        logger.error(f"❌ ส่งอีเมลล้มเหลว → {to} | ข้อผิดพลาด: {e}")
        return False


# ──────────────────────────────────────────────
#  HTML Email Templates
# ──────────────────────────────────────────────

def _email_wrapper(content_html):
    """Wrapper HTML template สำหรับอีเมลทุกประเภท — ธีมสีน้ำเงินมิดไนท์"""
    return f"""
    <div style="font-family: 'Segoe UI', Tahoma, sans-serif; max-width: 600px; margin: 0 auto; background: #f8fafc; border-radius: 16px; overflow: hidden; border: 1px solid #e2e8f0;">
        <!-- Header -->
        <div style="background: linear-gradient(135deg, #0284C7 0%, #1E3A8A 100%); padding: 24px 32px; text-align: center;">
            <h1 style="color: white; margin: 0; font-size: 1.25rem; font-weight: 700; letter-spacing: 0.5px;">
                🔬 LAB Equipment System
            </h1>
            <p style="color: rgba(255,255,255,0.75); margin: 4px 0 0; font-size: 0.85rem;">
                ระบบจัดการครุภัณฑ์ห้องปฏิบัติการ — ATCC
            </p>
        </div>
        <!-- Body -->
        <div style="padding: 32px;">
            {content_html}
        </div>
        <!-- Footer -->
        <div style="background: #f1f5f9; padding: 16px 32px; text-align: center; border-top: 1px solid #e2e8f0;">
            <p style="margin: 0; font-size: 0.75rem; color: #94a3b8;">
                อีเมลนี้ถูกส่งอัตโนมัติจากระบบจัดการครุภัณฑ์ กรุณาอย่าตอบกลับอีเมลนี้
            </p>
        </div>
    </div>
    """


# ──────────────────────────────────────────────
#  Notification Functions
# ──────────────────────────────────────────────

def notify_user_approved(borrow_req):
    """ส่งอีเมลแจ้งผู้ยืมว่าคำขอได้รับการอนุมัติ"""
    if not current_app.config.get('NOTIFY_ON_APPROVE', True):
        return False

    user = borrow_req.requester
    eq = borrow_req.equipment

    borrow_date = borrow_req.borrow_datetime.strftime('%d/%m/%Y') if borrow_req.borrow_datetime else '-'
    due_date = borrow_req.return_due_datetime.strftime('%d/%m/%Y') if borrow_req.return_due_datetime else '-'

    content = f"""
    <h2 style="color: #0f172a; margin: 0 0 16px; font-size: 1.15rem;">
        ✅ คำขอยืมครุภัณฑ์ของคุณได้รับการอนุมัติแล้ว
    </h2>
    <p style="color: #475569; line-height: 1.6; margin: 0 0 20px;">
        สวัสดีครับ/ค่ะ คุณ<strong>{user.full_name}</strong>,
    </p>
    <div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 12px; padding: 20px; margin-bottom: 20px;">
        <table style="width: 100%; border-collapse: collapse; font-size: 0.92rem; color: #334155;">
            <tr>
                <td style="padding: 6px 0; font-weight: 600; width: 140px;">📦 ครุภัณฑ์:</td>
                <td style="padding: 6px 0;">{eq.name}</td>
            </tr>
            <tr>
                <td style="padding: 6px 0; font-weight: 600;">🏷️ รหัส:</td>
                <td style="padding: 6px 0;"><code style="background: #e0f2fe; padding: 2px 8px; border-radius: 4px; font-size: 0.85rem;">{eq.equipment_code}</code></td>
            </tr>
            <tr>
                <td style="padding: 6px 0; font-weight: 600;">📅 วันที่ยืม:</td>
                <td style="padding: 6px 0;">{borrow_date}</td>
            </tr>
            <tr>
                <td style="padding: 6px 0; font-weight: 600;">⏰ กำหนดส่งคืน:</td>
                <td style="padding: 6px 0;"><strong style="color: #dc2626;">{due_date}</strong></td>
            </tr>
        </table>
    </div>
    <p style="color: #475569; line-height: 1.6; margin: 0;">
        กรุณาติดต่อรับครุภัณฑ์ได้ที่เจ้าหน้าที่ดูแลระบบ<br>
        และส่งคืนตามกำหนดเวลาที่ระบุด้านบน
    </p>
    """
    return send_email(
        to=user.email,
        subject='✅ คำขอยืมครุภัณฑ์ของคุณได้รับการอนุมัติแล้ว',
        body_html=_email_wrapper(content)
    )


def notify_user_rejected(borrow_req):
    """ส่งอีเมลแจ้งผู้ยืมว่าคำขอถูกปฏิเสธ"""
    if not current_app.config.get('NOTIFY_ON_REJECT', True):
        return False

    user = borrow_req.requester
    eq = borrow_req.equipment

    reason_html = ""
    if borrow_req.warning_message:
        reason_html = f"""
        <tr>
            <td style="padding: 6px 0; font-weight: 600; color: #dc2626;">💬 เหตุผล:</td>
            <td style="padding: 6px 0; color: #dc2626;">{borrow_req.warning_message}</td>
        </tr>
        """

    content = f"""
    <h2 style="color: #0f172a; margin: 0 0 16px; font-size: 1.15rem;">
        ❌ คำขอยืมครุภัณฑ์ของคุณถูกปฏิเสธ
    </h2>
    <p style="color: #475569; line-height: 1.6; margin: 0 0 20px;">
        สวัสดีครับ/ค่ะ คุณ<strong>{user.full_name}</strong>,
    </p>
    <div style="background: #fef2f2; border: 1px solid #fecaca; border-radius: 12px; padding: 20px; margin-bottom: 20px;">
        <table style="width: 100%; border-collapse: collapse; font-size: 0.92rem; color: #334155;">
            <tr>
                <td style="padding: 6px 0; font-weight: 600; width: 140px;">📦 ครุภัณฑ์:</td>
                <td style="padding: 6px 0;">{eq.name}</td>
            </tr>
            <tr>
                <td style="padding: 6px 0; font-weight: 600;">🏷️ รหัส:</td>
                <td style="padding: 6px 0;"><code style="background: #fee2e2; padding: 2px 8px; border-radius: 4px; font-size: 0.85rem;">{eq.equipment_code}</code></td>
            </tr>
            {reason_html}
        </table>
    </div>
    <p style="color: #475569; line-height: 1.6; margin: 0;">
        หากมีข้อสงสัย กรุณาติดต่อผู้ดูแลระบบโดยตรง<br>
        หรือทำรายการขอยืมครุภัณฑ์ชิ้นอื่นได้ใหม่อีกครั้ง
    </p>
    """
    return send_email(
        to=user.email,
        subject='❌ คำขอยืมครุภัณฑ์ของคุณถูกปฏิเสธ',
        body_html=_email_wrapper(content)
    )


def check_and_send_due_warnings():
    """
    ตรวจสอบรายการยืมที่จะครบกำหนดส่งคืนภายใน 24 ชั่วโมงข้างหน้า
    แล้วส่งอีเมลแจ้งเตือนผู้ยืม — เรียกใช้โดย APScheduler ทุกวัน 08:00
    """
    from models import db, BorrowRequest, get_local_now

    try:
        if not current_app.config.get('NOTIFY_DUE_REMINDER', True):
            logger.info("🔕 ระบบแจ้งเตือนก่อนครบกำหนดถูกปิดอยู่ — ข้าม")
            return

        now = get_local_now()
        tomorrow = now + timedelta(hours=24)

        # ค้นหารายการที่ครบกำหนดภายใน 24 ชม. ที่ยังไม่ได้แจ้งเตือน
        due_soon = BorrowRequest.query.filter(
            BorrowRequest.status == 'approved',
            BorrowRequest.return_due_datetime.isnot(None),
            BorrowRequest.return_due_datetime <= tomorrow,
            BorrowRequest.return_due_datetime > now,
            BorrowRequest.overdue_notified == False
        ).all()

        if not due_soon:
            logger.info("✅ ไม่มีรายการยืมที่ใกล้ครบกำหนด")
            return

        sent_count = 0
        for req in due_soon:
            user = req.requester
            eq = req.equipment
            due_date = req.return_due_datetime.strftime('%d/%m/%Y')

            content = f"""
            <h2 style="color: #b91c1c; margin: 0 0 16px; font-size: 1.25rem; font-weight: 700;">
                ⚠️ แจ้งเตือนด่วน: กรุณาส่งคืนครุภัณฑ์เกินกำหนด
            </h2>
            <p style="color: #475569; line-height: 1.6; margin: 0 0 20px;">
                เรียน คุณ<strong>{user.full_name}</strong>,<br><br>
                ระบบตรวจสอบพบว่ารายการครุภัณฑ์ที่คุณยืมไว้ขณะนี้ **เกินกำหนดเวลาส่งคืนแล้ว** 
                กรุณานำอุปกรณ์ดังกล่าวมาส่งคืน ณ ห้องปฏิบัติการกลางโดยด่วนที่สุด เพื่อไม่ให้ส่งผลกระทบต่อสิทธิ์การใช้งานของท่านและการใช้งานของผู้อื่น
            </p>
            <div style="background: #fff1f2; border: 1px solid #fecdd3; border-radius: 12px; padding: 20px; margin-bottom: 20px;">
                <table style="width: 100%; border-collapse: collapse; font-size: 0.92rem; color: #334155;">
                    <tr>
                        <td style="padding: 6px 0; font-weight: 600; width: 140px; color: #b91c1c;">📦 ครุภัณฑ์:</td>
                        <td style="padding: 6px 0; font-weight: bold;">{eq.name}</td>
                    </tr>
                    <tr>
                        <td style="padding: 6px 0; font-weight: 600; color: #b91c1c;">🏷️ รหัสครุภัณฑ์:</td>
                        <td style="padding: 6px 0;"><code style="background: #ffe4e6; padding: 2px 8px; border-radius: 4px; font-size: 0.85rem; color: #b91c1c; font-weight: bold;">{eq.equipment_code}</code></td>
                    </tr>
                    <tr>
                        <td style="padding: 6px 0; font-weight: 600; color: #b91c1c;">⏰ กำหนดส่งคืน:</td>
                        <td style="padding: 6px 0;"><strong style="color: #e11d48;">{due_date} (เกินกำหนดส่งคืน)</strong></td>
                    </tr>
                </table>
            </div>
            <div style="background: #fffbeb; border: 1px solid #fde68a; border-radius: 12px; padding: 16px; font-size: 0.88rem; color: #854d0e; line-height: 1.5;">
                ⚠️ <strong>หมายเหตุ:</strong> กรุณาติดต่อส่งคืนอุปกรณ์โดยด่วนที่สุดเพื่อป้องกันการถูกระงับสิทธิ์การใช้งานชั่วคราว
            </div>
            """

            success = send_email(
                to=user.email,
                subject=f'⚠️ แจ้งเตือนด่วน: กรุณาส่งคืนครุภัณฑ์ "{eq.name}" ที่เกินกำหนดส่งคืน',
                body_html=_email_wrapper(content)
            )

            if success:
                req.overdue_notified = True
                sent_count += 1

        db.session.commit()
        logger.info(f"📧 ส่งอีเมลแจ้งเตือนก่อนครบกำหนดสำเร็จ {sent_count}/{len(due_soon)} รายการ")

    except Exception as e:
        logger.error(f"❌ Scheduler check_and_send_due_warnings ล้มเหลว: {e}")
