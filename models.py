from datetime import datetime, timezone, timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

def get_local_now():
    """ดึงเวลาปัจจุบันอ้างอิงเขตเวลาไทย (ICT, UTC+7) แบบ timezone-naive เพื่อใช้งานร่วมกับโมเดล"""
    return datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None)

# === สร้าง instance ของ SQLAlchemy ===
db = SQLAlchemy()

class Building(db.Model):
    """โมเดลอาคาร"""
    __tablename__ = 'buildings'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    floors = db.relationship('Floor', backref='building', lazy='dynamic', cascade="all, delete-orphan")

class Floor(db.Model):
    """โมเดลชั้น"""
    __tablename__ = 'floors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.id'), nullable=False)
    rooms = db.relationship('Room', backref='floor', lazy='dynamic', cascade="all, delete-orphan")

class Room(db.Model):
    """โมเดลห้อง"""
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    floor_id = db.Column(db.Integer, db.ForeignKey('floors.id'), nullable=False)
    equipments = db.relationship('Equipment', backref='room_ref', lazy='dynamic')


class User(UserMixin, db.Model):
    """โมเดลผู้ใช้งานระบบ"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    role = db.Column(db.String(10), nullable=False, default='user')
    profile_image = db.Column(db.Text, default='')
    student_id = db.Column(db.String(20), unique=True, nullable=True, index=True)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    verification_token = db.Column(db.String(100), nullable=True, index=True)
    verification_sent_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=get_local_now)
    
    borrow_requests = db.relationship('BorrowRequest', backref='requester', lazy='dynamic')

    @property
    def avatar_url(self):
        """ส่งคืน URL ของรูปโปรไฟล์ รองรับทั้ง Data URL (Base64) และ Static file"""
        if not self.profile_image:
            return None
        if self.profile_image.startswith('data:') or self.profile_image.startswith('http'):
            return self.profile_image
        return f"/static/uploads/{self.profile_image}"
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        return self.role == 'admin'

    def is_student(self):
        """ตรวจสอบว่าเป็นนักเรียนหรือไม่ (อีเมลขึ้นต้นด้วยตัวเลข @atcc.ac.th หรือ @*.ac.th)"""
        if self.is_admin():
            return False
        if not self.email:
            return False
        email_lower = self.email.lower()
        if email_lower.endswith('.ac.th'):
            username_part = email_lower.split('@')[0]
            return username_part.isdigit()
        return False

    def is_teacher(self):
        """ตรวจสอบว่าเป็นอาจารย์หรือไม่ (เป็น admin หรือ อีเมลขึ้นต้นด้วยตัวอักษร @atcc.ac.th)"""
        if self.is_admin():
            return True
        if not self.email:
            return False
        email_lower = self.email.lower()
        if email_lower.endswith('.ac.th'):
            username_part = email_lower.split('@')[0]
            return not username_part.isdigit()
        return False


class Equipment(db.Model):
    """โมเดลครุภัณฑ์ — รองรับทั้งครุภัณฑ์ยืมคืนและวัสดุสิ้นเปลือง"""
    __tablename__ = 'equipment'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    equipment_code = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, default='')
    
    # === หมวดหมู่ รูปภาพ จำนวน ===
    category = db.Column(db.String(100), default='ทั่วไป')
    image_filename = db.Column(db.Text, default='')
    total_quantity = db.Column(db.Integer, nullable=False, default=1)
    available_quantity = db.Column(db.Integer, nullable=False, default=1)
    
    # === ประเภทย่อย: 'durable' (ครุภัณฑ์ ยืม-คืน) หรือ 'consumable' (วัสดุสิ้นเปลือง) ===
    item_type = db.Column(db.String(20), nullable=False, default='durable')
    
    # === ชั้นของอาคาร และ สถานะการยืมกลับ ===
    floor = db.Column(db.Integer, nullable=True, default=0) # เก็บไว้ชั่วคราวเผื่อระบบพัง
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=True)
    is_borrowable = db.Column(db.Boolean, nullable=False, default=True)
    
    status = db.Column(db.String(20), nullable=False, default='available')
    
    borrow_requests = db.relationship('BorrowRequest', backref='equipment', lazy='dynamic')
    
    @property
    def image_url(self):
        """ส่งคืน URL ของรูปครุภัณฑ์ รองรับทั้ง Data URL (Base64) และ Static file"""
        if not self.image_filename:
            return None
        if self.image_filename.startswith('data:') or self.image_filename.startswith('http'):
            return self.image_filename
        return f"/static/uploads/{self.image_filename}"

    def is_durable(self):
        return self.item_type == 'durable'
    
    def is_consumable(self):
        return self.item_type == 'consumable'
    
    def __repr__(self):
        return f'<Equipment {self.equipment_code}: {self.name}>'


class BorrowRequest(db.Model):
    """โมเดลคำขอยืม-คืนครุภัณฑ์ / เบิกวัสดุสิ้นเปลือง"""
    __tablename__ = 'borrow_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')
    borrow_datetime = db.Column(db.DateTime, nullable=False, default=get_local_now)
    return_due_datetime = db.Column(db.DateTime, nullable=True)
    warning_message = db.Column(db.Text, default='')
    requested_at = db.Column(db.DateTime, default=get_local_now)
    approved_at = db.Column(db.DateTime, nullable=True)
    returned_at = db.Column(db.DateTime, nullable=True)
    
    # === ฟิลด์ใหม่: จำนวนวันยืม, สถานะความเสียหาย, จำนวนเบิก ===
    borrow_days = db.Column(db.Integer, nullable=True, default=3)        # ผู้ใช้ระบุจำนวนวันยืม
    quantity = db.Column(db.Integer, nullable=False, default=1)          # จำนวนที่เบิก (สำหรับวัสดุสิ้นเปลือง)
    damage_status = db.Column(db.String(20), default='normal')           # normal / damaged
    damage_note = db.Column(db.Text, default='')                         # รายละเอียดความเสียหาย
    return_image_filename = db.Column(db.Text, default='')               # รูปแนบส่งคืน (รองรับ Data URL Base64)
    overdue_notified = db.Column(db.Boolean, default=False)              # เคยส่งแจ้งเตือนเกินกำหนดหรือยัง
    hidden_by_user = db.Column(db.Boolean, default=False)                # ซ่อนจากแดชบอร์ดของผู้ใช้
    hidden_by_admin = db.Column(db.Boolean, default=False)               # ซ่อนจากแดชบอร์ดของแอดมิน (แต่ยังคงอยู่ในหน้าประวัติรวม)
    
    @property
    def return_image_url(self):
        """ส่งคืน URL ของรูปส่งคืน รองรับทั้ง Data URL (Base64) และ Static file"""
        if not self.return_image_filename:
            return None
        if self.return_image_filename.startswith('data:') or self.return_image_filename.startswith('http'):
            return self.return_image_filename
        return f"/static/uploads/{self.return_image_filename}"
    
    def is_overdue(self):
        """ตรวจว่ายืมเกินกำหนดหรือไม่"""
        if self.status == 'approved' and self.return_due_datetime:
            return get_local_now() > self.return_due_datetime
        return False


class RepairRequest(db.Model):
    """โมเดลแจ้งซ่อมครุภัณฑ์"""
    __tablename__ = 'repair_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    issue_description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending') # pending, in_progress, completed
    reported_at = db.Column(db.DateTime, default=get_local_now)
    resolved_at = db.Column(db.DateTime, nullable=True)
    admin_note = db.Column(db.Text, default='')
    
    equipment = db.relationship('Equipment', backref=db.backref('repair_requests', lazy='dynamic'))
    reporter = db.relationship('User', backref=db.backref('repair_requests', lazy='dynamic'))


class AuditLog(db.Model):
    """โมเดลประวัติการแก้ไขและจัดการข้อมูลระบบ (Audit Log / Activity History)"""
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    user = db.relationship('User', backref=db.backref('audit_logs', lazy='dynamic'))
    
    action = db.Column(db.String(50), nullable=False) # e.g. 'ADD_EQUIPMENT', 'EDIT_EQUIPMENT', 'DELETE_EQUIPMENT', 'DISPOSE_EQUIPMENT', 'ADD_BUILDING', etc.
    category = db.Column(db.String(30), nullable=False) # 'equipment', 'location'
    target_type = db.Column(db.String(30), nullable=False) # 'ครุภัณฑ์/อุปกรณ์', 'อาคาร', 'ชั้น', 'ห้อง'
    target_id = db.Column(db.Integer, nullable=True)
    target_name = db.Column(db.String(255), nullable=False)
    details = db.Column(db.Text, nullable=True)
    ip_address = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=get_local_now)


