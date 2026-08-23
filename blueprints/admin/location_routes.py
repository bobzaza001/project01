from flask import render_template, redirect, url_for, flash, request, jsonify
from models import db, Building, Floor, Room, Equipment
from utils import admin_required, log_audit
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
            
            # บันทึก Audit Log
            log_audit(
                action='ADD_BUILDING',
                category='location',
                target_type='อาคาร',
                target_name=name,
                details=f"เพิ่มอาคารเรียน/สถานที่ใหม่: '{name}'",
                target_id=new_building.id
            )
            
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
    old_name = building.name
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if name:
            building.name = name
            db.session.commit()
            
            # บันทึก Audit Log
            log_audit(
                action='EDIT_BUILDING',
                category='location',
                target_type='อาคาร',
                target_name=name,
                details=f"เปลี่ยนชื่ออาคารจาก '{old_name}' เป็น '{name}'",
                target_id=building.id
            )
            
            flash(f'แก้ไขอาคารสำเร็จ', 'success')
            return redirect(url_for('admin.manage_locations'))
        else:
            flash('กรุณากรอกชื่ออาคาร', 'danger')
            
    return render_template('admin_building_form.html', building=building)

@admin_bp.route('/building/delete/<int:b_id>', methods=['POST'])
@admin_required
def delete_building(b_id):
    building = Building.query.get_or_404(b_id)
    b_name = building.name
    floors_count = building.floors.count()
    
    db.session.delete(building)
    db.session.commit()
    
    # บันทึก Audit Log
    log_audit(
        action='DELETE_BUILDING',
        category='location',
        target_type='อาคาร',
        target_name=b_name,
        details=f"ลบอาคาร '{b_name}' พร้อมโครงสร้างชั้นและห้องทั้งหมด ({floors_count} ชั้น)",
        target_id=b_id
    )
    
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
            
            # บันทึก Audit Log
            log_audit(
                action='ADD_FLOOR',
                category='location',
                target_type='ชั้น',
                target_name=f"{name} ({building.name})",
                details=f"เพิ่มชั้นใหม่: '{name}' ในอาคาร '{building.name}'",
                target_id=new_floor.id
            )
            
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
    old_name = floor.name
    b_name = floor.building.name
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if name:
            floor.name = name
            db.session.commit()
            
            # บันทึก Audit Log
            log_audit(
                action='EDIT_FLOOR',
                category='location',
                target_type='ชั้น',
                target_name=f"{name} ({b_name})",
                details=f"เปลี่ยนชื่อชั้นจาก '{old_name}' เป็น '{name}' ในอาคาร '{b_name}'",
                target_id=floor.id
            )
            
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
    f_name = floor.name
    b_name = floor.building.name
    rooms_count = floor.rooms.count()
    
    db.session.delete(floor)
    db.session.commit()
    
    # บันทึก Audit Log
    log_audit(
        action='DELETE_FLOOR',
        category='location',
        target_type='ชั้น',
        target_name=f"{f_name} ({b_name})",
        details=f"ลบชั้น '{f_name}' ในอาคาร '{b_name}' พร้อมห้องภายใน ({rooms_count} ห้อง)",
        target_id=f_id
    )
    
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
            
            # บันทึก Audit Log
            log_audit(
                action='ADD_ROOM',
                category='location',
                target_type='ห้อง',
                target_name=f"ห้อง {name} ({floor.name}, {floor.building.name})",
                details=f"เพิ่มห้องใหม่: 'ห้อง {name}' ใน {floor.name} อาคาร {floor.building.name}",
                target_id=new_room.id
            )
            
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
    added_names = []
    for num in range(start_num, end_num + 1):
        room_name = f"{prefix}{num}" if prefix else str(num)
        existing = Room.query.filter_by(floor_id=f_id, name=room_name).first()
        if not existing:
            new_room = Room(name=room_name, floor_id=f_id)
            db.session.add(new_room)
            created_count += 1
            added_names.append(room_name)

    db.session.commit()
    
    # บันทึก Audit Log
    if created_count > 0:
        log_audit(
            action='ADD_ROOM_BULK',
            category='location',
            target_type='ห้อง',
            target_name=f"ชุดห้อง {prefix}{start_num}-{prefix}{end_num} ({floor.name}, {floor.building.name})",
            details=f"เพิ่มห้องแบบกลุ่มจำนวน {created_count} ห้อง ({', '.join(added_names[:5])}{'...' if len(added_names) > 5 else ''}) ใน {floor.name} อาคาร {floor.building.name}",
            target_id=floor.id
        )
        
    flash(f'สร้างห้องใหม่สำเร็จจำนวน {created_count} ห้องในชั้น {floor.name}', 'success')
    return redirect(url_for('admin.manage_building_detail', b_id=b_id))

@admin_bp.route('/room/edit/<int:r_id>', methods=['GET', 'POST'])
@admin_required
def edit_room(r_id):
    """หน้าฟอร์มแก้ไขห้อง"""
    room = Room.query.get_or_404(r_id)
    b_id = room.floor.building_id
    old_name = room.name
    f_name = room.floor.name
    b_name = room.floor.building.name
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if name:
            room.name = name
            db.session.commit()
            
            # บันทึก Audit Log
            log_audit(
                action='EDIT_ROOM',
                category='location',
                target_type='ห้อง',
                target_name=f"ห้อง {name} ({f_name}, {b_name})",
                details=f"เปลี่ยนชื่อห้องจาก 'ห้อง {old_name}' เป็น 'ห้อง {name}' ใน {f_name} อาคาร {b_name}",
                target_id=room.id
            )
            
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
    r_name = room.name
    f_name = room.floor.name
    b_name = room.floor.building.name
    
    if room.equipments.count() > 0:
        flash(f'ไม่สามารถลบห้องที่มีอุปกรณ์อยู่ได้ กรุณาย้ายอุปกรณ์ก่อน', 'danger')
    else:
        db.session.delete(room)
        db.session.commit()
        
        # บันทึก Audit Log
        log_audit(
            action='DELETE_ROOM',
            category='location',
            target_type='ห้อง',
            target_name=f"ห้อง {r_name} ({f_name}, {b_name})",
            details=f"ลบห้อง 'ห้อง {r_name}' ใน {f_name} อาคาร {b_name}",
            target_id=r_id
        )
        
        flash(f'ลบห้องเรียบร้อยแล้ว', 'success')
    return redirect(url_for('admin.manage_building_detail', b_id=b_id))

@admin_bp.route('/api/room/<int:r_id>/equipments')
@admin_required
def api_room_equipments(r_id):
    """ส่งคืนรายการครุภัณฑ์ภายในห้องในรูปแบบ JSON เพื่อแสดงผลใน Modal"""
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
