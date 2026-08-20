import xml.etree.ElementTree as ET
import os

def create_drawio_xml():
    # Set dark background draw.io template
    mxfile = ET.Element('mxfile', host="Electron", modified="2026-08-20T15:52:56.000Z", agent="Antigravity", version="20.0.0")
    diagram = ET.SubElement(mxfile, 'diagram', id="Page-1", name="Page-1")
    mxGraphModel = ET.SubElement(diagram, 'mxGraphModel', dx="1200", dy="1600", grid="1", gridSize="10", guides="1", tooltips="1", connect="1", arrows="1", fold="1", page="1", pageScale="1", pageWidth="1169", pageHeight="1600", background="#1a1a1e", math="0", shadow="0")
    root = ET.SubElement(mxGraphModel, 'root')
    
    # Base cells
    ET.SubElement(root, 'mxCell', id="0")
    ET.SubElement(root, 'mxCell', id="1", parent="0")

    # Node styles
    style_oval = "ellipse;whiteSpace=wrap;html=1;fillColor=#2b2d31;strokeColor=#3f4248;fontColor=#ffffff;fontStyle=1;"
    style_rect = "rounded=1;whiteSpace=wrap;html=1;fillColor=#1e1e24;strokeColor=#3f4248;fontColor=#ffffff;"
    style_rect_green = "rounded=1;whiteSpace=wrap;html=1;fillColor=#1e1e24;strokeColor=#10b981;fontColor=#ffffff;"
    style_rect_red = "rounded=1;whiteSpace=wrap;html=1;fillColor=#1e1e24;strokeColor=#f43f5e;fontColor=#ffffff;"
    style_diamond = "rhombus;whiteSpace=wrap;html=1;fillColor=#1e1e24;strokeColor=#f59e0b;fontColor=#ffffff;fontStyle=1;"

    # Dictionary of nodes with their positions (scaled for draw.io)
    # Map (X, Y) to draw.io coords: x = X * 60 + 50, y = (22 - Y) * 65 + 30
    nodes = {
        "start": ("เริ่มต้น", "oval", 9, 20.5, 120, 50),
        "login": ("เข้าสู่ระบบ Login\n(ระบุชื่อผู้ใช้/รหัสผ่าน)", "rect", 9, 19.3, 180, 60),
        "role_check": ("ตรวจสอบสิทธิ์การเข้าใช้?", "diamond", 9, 17.5, 160, 80),
        
        # Student Path
        "std_dash": ("หน้าจอคลังอุปกรณ์ Equipment List", "rect", 4.0, 15.6, 210, 60),
        "std_filter": ("ค้นหาและกรองอุปกรณ์ตามอาคาร ชั้น ห้อง\nหรือตามประเภทครุภัณฑ์/วัสดุ", "rect", 4.0, 14.2, 230, 60),
        "std_select": ("เลือกประเภทการทำรายการ?", "diamond", 4.0, 12.4, 160, 80),
        
        # Consumable Path
        "req_con": ("ยื่นคำขอเบิกวัสดุ\nConsumable", "rect", 1.5, 10.7, 160, 60),
        "con_approve": ("แอดมินอนุมัติ?", "diamond", 1.5, 9.2, 140, 70),
        "con_ok": ("หักจำนวนสะสมในคลัง\n(ไม่ต้องส่งคืน)", "rect_green", 0.7, 7.5, 140, 60),
        "con_rej": ("ระบบยกเลิกคำขอ /\nแจ้งปฏิเสธการเบิก", "rect_red", 2.3, 7.5, 140, 60),
        
        # Durable Path
        "req_dur": ("ยื่นคำขอยืมครุภัณฑ์ Durable\n(ระบุวันเวลายืม + จำนวนวัน)", "rect", 5.5, 10.7, 180, 60),
        "dur_approve": ("แอดมินอนุมัติ?", "diamond", 7.0, 9.2, 140, 70),
        "dur_rej": ("ส่งเมลแจ้งปฏิเสธ\n(Rejected Email)", "rect_red", 5.5, 7.5, 140, 60),
        "dur_ok": ("หักสต็อกพร้อมยืมชั่วคราว\nส่งเมลแจ้งผลอนุมัติ", "rect_green", 7.5, 7.5, 150, 60),
        "dur_use": ("ผู้ใช้รับอุปกรณ์ไปใช้งาน", "rect", 7.5, 6.3, 150, 50),
        "dur_return": ("แจ้งส่งคืนผ่านระบบ\nพร้อมอัปโหลดภาพหลักฐาน", "rect", 7.5, 5.1, 170, 60),
        "dur_return_check": ("แอดมินอนุมัติคืน?", "diamond", 7.5, 3.5, 140, 70),
        "dur_returned": ("บวกสต็อกกลับคืนคลัง\n(สถานะ: คืนเรียบร้อย)", "rect_green", 7.5, 2.0, 160, 60),
        
        # Admin Path
        "adm_dash": ("แดชบอร์ดแอดมิน\nAdmin Dashboard", "rect", 14.0, 15.6, 180, 60),
        "adm_action": ("เลือกการทำงาน?", "diamond", 14.0, 13.9, 140, 70),
        "adm_review": ("ตรวจสอบใบคำร้องยื่นยืม\nและ ตรวจรูปถ่ายสภาพการคืน", "rect", 11.0, 12.3, 180, 60),
        "adm_manage_eq": ("เพิ่ม / แก้ไข / ลบ\nข้อมูลอุปกรณ์และรูปภาพ", "rect", 12.2, 10.7, 150, 50),
        "adm_manage_loc": ("จัดการพิกัดห้องเรียน\n(อาคาร / ชั้น / ห้อง)", "rect", 14.8, 10.7, 150, 50),
        "adm_overdue": ("ส่งใบเตือนคืนของ\n(Overdue)", "rect", 17.0, 10.7, 140, 50),
        "adm_overdue_check": ("ค้างคืนครุภัณฑ์?", "diamond", 17.0, 9.2, 140, 70),
        "adm_warn_email": ("ส่งอีเมลเตือนด่วนสีแดง\n(ตรวจเช็คค้างส่งอัตโนมัติ)", "rect_red", 16.0, 7.5, 170, 60),
        
        # End
        "end": ("สิ้นสุดการทำงาน", "oval", 9.0, 0.8, 140, 50)
    }

    # Add vertices
    for nid, (text, ntype, gx, gy, w, h) in nodes.items():
        # Scale coordinates to fit draw.io viewport nicely
        x = int(gx * 65 + 10)
        y = int((22 - gy) * 65 - 20)
        
        style = style_oval
        if ntype == "rect":
            style = style_rect
        elif ntype == "rect_green":
            style = style_rect_green
        elif ntype == "rect_red":
            style = style_rect_red
        elif ntype == "diamond":
            style = style_diamond
            
        cell = ET.SubElement(root, 'mxCell', id=nid, value=text, style=style, vertex="1", parent="1")
        ET.SubElement(cell, 'mxGeometry', x=str(x), y=str(y), width=str(w), height=str(h), as_="geometry")

    # Helper function to add edges (lines) with straight orthogonal routing
    edge_idx = 100
    def add_edge(source, target, label="", color="#38bdf8"):
        nonlocal edge_idx
        style = f"edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor={color};strokeWidth=1.5;fontColor=#ffffff;fontSize=9;"
        edge = ET.SubElement(root, 'mxCell', id=f"edge_{edge_idx}", value=label, style=style, edge="1", parent="1", source=source, target=target)
        ET.SubElement(edge, 'mxGeometry', relative="1", as_="geometry")
        edge_idx += 1

    # Connect nodes
    add_edge("start", "login")
    add_edge("login", "role_check")
    add_edge("role_check", "std_dash", "นักศึกษา / อาจารย์")
    add_edge("role_check", "adm_dash", "ผู้ดูแลระบบ (Admin)")
    
    # Student path
    add_edge("std_dash", "std_filter")
    add_edge("std_filter", "std_select")
    add_edge("std_select", "req_con", "เบิกวัสดุ")
    add_edge("std_select", "req_dur", "ยืมครุภัณฑ์")
    
    # Consumable
    add_edge("req_con", "con_approve")
    add_edge("con_approve", "con_ok", "อนุมัติ")
    add_edge("con_approve", "con_rej", "ปฏิเสธ")
    add_edge("con_ok", "end")
    add_edge("con_rej", "end")
    
    # Durable
    add_edge("req_dur", "dur_approve")
    add_edge("dur_approve", "dur_ok", "อนุมัติ")
    add_edge("dur_approve", "dur_rej", "ปฏิเสธ")
    add_edge("dur_rej", "end")
    
    add_edge("dur_ok", "dur_use")
    add_edge("dur_use", "dur_return")
    add_edge("dur_return", "dur_return_check")
    add_edge("dur_return_check", "dur_returned", "ยืนยันรับคืน")
    add_edge("dur_return_check", "dur_return", "ไม่อนุมัติคืน (แก้ไข)", color="#f43f5e")
    add_edge("dur_returned", "end")
    
    # Admin path
    add_edge("adm_dash", "adm_action")
    add_edge("adm_action", "adm_review", "อนุมัติยืม-คืน")
    add_edge("adm_action", "adm_manage_eq", "จัดเก็บคลัง")
    add_edge("adm_action", "adm_manage_loc", "พิกัดห้อง")
    add_edge("adm_action", "adm_overdue", "เตือนส่งคืน")
    
    # Admin review feedback loops to student diamonds
    add_edge("adm_review", "dur_approve")
    add_edge("adm_review", "dur_return_check")
    
    # Overdue checks
    add_edge("adm_overdue", "adm_overdue_check")
    add_edge("adm_overdue_check", "adm_warn_email", "เกินกำหนด")
    add_edge("adm_overdue_check", "end", "ปกติ")
    
    add_edge("adm_manage_eq", "end")
    add_edge("adm_manage_loc", "end")
    add_edge("adm_warn_email", "end")

    # Write to XML file
    xml_str = ET.tostring(mxfile, encoding='utf-8')
    # Save file
    out_dir = "scratch"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "system_flowchart_drawio.xml")
    with open(out_path, "wb") as f:
        f.write(xml_str)
    print(f"Generated draw.io XML file successfully at: {out_path}")

if __name__ == "__main__":
    create_drawio_xml()
