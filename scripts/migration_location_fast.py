from app import app
from models import db, Building, Floor, Room, Equipment
from sqlalchemy import text
import re

def run_migration():
    with app.app_context():
        print("Starting migration (optimized)...")
        
        main_building = Building.query.filter_by(name="อาคารหลัก").first()
        if not main_building:
            main_building = Building(name="อาคารหลัก")
            db.session.add(main_building)
            db.session.commit()
            print("Created default building")

        equipments = Equipment.query.all()
        
        # Cache to prevent DB lookups
        floors_cache = {}
        rooms_cache = {}
        
        # Load existing floors/rooms
        for f in Floor.query.all():
            floors_cache[f.name] = f
        for r in Room.query.all():
            rooms_cache[f"{r.name}_{r.floor_id}"] = r
            
        migrated_count = 0
        
        for eq in equipments:
            room_name = None
            floor_name = str(eq.floor) if eq.floor else "ไม่ระบุ"
            
            match = re.search(r'ห้อง\s*(\w+)', eq.description)
            if match:
                room_name = match.group(1)
            
            if not room_name and eq.floor == 0:
                continue
                
            if not room_name:
                room_name = "ทั่วไป"
            
            # Get or create floor
            if floor_name not in floors_cache:
                new_floor = Floor(name=floor_name, building_id=main_building.id)
                db.session.add(new_floor)
                db.session.commit() # need ID
                floors_cache[floor_name] = new_floor
                
            floor = floors_cache[floor_name]
            
            # Get or create room
            cache_key = f"{room_name}_{floor.id}"
            if cache_key not in rooms_cache:
                new_room = Room(name=room_name, floor_id=floor.id)
                db.session.add(new_room)
                db.session.commit() # need ID
                rooms_cache[cache_key] = new_room
                
            room = rooms_cache[cache_key]
            
            # Set room
            eq.room_id = room.id
            migrated_count += 1
            
        db.session.commit()
        print(f"Migration completed. Updated {migrated_count} items with room_id.")

if __name__ == "__main__":
    run_migration()
