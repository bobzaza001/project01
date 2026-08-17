from app import app
from models import db
from sqlalchemy import text

with app.app_context():
    try:
        db.session.execute(text("ALTER TABLE equipment ADD COLUMN floor INTEGER DEFAULT 0;"))
        db.session.commit()
        print("✅ Added equipment.floor")
    except Exception as e:
        db.session.rollback()
        print(f"Error (might already exist): {e}")
