import pandas as pd
import math
from app import app
from models import db, Equipment, BorrowRequest

def clean_int(val):
    try:
        if pd.isna(val) or val == '-':
            return 0
        return int(float(str(val).replace(',', '')))
    except Exception:
        return 0

def import_data():
    file_path = "แบบการเก็บข้อมูลครุภัณฑ์แผนก (ปรับปรุง 20-03-2568).xlsx"
    print(f"Reading Excel file: {file_path}")
    
    xl = pd.ExcelFile(file_path)
    skip_sheets = ['ตัวอย่าง ชีตว่าง', 'ตัวอย่าง', 'Sheet1']
    
    with app.app_context():
        print("Clearing old data...")
        # ลบข้อมูลการยืมทั้งหมดก่อน (เพื่อไม่ให้ติด Foreign Key)
        BorrowRequest.query.delete()
        # ลบข้อมูลอุปกรณ์ทั้งหมด
        Equipment.query.delete()
        db.session.commit()
        print("Old data cleared.")
        
        added_count = 0
        
        for sheet in xl.sheet_names:
            if sheet in skip_sheets:
                continue
                
            print(f"Importing sheet: {sheet}")
            try:
                df = pd.read_excel(file_path, sheet_name=sheet, header=4)
                df.dropna(how='all', inplace=True)
                
                # กำหนดชื่อคอลัมน์ใหม่เพื่อให้อ้างอิงง่าย
                df.columns = [
                    'seq', 'name', 'total_qty', 'unit', 'available_qty', 
                    'broken_qty', 'remaining_qty', 'broken_reason', 
                    'broken_case', 'blank_1', 'remarks', 'image', 'extra1', 'extra2'
                ][:len(df.columns)]
                
                item_index = 1
                for index, row in df.iterrows():
                    name = str(row['name']).strip()
                    
                    # ถ้าชื่อเป็น nan หรือ ค่าว่าง ให้ข้าม
                    if pd.isna(row['name']) or name == 'nan' or name == '':
                        continue
                        
                    # บางครั้งหัวตารางที่อยู่ล่างๆ ก็หลุดมา
                    if 'รายการ' in name or 'รวม' in name:
                        continue
                        
                    total = clean_int(row['total_qty'])
                    available = clean_int(row.get('available_qty', total))
                    
                    eq_code = f"EQ-{sheet}-{item_index:03d}"
                    # === Logic จัดหมวดหมู่และรูปภาพ ===
                    name_lower = name.lower()
                    if any(kw in name_lower for kw in ['monitor', 'คอมพิวเตอร์', 'cpu', 'mouse', 'keyboard', 'switching', 'ตู้แร็ค']):
                        category = 'ไอทีและคอมพิวเตอร์'
                        image_filename = 'cat_it.jpg'
                    elif any(kw in name_lower for kw in ['เก้าอี้', 'โต๊ะ', 'ตู้เก็บของ', 'ตู้เอกสาร']):
                        category = 'เฟอร์นิเจอร์'
                        image_filename = 'cat_furniture.jpg'
                    elif any(kw in name_lower for kw in ['เครื่องปรับอากาศ', 'หลอดไฟ', 'ตู้ควบคุม', 'พัดลม']):
                        category = 'เครื่องใช้ไฟฟ้า'
                        image_filename = 'cat_electrical.jpg'
                    elif any(kw in name_lower for kw in ['ทีวี', 'กล้อง', 'ลำโพง', 'ไมค์', 'เพาเวอร์แอมป์', 'จอรับภาพ']):
                        category = 'โสตทัศนูปกรณ์'
                        image_filename = 'cat_av.jpg'
                    else:
                        category = 'ทั่วไป'
                        image_filename = 'cat_general.jpg'
                        
                    # === Logic ชั้นของอาคาร ===
                    if sheet.startswith('23'):
                        floor = 3
                    elif sheet.startswith('24'):
                        floor = 4
                    else:
                        floor = 0
                        
                    equipment = Equipment(
                        equipment_code=eq_code,
                        name=name,
                        description=f"ห้อง {sheet}",
                        category=category,
                        total_quantity=total,
                        available_quantity=available,
                        image_filename=image_filename,
                        floor=floor
                    )
                    
                    db.session.add(equipment)
                    added_count += 1
                    item_index += 1
                    
            except Exception as e:
                print(f"Error reading sheet {sheet}: {e}")
                
        db.session.commit()
        print(f"Import complete! Added {added_count} items to the database.")

if __name__ == '__main__':
    import_data()
