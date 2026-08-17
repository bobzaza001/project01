from app import app, db
from models import Equipment

with app.app_context():
    eqs = Equipment.query.all()
    for eq in eqs:
        print(f"{eq.id}: {eq.name} ({eq.category}) -> {eq.image_filename}")
