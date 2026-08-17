from app import app
from models import db, Building, Floor, Room, Equipment
from sqlalchemy import text
import re

def run_migration():
    with app.app_context():
        print("Creating new tables...")
        # create_all will create Building, Floor, Room tables
        db.create_all()
        
        # Add room_id to equipment (if not exists)
        try:
            db.session.execute(text("ALTER TABLE equipment ADD COLUMN room_id INTEGER REFERENCES rooms(id) ON DELETE SET NULL;"))
            db.session.commit()
            print("Added room_id column to equipment")
        except Exception as e:
            db.session.rollback()
            print("room_id might already exist or error:", e)

        print("Migrating existing equipment locations...")
        
        # 1. Create default Building
        main_building = Building.query.filter_by(name="อาคารหลัก").first()
        if not main_building:
            main_building = Building(name="อาคารหลัก")
            db.session.add(main_building)
            db.session.commit()
            print("Created default building")

        equipments = Equipment.query.all()
        migrated_count = 0
        
        for eq in equipments:
            room_name = None
            floor_name = str(eq.floor) if eq.floor else "ไม่ระบุ"
            
            # Parse room from description e.g. "ห้อง 231"
            match = re.search(r'ห้อง\s*(\w+)', eq.description)
            if match:
                room_name = match.group(1)
            
            if not room_name and eq.floor == 0:
                continue # Skip if no clear room or floor
                
            if not room_name:
                room_name = "ทั่วไป"
            
            # Find or Create Floor
            floor = Floor.query.filter_by(name=floor_name, building_id=main_building.id).first()
            if not floor:
                floor = Floor(name=floor_name, building_id=main_building.id)
                db.session.add(floor)
                db.session.commit()
                
            # Find or Create Room
            room = Room.query.filter_by(name=room_name, floor_id=floor.id).first()
            if not room:
                room = Room(name=room_name, floor_id=floor.id)
                db.session.add(room)
                db.session.commit()
                
            # Update Equipment
            eq.room_id = room.id
            migrated_count += 1
            
        db.session.commit()
        print(f"Migration completed. Updated {migrated_count} items with room_id.")

if __name__ == "__main__":
    run_migration()
