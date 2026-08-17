from app import app
from models import db
from sqlalchemy import text

with app.app_context():
    columns = [
        ("equipment", "item_type", "VARCHAR(20) DEFAULT 'durable'"),
        ("borrow_requests", "borrow_days", "INTEGER DEFAULT 3"),
        ("borrow_requests", "quantity", "INTEGER DEFAULT 1"),
        ("borrow_requests", "damage_status", "VARCHAR(20) DEFAULT 'normal'"),
        ("borrow_requests", "damage_note", "TEXT DEFAULT ''"),
        ("borrow_requests", "return_image_filename", "VARCHAR(255) DEFAULT ''"),
        ("borrow_requests", "overdue_notified", "BOOLEAN DEFAULT FALSE"),
        ("users", "profile_image", "VARCHAR(255) DEFAULT ''"),
        ("users", "created_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"),
        ("equipment", "category", "VARCHAR(100) DEFAULT 'ทั่วไป'"),
        ("equipment", "room_id", "INTEGER REFERENCES rooms(id)"),
        ("equipment", "is_borrowable", "BOOLEAN DEFAULT TRUE"),
        ("equipment", "floor", "INTEGER DEFAULT 0"),
    ]
    
    for table, col, col_type in columns:
        try:
            db.session.execute(text(f'ALTER TABLE {table} ADD COLUMN {col} {col_type};'))
            db.session.commit()
            print(f"✅ Added {table}.{col}")
        except Exception as e:
            db.session.rollback()
            if 'already exists' in str(e).lower() or 'duplicate' in str(e).lower():
                print(f"⏩ {table}.{col} already exists, skipping.")
            else:
                print(f"❌ Error adding {table}.{col}: {e}")
    
    print("\nDone!")
