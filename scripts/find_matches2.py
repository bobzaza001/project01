from app import app, db
from models import Equipment

with app.app_context():
    # Search for potential matches for our 4 images
    keywords = ['Dell', 'Apple', 'Mac']
    for kw in keywords:
        matches = Equipment.query.filter(Equipment.name.ilike(f'%{kw}%')).limit(3).all()
        print(f"--- Matches for '{kw}' ---")
        for m in matches:
            print(f"{m.id}: {m.name} ({m.category})")
