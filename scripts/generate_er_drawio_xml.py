import xml.etree.ElementTree as ET
import os

def create_er_xml():
    # Set dark background draw.io template matching dark Glassmorphism theme
    mxfile = ET.Element('mxfile', host="Electron", modified="2026-08-20T18:11:17.000Z", agent="Antigravity", version="20.0.0")
    diagram = ET.SubElement(mxfile, 'diagram', id="Page-1", name="Page-1")
    mxGraphModel = ET.SubElement(diagram, 'mxGraphModel', dx="1400", dy="1200", grid="1", gridSize="10", guides="1", tooltips="1", connect="1", arrows="1", fold="1", page="1", pageScale="1", pageWidth="1200", pageHeight="1000", background="#1a1a1e", math="0", shadow="0")
    root = ET.SubElement(mxGraphModel, 'root')
    
    # Base cells
    ET.SubElement(root, 'mxCell', id="0")
    ET.SubElement(root, 'mxCell', id="1", parent="0")

    # Node styles (DFD Standard Elements in Dark Theme)
    style_user = "swimlane;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=26;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;fillColor=#1e1e24;strokeColor=#38bdf8;fontColor=#ffffff;strokeWidth=2;"
    style_borrow = "swimlane;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=26;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;fillColor=#1e1e24;strokeColor=#0ea5e9;fontColor=#ffffff;strokeWidth=2;"
    style_equip = "swimlane;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=26;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;fillColor=#1e1e24;strokeColor=#38bdf8;fontColor=#ffffff;strokeWidth=2;"
    style_repair = "swimlane;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=26;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;fillColor=#1e1e24;strokeColor=#ef4444;fontColor=#ffffff;strokeWidth=2;"
    style_location = "swimlane;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=26;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;fillColor=#1e1e24;strokeColor=#8b5cf6;fontColor=#ffffff;strokeWidth=2;"
    
    style_row = "text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontColor=#ffffff;fontSize=10;"
    style_line = "edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#a1a1aa;strokeWidth=1.5;fontColor=#e4e4e7;fontSize=9;endArrow=classic;endFill=1;startArrow=oval;startFill=0;"
    style_line_dashed = "edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#f43f5e;strokeWidth=1.5;fontColor=#e4e4e7;fontSize=9;endArrow=classic;endFill=1;startArrow=oval;startFill=0;dashed=1;"

    # Add Vertices (Entities)
    # Helper to create tables with columns
    def add_table(tid, name, x, y, w, h, attrs, style):
        table = ET.SubElement(root, 'mxCell', id=tid, value=name, style=style, vertex="1", parent="1")
        geom = ET.SubElement(table, 'mxGeometry', x=str(x), y=str(y), width=str(w), height=str(h))
        geom.set('as', 'geometry')
        
        # Add rows
        for idx, attr in enumerate(attrs):
            row_id = f"{tid}_row_{idx}"
            row = ET.SubElement(root, 'mxCell', id=row_id, value=attr, style=style_row, vertex="1", parent=tid)
            # Row geometry inside parent table
            rgeom = ET.SubElement(row, 'mxGeometry', y=str(26 + (idx * 20)), width=str(w), height="20")
            rgeom.set('as', 'geometry')

    # 1. User
    add_table("user", "User (ผู้ใช้)", 60, 100, 220, 190, [
        "PK: id (INT)",
        "username (VARCHAR)",
        "full_name (VARCHAR)",
        "email (VARCHAR)",
        "password_hash (VARCHAR)",
        "role (VARCHAR)",
        "profile_image (VARCHAR)",
        "created_at (DATETIME)"
    ], style_user)

    # 2. BorrowRequest
    add_table("borrow", "BorrowRequest (การยืม)", 490, 100, 220, 330, [
        "PK: id (INT)",
        "FK: user_id (INT)",
        "FK: equipment_id (INT)",
        "status (VARCHAR)",
        "requested_at (DATETIME)",
        "borrow_datetime (DATETIME)",
        "return_due_datetime (DATETIME)",
        "returned_at (DATETIME)",
        "borrow_days (INT)",
        "quantity (INT)",
        "damage_status (VARCHAR)",
        "damage_note (TEXT)",
        "return_image_filename (VARCHAR)",
        "warning_message (TEXT)",
        "overdue_notified (BOOLEAN)"
    ], style_borrow)

    # 3. Equipment
    add_table("equip", "Equipment (ครุภัณฑ์)", 920, 100, 220, 270, [
        "PK: id (INT)",
        "FK: room_id (INT)",
        "equipment_code (VARCHAR)",
        "name (VARCHAR)",
        "description (TEXT)",
        "category (VARCHAR)",
        "image_filename (VARCHAR)",
        "status (VARCHAR)",
        "total_quantity (INT)",
        "available_quantity (INT)",
        "item_type (VARCHAR)",
        "is_borrowable (BOOLEAN)"
    ], style_equip)

    # 4. RepairRequest
    add_table("repair", "RepairRequest (แจ้งซ่อม)", 490, 560, 220, 190, [
        "PK: id (INT)",
        "FK: user_id (INT)",
        "FK: equipment_id (INT)",
        "issue_description (TEXT)",
        "status (VARCHAR)",
        "reported_at (DATETIME)",
        "resolved_at (DATETIME)",
        "admin_note (TEXT)"
    ], style_repair)

    # 5. Room
    add_table("room", "Room (ห้อง)", 920, 560, 220, 90, [
        "PK: id (INT)",
        "FK: floor_id (INT)",
        "name (VARCHAR)"
    ], style_location)

    # 6. Floor
    add_table("floor", "Floor (ชั้น)", 920, 780, 220, 90, [
        "PK: id (INT)",
        "FK: building_id (INT)",
        "name (VARCHAR)"
    ], style_location)

    # 7. Building
    add_table("building", "Building (อาคาร)", 490, 780, 220, 70, [
        "PK: id (INT)",
        "name (VARCHAR)"
    ], style_location)

    # Add Edges (Lines & DFD Relationships)
    edge_idx = 300
    def add_relation(source, target, label, start_lbl="1", end_lbl="N", style=style_line):
        nonlocal edge_idx
        edge = ET.SubElement(root, 'mxCell', id=f"edge_{edge_idx}", value=label, style=style, edge="1", parent="1", source=source, target=target)
        geom = ET.SubElement(edge, 'mxGeometry', relative="1")
        geom.set('as', 'geometry')
        edge_idx += 1

    # Connect nodes
    add_relation("user", "borrow", "ยื่นคำขอ")
    add_relation("equip", "borrow", "ถูกยืม")
    add_relation("user", "repair", "แจ้งปัญหา", style=style_line_dashed)
    add_relation("equip", "repair", "ชำรุด", style=style_line_dashed)
    add_relation("room", "equip", "เก็บอยู่ที่")
    add_relation("floor", "room", "สังกัด")
    add_relation("building", "floor", "ตั้งอยู่ใน")

    # Save to XML file
    xml_str = ET.tostring(mxfile, encoding='utf-8')
    out_dir = "scratch"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "er_diagram_drawio.xml")
    with open(out_path, "wb") as f:
        f.write(xml_str)
    
    # Copy to static and brain directories
    shutil_path_local = "static/img/diagrams/er_diagram_drawio.xml"
    shutil_path_brain = "C:/Users/ACER/.gemini/antigravity/brain/b500e698-6452-4be9-bee4-08259588db82/er_diagram_drawio.xml"
    
    import shutil
    shutil.copy(out_path, shutil_path_local)
    shutil.copy(out_path, shutil_path_brain)
    
    print(f"Generated draw.io XML for ER Diagram successfully at: {out_path}")

if __name__ == "__main__":
    create_er_xml()
