from flask import render_template, redirect, url_for, flash, request
from models import db, Building, Floor, Room
from utils import admin_required
from . import admin_bp

# ==========================================
# 1. จัดการอาคาร (Building)
# ==========================================

@admin_bp.route('/locations')
@admin_required
def manage_locations():
    """หน้าหลัก: แสดงรายการอาคารทั้งหมด พร้อมสถิติภาพรวมและโครงสร้างย่อย"""
    buildings = Building.query.all()
    total_floors = Floor.query.count()
    total_rooms = Room.query.count()
    
    # คำนวณจำนวนอุปกรณ์ทั้งหมดที่ถูกติดตั้งในห้อง
    from models import Equipment
    total_equipments = Equipment.query.filter(Equipment.room_id.isnot(None)).count()
    
    return render_template('admin_locations.html', 
                           buildings=buildings, 
                           total_floors=total_floors,
                           total_rooms=total_rooms,
                           total_equipments=total_equipments)

@admin_bp.route('/building/add', methods=['GET', 'POST'])
@admin_required
def add_building():
    """หน้าฟอร์มเพิ่มอาคารใหม่"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if name:
            new_building = Building(name=name)
            db.session.add(new_building)
            db.session.commit()
            flash(f'เพิ่มอาคาร "{name}" เรียบร้อยแล้ว', 'success')
            return redirect(url_for('admin.manage_locations'))
        else:
            flash('กรุณากรอกชื่ออาคาร', 'danger')
            
    return render_template('admin_building_form.html', building=None)

@admin_bp.route('/building/edit/<int:b_id>', methods=['GET', 'POST'])
@admin_required
def edit_building(b_id):
    """หน้าฟอร์มแก้ไขชื่ออาคาร"""
    building = Building.query.get_or_404(b_id)
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if name:
            building.name = name
            db.session.commit()
            flash(f'แก้ไขอาคารสำเร็จ', 'success')
            return redirect(url_for('admin.manage_locations'))
        else:
            flash('กรุณากรอกชื่ออาคาร', 'danger')
            
    return render_template('admin_building_form.html', building=building)

@admin_bp.route('/building/delete/<int:b_id>', methods=['POST'])
@admin_required
def delete_building(b_id):
    building = Building.query.get_or_404(b_id)
    db.session.delete(building)
    db.session.commit()
    flash(f'ลบอาคารเรียบร้อยแล้ว', 'success')
    return redirect(url_for('admin.manage_locations'))

# ==========================================
# 2. จัดการรายละเอียดภายในอาคาร (Detail)
# ==========================================

@admin_bp.route('/building/<int:b_id>/manage')
@admin_required
def manage_building_detail(b_id):
    """หน้ารายละเอียดอาคาร: แสดงชั้นและห้องภายในอาคารที่เลือก"""
    building = Building.query.get_or_404(b_id)
    return render_template('admin_building_detail.html', building=building)

# ==========================================
# 3. จัดการชั้น (Floor)
# ==========================================

@admin_bp.route('/building/<int:b_id>/floor/add', methods=['GET', 'POST'])
@admin_required
def add_floor(b_id):
    """หน้าฟอร์มเพิ่มชั้น"""
    building = Building.query.get_or_404(b_id)
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if name:
            new_floor = Floor(name=name, building_id=b_id)
            db.session.add(new_floor)
            db.session.commit()
            flash(f'เพิ่มชั้นเรียบร้อยแล้ว', 'success')
            return redirect(url_for('admin.manage_building_detail', b_id=b_id))
        else:
            flash('กรุณากรอกชื่อชั้น', 'danger')
            
    return render_template('admin_floor_form.html', building=building, floor=None)

@admin_bp.route('/floor/edit/<int:f_id>', methods=['GET', 'POST'])
@admin_required
def edit_floor(f_id):
    """หน้าฟอร์มแก้ไขชื่อชั้น"""
    floor = Floor.query.get_or_404(f_id)
    b_id = floor.building_id
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if name:
            floor.name = name
            db.session.commit()
            flash(f'แก้ไขชั้นสำเร็จ', 'success')
            return redirect(url_for('admin.manage_building_detail', b_id=b_id))
        else:
            flash('กรุณากรอกชื่อชั้น', 'danger')
            
    return render_template('admin_floor_form.html', building=floor.building, floor=floor)

@admin_bp.route('/floor/delete/<int:f_id>', methods=['POST'])
@admin_required
def delete_floor(f_id):
    floor = Floor.query.get_or_404(f_id)
    b_id = floor.building_id
    db.session.delete(floor)
    db.session.commit()
    flash(f'ลบชั้นเรียบร้อยแล้ว', 'success')
    return redirect(url_for('admin.manage_building_detail', b_id=b_id))

# ==========================================
# 4. จัดการห้อง (Room)
# ==========================================

@admin_bp.route('/floor/<int:f_id>/room/add', methods=['GET', 'POST'])
@admin_required
def add_room(f_id):
    """หน้าฟอร์มเพิ่มห้องเดียว"""
    floor = Floor.query.get_or_404(f_id)
    b_id = floor.building_id
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if name:
            new_room = Room(name=name, floor_id=f_id)
            db.session.add(new_room)
            db.session.commit()
            flash(f'เพิ่มห้อง "{name}" เรียบร้อยแล้ว', 'success')
            return redirect(url_for('admin.manage_building_detail', b_id=b_id))
        else:
            flash('กรุณากรอกชื่อห้อง', 'danger')
            
    return render_template('admin_room_form.html', floor=floor, room=None)

@admin_bp.route('/floor/<int:f_id>/room/bulk_add', methods=['POST'])
@admin_required
def bulk_add_rooms(f_id):
    """เพิ่มทีละหลายห้องอัตโนมัติ (เช่น 201 ถึง 205)"""
    floor = Floor.query.get_or_404(f_id)
    b_id = floor.building_id
    prefix = request.form.get('prefix', '').strip()
    start_num = request.form.get('start_num', type=int)
    end_num = request.form.get('end_num', type=int)

    if start_num is None or end_num is None or start_num > end_num:
        flash('กรุณาระบุช่วงตัวเลขห้องให้ถูกต้อง', 'danger')
        return redirect(url_for('admin.manage_building_detail', b_id=b_id))

    created_count = 0
    for num in range(start_num, end_num + 1):
        room_name = f"{prefix}{num}" if prefix else str(num)
        # ตรวจสอบว่ามีห้องชื่อนี้ในชั้นหรือยัง
        existing = Room.query.filter_by(floor_id=f_id, name=room_name).first()
        if not existing:
            new_room = Room(name=room_name, floor_id=f_id)
            db.session.add(new_room)
            created_count += 1

    db.session.commit()
    flash(f'สร้างห้องใหม่สำเร็จจำนวน {created_count} ห้องในชั้น {floor.name}', 'success')
    return redirect(url_for('admin.manage_building_detail', b_id=b_id))

@admin_bp.route('/room/edit/<int:r_id>', methods=['GET', 'POST'])
@admin_required
def edit_room(r_id):
    """หน้าฟอร์มแก้ไขห้อง"""
    room = Room.query.get_or_404(r_id)
    b_id = room.floor.building_id
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if name:
            room.name = name
            db.session.commit()
            flash(f'แก้ไขห้องสำเร็จ', 'success')
            return redirect(url_for('admin.manage_building_detail', b_id=b_id))
        else:
            flash('กรุณากรอกชื่อห้อง', 'danger')
            
    return render_template('admin_room_form.html', floor=room.floor, room=room)

@admin_bp.route('/room/delete/<int:r_id>', methods=['POST'])
@admin_required
def delete_room(r_id):
    room = Room.query.get_or_404(r_id)
    b_id = room.floor.building_id
    if room.equipments.count() > 0:
        flash(f'ไม่สามารถลบห้องที่มีอุปกรณ์อยู่ได้ กรุณาย้ายอุปกรณ์ก่อน', 'danger')
    else:
        db.session.delete(room)
        db.session.commit()
        flash(f'ลบห้องเรียบร้อยแล้ว', 'success')
    return redirect(url_for('admin.manage_building_detail', b_id=b_id))

@admin_bp.route('/api/room/<int:r_id>/equipments')
@admin_required
def api_room_equipments(r_id):
    """ส่งคืนรายการครุภัณฑ์ภายในห้องในรูปแบบ JSON เพื่อแสดงผลใน Modal"""
    from flask import jsonify
    room = Room.query.get_or_404(r_id)
    items = []
    for eq in room.equipments:
        items.append({
            'id': eq.id,
            'code': eq.equipment_code,
            'name': eq.name,
            'category': eq.category,
            'type': 'ครุภัณฑ์ยืม-คืน' if eq.item_type == 'durable' else 'วัสดุสิ้นเปลือง',
            'available': eq.available_quantity,
            'total': eq.total_quantity,
            'status': eq.status
        })
    return jsonify({
        'room_name': room.name,
        'building_name': room.floor.building.name,
        'floor_name': room.floor.name,
        'equipments': items
    })

