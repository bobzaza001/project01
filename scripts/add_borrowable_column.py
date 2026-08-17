from app import app
from models import db
from sqlalchemy import text

def update_database():
    with app.app_context():
        # 1. Add column if not exists
        try:
            db.session.execute(text("ALTER TABLE equipment ADD COLUMN is_borrowable BOOLEAN DEFAULT TRUE;"))
            db.session.commit()
            print("Added is_borrowable column.")
        except Exception as e:
            db.session.rollback()
            print(f"Column might already exist or error: {e}")
        
        # 2. Auto-categorize existing items
        # Set is_borrowable = False for items that match these keywords
        keywords = ['แอร์', 'ทีวี', 'จอ', 'Monitor', 'คอมพิวเตอร์', 'โต๊ะ', 'เก้าอี้', 'แร็ค', 'Rack', 'HUB', 'หลอดไฟ', 'ตู้ควบคุม', 'วงจรปิด']
        
        # Build SQL condition
        conditions = []
        for kw in keywords:
            conditions.append(f"name ILIKE '%{kw}%'")
            conditions.append(f"category ILIKE '%{kw}%'")
        
        where_clause = " OR ".join(conditions)
        
        try:
            result = db.session.execute(text(f"UPDATE equipment SET is_borrowable = FALSE WHERE {where_clause}"))
            db.session.commit()
            print(f"Updated {result.rowcount} items to is_borrowable = False")
        except Exception as e:
            db.session.rollback()
            print(f"Error updating rows: {e}")

if __name__ == "__main__":
    update_database()
