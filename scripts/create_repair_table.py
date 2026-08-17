from app import app, db
from models import RepairRequest

with app.app_context():
    db.create_all()
    print("RepairRequest table created successfully!")
