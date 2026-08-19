from app import app
from models import db, User, Equipment, BorrowRequest, Building, Floor, Room, RepairRequest

def fetch_supabase_data():
    with app.app_context():
        print("=== 1. USERS DATA ===")
        users = User.query.limit(5).all()
        for u in users:
            print(f"ID: {u.id} | User: {u.username} | Name: {u.full_name} | Role: {u.role} | Email: {u.email}")
            
        print("\n=== 2. BUILDINGS DATA ===")
        buildings = Building.query.limit(5).all()
        for b in buildings:
            print(f"ID: {b.id} | Name: {b.name}")
            
        print("\n=== 3. FLOORS DATA ===")
        floors = Floor.query.limit(5).all()
        for f in floors:
            print(f"ID: {f.id} | Name: {f.name} | Bldg ID: {f.building_id}")

        print("\n=== 4. ROOMS DATA ===")
        rooms = Room.query.limit(5).all()
        for r in rooms:
            print(f"ID: {r.id} | Name: {r.name} | Floor ID: {r.floor_id}")

        print("\n=== 5. EQUIPMENT DATA ===")
        eqs = Equipment.query.limit(5).all()
        for eq in eqs:
            print(f"ID: {eq.id} | Code: {eq.equipment_code} | Name: {eq.name} | Status: {eq.status} | Qty: {eq.total_quantity}")

        print("\n=== 6. BORROW REQUESTS DATA ===")
        reqs = BorrowRequest.query.limit(5).all()
        for req in reqs:
            print(f"ID: {req.id} | User ID: {req.user_id} | Eq ID: {req.equipment_id} | Status: {req.status} | Qty: {req.quantity}")

if __name__ == "__main__":
    fetch_supabase_data()
