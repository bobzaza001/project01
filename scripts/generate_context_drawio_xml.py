import xml.etree.ElementTree as ET
import os

def create_context_xml():
    # Set dark background draw.io template matching dark Glassmorphism theme
    mxfile = ET.Element('mxfile', host="Electron", modified="2026-08-20T16:06:37.000Z", agent="Antigravity", version="20.0.0")
    diagram = ET.SubElement(mxfile, 'diagram', id="Page-1", name="Page-1")
    mxGraphModel = ET.SubElement(diagram, 'mxGraphModel', dx="1200", dy="1000", grid="1", gridSize="10", guides="1", tooltips="1", connect="1", arrows="1", fold="1", page="1", pageScale="1", pageWidth="1000", pageHeight="800", background="#1a1a1e", math="0", shadow="0")
    root = ET.SubElement(mxGraphModel, 'root')
    
    # Base cells
    ET.SubElement(root, 'mxCell', id="0")
    ET.SubElement(root, 'mxCell', id="1", parent="0")

    # Node styles (DFD Standard Elements in Dark Theme)
    style_process = "ellipse;whiteSpace=wrap;html=1;fillColor=#1e1e24;strokeColor=#38bdf8;strokeWidth=3;fontColor=#ffffff;fontStyle=1;"
    style_entity = "rounded=0;whiteSpace=wrap;html=1;fillColor=#2b2d31;strokeColor=#3f4248;strokeWidth=2;fontColor=#ffffff;fontStyle=1;"
    style_edge = "edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#a1a1aa;strokeWidth=1.5;fontColor=#ffffff;fontSize=9;"
    style_edge_green = "edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#10b981;strokeWidth=1.5;fontColor=#ffffff;fontSize=9;"

    # Add Vertices
    # 1. Center System Process
    cell_sys = ET.SubElement(root, 'mxCell', id="sys", value="ระบบจัดการยืม-คืนครุภัณฑ์&#10;(LAB Equipment System)", style=style_process, vertex="1", parent="1")
    geom_sys = ET.SubElement(cell_sys, 'mxGeometry', x="375", y="280", width="250", height="160")
    geom_sys.set('as', 'geometry')

    # 2. General User Entity (Left)
    cell_user = ET.SubElement(root, 'mxCell', id="user", value="ผู้ใช้งานทั่วไป&#10;(นักศึกษา / อาจารย์)", style=style_entity, vertex="1", parent="1")
    geom_user = ET.SubElement(cell_user, 'mxGeometry', x="60", y="320", width="180", height="80")
    geom_user.set('as', 'geometry')

    # 3. Admin Entity (Right)
    cell_admin = ET.SubElement(root, 'mxCell', id="admin", value="ผู้ดูแลระบบ&#10;(Admin)", style=style_entity, vertex="1", parent="1")
    geom_admin = ET.SubElement(cell_admin, 'mxGeometry', x="760", y="320", width="180", height="80")
    geom_admin.set('as', 'geometry')

    # 4. SMTP Mail Server Entity (Top)
    cell_smtp = ET.SubElement(root, 'mxCell', id="smtp", value="ระบบส่งอีเมล&#10;(SMTP Mail Server)", style=style_entity, vertex="1", parent="1")
    geom_smtp = ET.SubElement(cell_smtp, 'mxGeometry', x="410", y="70", width="180", height="80")
    geom_smtp.set('as', 'geometry')

    # Add Edges (Lines & Data Flows)
    edge_idx = 200
    def add_data_flow(source, target, label, color="#a1a1aa", style_custom=None):
        nonlocal edge_idx
        style = style_custom if style_custom else f"edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor={color};strokeWidth=1.5;fontColor=#e4e4e7;fontSize=9;"
        edge = ET.SubElement(root, 'mxCell', id=f"edge_{edge_idx}", value=label, style=style, edge="1", parent="1", source=source, target=target)
        geom = ET.SubElement(edge, 'mxGeometry', relative="1")
        geom.set('as', 'geometry')
        edge_idx += 1

    # --- User -> System Flows ---
    add_data_flow("user", "sys", "1. ข้อมูลลงทะเบียน / ยึนยันตัวตน&#10;2. คำขอยืมครุภัณฑ์ / เบิกวัสดุ&#10;3. หลักฐานรูปถ่ายส่งคืนของ&#10;4. ข้อมูลใบแจ้งซ่อมครุภัณฑ์")
    
    # --- System -> User Flows ---
    # Draw curved/orthogonal routing below the other line
    add_data_flow("sys", "user", "1. ข้อมูลสถานะคลังครุภัณฑ์&#10;2. ประวัติและสถานะคำร้องยืมคืน")

    # --- Admin -> System Flows ---
    add_data_flow("admin", "sys", "1. ผลอนุมัติ / ปฏิเสธคำร้อง&#10;2. จัดการอุปกรณ์ (เพิ่ม/แก้/ลบ)&#10;3. จัดการผังสถานที่ (ตึก/ห้อง)")
    
    # --- System -> Admin Flows ---
    add_data_flow("sys", "admin", "1. รายการคำร้องที่รอการอนุมัติ&#10;2. รายงานข้อมูลวิเคราะห์สต็อก")

    # --- System -> SMTP Server Flows ---
    add_data_flow("sys", "smtp", "ส่งคำร้องขอประมวลผลเมลเตือน")

    # --- SMTP Server -> User Flows (Direct Green Arrow) ---
    add_data_flow("smtp", "user", "นำส่งอีเมลแจ้งผลการยืมคืน / แจ้งเตือนภัยส่งคืนล่าช้าด่วนดึก", color="#10b981")

    # Save to XML file
    xml_str = ET.tostring(mxfile, encoding='utf-8')
    out_dir = "scratch"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "context_diagram_drawio.xml")
    with open(out_path, "wb") as f:
        f.write(xml_str)
    
    # Copy to static and brain directories
    shutil_path_local = "static/img/diagrams/context_diagram_drawio.xml"
    shutil_path_brain = "C:/Users/ACER/.gemini/antigravity/brain/b500e698-6452-4be9-bee4-08259588db82/context_diagram_drawio.xml"
    
    import shutil
    shutil.copy(out_path, shutil_path_local)
    shutil.copy(out_path, shutil_path_brain)
    
    print(f"Generated draw.io XML for Context Diagram successfully at: {out_path}")

if __name__ == "__main__":
    create_context_xml()
