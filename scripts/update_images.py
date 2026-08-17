import os
import shutil
from app import app, db
from models import Equipment

brain_dir = r"C:\Users\ACER\.gemini\antigravity\brain\b500e698-6452-4be9-bee4-08259588db82"
upload_dir = r"d:\equipment test\static\uploads"

os.makedirs(upload_dir, exist_ok=True)

images = [
    "camera_canon_eos_1784115045495.jpg",
    "ipad_pro_1784115036139.jpg",
    "laptop_dell_xps13_1784115016570.jpg",
    "projector_epson_1784115026548.jpg"
]

for img in images:
    src = os.path.join(brain_dir, img)
    dst = os.path.join(upload_dir, img)
    if os.path.exists(src):
        shutil.copy(src, dst)

with app.app_context():
    # 1. Clear all existing images
    Equipment.query.update({Equipment.image_filename: ''})
    
    # 2. Assign real images
    # Camera
    eq_cam = Equipment.query.get(1576)
    if eq_cam:
        eq_cam.image_filename = "camera_canon_eos_1784115045495.jpg"
        
    # Projector
    eq_proj = Equipment.query.get(1734)
    if eq_proj:
        eq_proj.image_filename = "projector_epson_1784115026548.jpg"
        
    # Laptop (update item to match)
    eq_lap = Equipment.query.get(1607)
    if eq_lap:
        eq_lap.name = "Notebook Dell XPS 13"
        eq_lap.category = "ไอทีและคอมพิวเตอร์"
        eq_lap.image_filename = "laptop_dell_xps13_1784115016570.jpg"
        
    # iPad (update item to match)
    eq_ipad = Equipment.query.get(1608)
    if eq_ipad:
        eq_ipad.name = "Apple iPad Pro 11-inch"
        eq_ipad.category = "ไอทีและคอมพิวเตอร์"
        eq_ipad.image_filename = "ipad_pro_1784115036139.jpg"
        
    db.session.commit()
    print("Database updated successfully.")
