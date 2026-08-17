"""สคริปต์สร้างฐานข้อมูลจำลอง — ข้อมูลอุปกรณ์ใหม่พร้อมรูปภาพ"""
from datetime import datetime, timedelta
from app import app
from models import db, User, Equipment, BorrowRequest


def init_database():
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        print('=== กำลังสร้างข้อมูลจำลอง ===')
        
        # ---------- ผู้ใช้จำลอง ----------
        admin = User(username='admin1', full_name='สมชาย ผู้ดูแลระบบ', email='admin1@lab.ac.th', role='admin')
        admin.set_password('admin1234')
        
        user1 = User(username='user1', full_name='สมหญิง นักศึกษา', email='user1@student.ac.th', role='user')
        user1.set_password('user1234')
        
        user2 = User(username='user2', full_name='สมศักดิ์ บุคลากร', email='user2@student.ac.th', role='user')
        user2.set_password('user2234')
        
        db.session.add_all([admin, user1, user2])
        db.session.commit()
        print('  ✓ สร้างผู้ใช้ 3 คน')
        
        # ---------- อุปกรณ์จำลอง (พร้อมรูปภาพ) ----------
        eq1 = Equipment(
            name='Laptop Dell XPS 13',
            equipment_code='EQ-001',
            description='แล็ปท็อปประสิทธิภาพสูง เหมาะสำหรับงานเขียนโปรแกรมและนำเสนอ',
            image_filename='laptop_dell_xps13.jpg',
            total_quantity=5,
            available_quantity=5,
            status='available'
        )
        eq2 = Equipment(
            name='Projector Epson',
            equipment_code='EQ-002',
            description='โปรเจคเตอร์ 1080p ความสว่าง 3300 lumens เหมาะสำหรับห้องประชุม',
            image_filename='projector_epson.jpg',
            total_quantity=2,
            available_quantity=2,
            status='available'
        )
        eq3 = Equipment(
            name='iPad Pro 12.9"',
            equipment_code='EQ-003',
            description='แท็บเล็ตสำหรับนำเสนองาน พร้อม Apple Pencil',
            image_filename='ipad_pro.jpg',
            total_quantity=3,
            available_quantity=3,
            status='available'
        )
        eq4 = Equipment(
            name='Camera Canon EOS',
            equipment_code='EQ-004',
            description='กล้อง DSLR บันทึกวิดีโอ 4K สำหรับงานกิจกรรม',
            image_filename='camera_canon_eos.jpg',
            total_quantity=2,
            available_quantity=2,
            status='available'
        )
        
        db.session.add_all([eq1, eq2, eq3, eq4])
        db.session.commit()
        print('  ✓ สร้างอุปกรณ์ 4 ชิ้น พร้อมรูปภาพ')
        
        # ---------- ประวัติการยืม ----------
        req1 = BorrowRequest(
            user_id=user1.id, equipment_id=eq1.id,
            borrow_datetime=datetime.utcnow() - timedelta(days=3),
            return_due_datetime=datetime.utcnow() + timedelta(days=1),
            status='approved',
            requested_at=datetime.utcnow() - timedelta(days=3),
            approved_at=datetime.utcnow() - timedelta(days=2)
        )
        eq1.available_quantity -= 1  # 5 -> 4
        
        req2 = BorrowRequest(
            user_id=user2.id, equipment_id=eq2.id,
            borrow_datetime=datetime.utcnow() - timedelta(days=2),
            return_due_datetime=datetime.utcnow() + timedelta(days=5),
            status='approved',
            requested_at=datetime.utcnow() - timedelta(days=2),
            approved_at=datetime.utcnow() - timedelta(days=1)
        )
        eq2.available_quantity -= 1  # 2 -> 1
        
        req3 = BorrowRequest(
            user_id=user1.id, equipment_id=eq3.id,
            borrow_datetime=datetime.utcnow() - timedelta(hours=5),
            return_due_datetime=datetime.utcnow() + timedelta(days=2),
            status='pending',
            requested_at=datetime.utcnow() - timedelta(hours=5)
        )
        
        req4 = BorrowRequest(
            user_id=user2.id, equipment_id=eq4.id,
            borrow_datetime=datetime.utcnow() - timedelta(days=10),
            return_due_datetime=datetime.utcnow() - timedelta(days=7),
            status='returned',
            requested_at=datetime.utcnow() - timedelta(days=10),
            approved_at=datetime.utcnow() - timedelta(days=9),
            returned_at=datetime.utcnow() - timedelta(days=5)
        )
        
        db.session.add_all([req1, req2, req3, req4])
        db.session.commit()
        print('  ✓ สร้างประวัติการยืม 4 รายการ')
        
        print('\n=== สร้างฐานข้อมูลเสร็จสมบูรณ์ ===')
        print('\n--- บัญชีทดสอบ ---')
        print('Admin:  admin1 / admin1234')
        print('User 1: user1  / user1234')
        print('User 2: user2  / user2234')
        
        print('\n--- อุปกรณ์ ---')
        for eq in Equipment.query.all():
            print(f'  {eq.equipment_code}: {eq.name} — ว่าง: {eq.available_quantity}/{eq.total_quantity}')


if __name__ == '__main__':
    init_database()
