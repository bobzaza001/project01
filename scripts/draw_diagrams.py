import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Set Thai Font
plt.rcParams['font.family'] = 'Tahoma'  # Tahoma is standard on Windows and supports Thai
plt.rcParams['figure.facecolor'] = '#f8fafc'
plt.rcParams['axes.facecolor'] = '#f8fafc'

# Create output directories
os.makedirs("static/img/diagrams", exist_ok=True)
os.makedirs("C:/Users/ACER/.gemini/antigravity/brain/b500e698-6452-4be9-bee4-08259588db82", exist_ok=True)

def save_fig(fig, filename):
    # Save both locally and to the brain artifacts directory
    local_path = os.path.join("static/img/diagrams", filename)
    artifact_path = os.path.join("C:/Users/ACER/.gemini/antigravity/brain/b500e698-6452-4be9-bee4-08259588db82", filename)
    fig.savefig(local_path, bbox_inches='tight', dpi=300)
    fig.savefig(artifact_path, bbox_inches='tight', dpi=300)
    print(f" Saved: {local_path} and {artifact_path}")

# ==========================================
# 1. Context Diagram
# ==========================================
def draw_context_diagram():
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')

    # Styles
    box_color = '#ffffff'
    border_color = '#0284c7'
    text_color = '#0f172a'
    line_color = '#475569'

    # Title
    ax.text(5, 7.5, "แผนภาพบริบท (Context Diagram) - LAB Equipment System", 
            ha='center', va='center', fontsize=14, weight='bold', color='#1e3a8a')

    # Center Process (System)
    rect_sys = patches.FancyBboxPatch((3.5, 3.0), 3.0, 2.0, boxstyle="round,pad=0.2",
                                      fc='#0ea5e9', ec='#0284c7', zorder=2)
    ax.add_patch(rect_sys)
    ax.text(5, 4.0, "ระบบจัดการยืม-คืนครุภัณฑ์\n(LAB Equipment System)", 
            ha='center', va='center', color='white', weight='bold', fontsize=11)

    # Entities
    # 1. User
    rect_user = patches.FancyBboxPatch((0.5, 3.25), 1.8, 1.5, boxstyle="round,pad=0.1",
                                       fc=box_color, ec='#0f172a', zorder=2)
    ax.add_patch(rect_user)
    ax.text(1.4, 4.0, "ผู้ใช้งานทั่วไป\n(นักศึกษา / อาจารย์)", 
            ha='center', va='center', color=text_color, weight='bold', fontsize=10)

    # 2. Admin
    rect_admin = patches.FancyBboxPatch((7.7, 3.25), 1.8, 1.5, boxstyle="round,pad=0.1",
                                        fc=box_color, ec='#0f172a', zorder=2)
    ax.add_patch(rect_admin)
    ax.text(8.6, 4.0, "ผู้ดูแลระบบ\n(Admin)", 
            ha='center', va='center', color=text_color, weight='bold', fontsize=10)

    # 3. SMTP Mail Server
    rect_smtp = patches.FancyBboxPatch((4.0, 5.8), 2.0, 1.0, boxstyle="round,pad=0.1",
                                       fc=box_color, ec='#10b981', zorder=2)
    ax.add_patch(rect_smtp)
    ax.text(5.0, 6.3, "ระบบส่งอีเมล\n(SMTP Mail Server)", 
            ha='center', va='center', color=text_color, weight='bold', fontsize=10)

    # Data Flows (Arrows)
    # User -> System
    ax.annotate("", xy=(3.3, 4.3), xytext=(2.4, 4.3),
                arrowprops=dict(arrowstyle="->", color=line_color, lw=1.5))
    ax.text(2.85, 4.45, "1. ยื่นคำขอยืม/เบิก\n2. ส่งคืนครุภัณฑ์ + แนบรูปภาพ", 
            ha='right', va='bottom', fontsize=8, color='#475569')

    # System -> User
    ax.annotate("", xy=(2.4, 3.7), xytext=(3.3, 3.7),
                arrowprops=dict(arrowstyle="->", color=line_color, lw=1.5))
    ax.text(2.85, 3.55, "1. อีเมลแจ้งอนุมัติ/ปฏิเสธ\n2. เมลเตือนคืนด่วน", 
            ha='right', va='top', fontsize=8, color='#475569')

    # Admin -> System
    ax.annotate("", xy=(6.9, 4.3), xytext=(7.6, 4.3),
                arrowprops=dict(arrowstyle="<-", color=line_color, lw=1.5))
    ax.text(7.25, 4.45, "1. อนุมัติ/ปฏิเสธคำขอ\n2. จัดการข้อมูลครุภัณฑ์/สถานที่", 
            ha='left', va='bottom', fontsize=8, color='#475569')

    # System -> Admin
    ax.annotate("", xy=(7.6, 3.7), xytext=(6.9, 3.7),
                arrowprops=dict(arrowstyle="<-", color=line_color, lw=1.5))
    ax.text(7.25, 3.55, "1. ข้อมูลรายงานสถิติ\n2. รายการร้องขอยืม-คืน", 
            ha='left', va='top', fontsize=8, color='#475569')

    # System -> SMTP Server
    ax.annotate("", xy=(4.7, 5.7), xytext=(4.7, 5.2),
                arrowprops=dict(arrowstyle="->", color=line_color, lw=1.5))
    ax.text(4.6, 5.45, "คำขอส่งเมล", ha='right', va='center', fontsize=8, color='#475569')

    # SMTP Server -> User
    ax.annotate("", xy=(1.4, 4.95), xytext=(3.9, 6.3),
                arrowprops=dict(arrowstyle="->", color='#10b981', lw=1.2, connectionstyle="arc3,rad=0.2"))
    ax.text(2.3, 5.9, "ส่งอีเมลแจ้งเตือนถึงผู้ใช้", ha='center', va='bottom', fontsize=8, color='#10b981', rotation=20)

    save_fig(fig, "context_diagram.png")
    plt.close(fig)

# ==========================================
# 2. ER Diagram
# ==========================================
def draw_er_diagram():
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Title
    ax.text(6, 9.5, "แผนภาพความสัมพันธ์ข้อมูล (ER Diagram)", 
            ha='center', va='center', fontsize=14, weight='bold', color='#1e3a8a')

    # Draw Entities
    def draw_entity(x, y, name, attrs, color='#1e3a8a'):
        # Entity Box
        h = 0.5 + (len(attrs) * 0.25)
        rect = patches.FancyBboxPatch((x, y-h), 2.2, h, boxstyle="round,pad=0.05",
                                      fc='#ffffff', ec=color, lw=2, zorder=3)
        ax.add_patch(rect)
        # Header Box
        header_rect = patches.FancyBboxPatch((x, y-0.45), 2.2, 0.45, boxstyle="round,pad=0.05",
                                             fc=color, ec=color, zorder=3)
        ax.add_patch(header_rect)
        ax.text(x+1.1, y-0.22, name, ha='center', va='center', color='white', weight='bold', fontsize=9, zorder=4)
        
        # Attributes
        for i, attr in enumerate(attrs):
            ax.text(x+0.1, y-0.7-(i*0.25), attr, ha='left', va='center', fontsize=8, color='#334155', zorder=4)

    # 1. User
    draw_entity(0.5, 8.5, "User (ผู้ใช้)", ["PK: id (INT)", "username (VARCHAR)", "full_name (VARCHAR)", "email (VARCHAR)", "password_hash (VARCHAR)", "role (VARCHAR)", "created_at (DATETIME)"], '#1e3a8a')
    
    # 2. BorrowRequest
    draw_entity(4.8, 8.5, "BorrowRequest (การยืม)", ["PK: id (INT)", "FK: user_id (INT)", "FK: equipment_id (INT)", "status (VARCHAR)", "requested_at (DATETIME)", "borrow_datetime (DATETIME)", "return_due_datetime (DATETIME)", "returned_at (DATETIME)", "quantity (INT)", "return_image_filename (VARCHAR)", "overdue_notified (BOOLEAN)"], '#0ea5e9')

    # 3. Equipment
    draw_entity(9.3, 8.5, "Equipment (ครุภัณฑ์)", ["PK: id (INT)", "FK: room_id (INT)", "equipment_code (VARCHAR)", "name (VARCHAR)", "category (VARCHAR)", "status (VARCHAR)", "quantity (INT)", "available_quantity (INT)", "item_type (VARCHAR)", "is_borrowable (BOOLEAN)"], '#1e3a8a')

    # 4. RepairRequest
    draw_entity(4.8, 4.5, "RepairRequest (แจ้งซ่อม)", ["PK: id (INT)", "FK: user_id (INT)", "FK: equipment_id (INT)", "description (TEXT)", "status (VARCHAR)", "reported_at (DATETIME)", "resolved_at (DATETIME)", "admin_note (TEXT)"], '#ef4444')

    # 5. Room
    draw_entity(9.3, 4.5, "Room (ห้อง)", ["PK: id (INT)", "FK: floor_id (INT)", "name (VARCHAR)"], '#8b5cf6')

    # 6. Floor
    draw_entity(9.3, 2.2, "Floor (ชั้น)", ["PK: id (INT)", "FK: building_id (INT)", "name (VARCHAR)"], '#8b5cf6')

    # 7. Building
    draw_entity(5.5, 2.2, "Building (อาคาร)", ["PK: id (INT)", "name (VARCHAR)"], '#8b5cf6')

    # Draw Relationships (Lines with labels)
    def draw_line(x1, y1, x2, y2, label_start, label_end, text="", style='-'):
        ax.plot([x1, x2], [y1, y2], color='#475569', lw=1.2, linestyle=style, zorder=2)
        ax.text(x1, y1, label_start, fontsize=9, color='#0284c7', ha='center', va='center', weight='bold', bbox=dict(facecolor='white', edgecolor='none', pad=1))
        ax.text(x2, y2, label_end, fontsize=9, color='#0284c7', ha='center', va='center', weight='bold', bbox=dict(facecolor='white', edgecolor='none', pad=1))
        if text:
            ax.text((x1+x2)/2, (y1+y2)/2, text, fontsize=8, color='#64748b', ha='center', va='center', backgroundcolor='white')

    # User (1) -- (N) BorrowRequest
    draw_line(2.8, 7.8, 4.7, 7.8, "1", "N", "ยื่นคำขอ")
    
    # Equipment (1) -- (N) BorrowRequest
    draw_line(9.2, 7.8, 7.1, 7.8, "1", "N", "ถูกยืม")

    # User (1) -- (N) RepairRequest
    draw_line(2.8, 6.8, 4.7, 4.0, "1", "N", "แจ้งปัญหา", style='--')

    # Equipment (1) -- (N) RepairRequest
    draw_line(10.4, 5.7, 7.1, 4.0, "1", "N", "ชำรุด", style='--')

    # Room (1) -- (N) Equipment
    draw_line(10.4, 4.6, 10.4, 5.8, "1", "N", "เก็บอยู่ที่")

    # Floor (1) -- (N) Room
    draw_line(10.4, 2.3, 10.4, 3.5, "1", "N", "สังกัด")

    # Building (1) -- (N) Floor
    draw_line(7.8, 1.8, 9.2, 1.8, "1", "N", "ตั้งอยู่ใน")

    save_fig(fig, "er_diagram.png")
    plt.close(fig)

# ==========================================
# 3. System Flowchart
# ==========================================
def draw_system_flowchart():
    fig, ax = plt.subplots(figsize=(10, 12))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis('off')

    # Title
    ax.text(5, 11.5, "แผนภาพขั้นตอนการทำงานของระบบ (System Flowchart)", 
            ha='center', va='center', fontsize=14, weight='bold', color='#1e3a8a')

    # Draw Flowchart Elements
    # 1. Start (Oval)
    ellipse_start = patches.Ellipse((5, 10.5), 1.5, 0.6, fc='#f1f5f9', ec='#475569', lw=1.5)
    ax.add_patch(ellipse_start)
    ax.text(5, 10.5, "เริ่มต้น (Start)", ha='center', va='center', weight='bold', fontsize=9)

    # Arrow 1
    ax.annotate("", xy=(5, 9.6), xytext=(5, 10.2), arrowprops=dict(arrowstyle="->", color='#475569', lw=1.2))

    # 2. Login (Rectangle)
    rect_login = patches.FancyBboxPatch((4.0, 9.0), 2.0, 0.6, boxstyle="round,pad=0.05", fc='#ffffff', ec='#0ea5e9', lw=1.5)
    ax.add_patch(rect_login)
    ax.text(5, 9.3, "เข้าสู่ระบบ (Login)\n(ระบุรหัสประจำตัว)", ha='center', va='center', fontsize=9)

    # Arrow 2
    ax.annotate("", xy=(5, 8.1), xytext=(5, 8.9), arrowprops=dict(arrowstyle="->", color='#475569', lw=1.2))

    # 3. Check Role (Diamond)
    # Draw Diamond
    diamond_pts = [[5, 8.0], [6.2, 7.3], [5, 6.6], [3.8, 7.3]]
    polygon_role = patches.Polygon(diamond_pts, closed=True, fc='#fffbeb', ec='#d97706', lw=1.5)
    ax.add_patch(polygon_role)
    ax.text(5, 7.3, "สิทธิ์การเข้าใช้?", ha='center', va='center', fontsize=8, weight='bold')

    # Arrow left (User Path)
    ax.annotate("", xy=(2.5, 7.3), xytext=(3.7, 7.3), arrowprops=dict(arrowstyle="->", color='#475569', lw=1.2))
    ax.text(3.1, 7.45, "นักศึกษา/อาจารย์", ha='center', va='bottom', fontsize=8, color='#475569')

    # Arrow right (Admin Path)
    ax.annotate("", xy=(7.5, 7.3), xytext=(6.3, 7.3), arrowprops=dict(arrowstyle="->", color='#475569', lw=1.2))
    ax.text(6.9, 7.45, "ผู้ดูแลระบบ (Admin)", ha='center', va='bottom', fontsize=8, color='#475569')

    # --- User Path ---
    # 4. View Equipment (Rectangle)
    rect_view = patches.FancyBboxPatch((1.5, 5.8), 2.0, 0.6, boxstyle="round,pad=0.05", fc='#ffffff', ec='#1e3a8a', lw=1.2)
    ax.add_patch(rect_view)
    ax.text(2.5, 6.1, "ดูคลังครุภัณฑ์/ค้นหา\n(กรองประเภท/สถานที่)", ha='center', va='center', fontsize=8)

    # Arrow User 1
    ax.annotate("", xy=(2.5, 4.9), xytext=(2.5, 5.7), arrowprops=dict(arrowstyle="->", color='#475569', lw=1.2))

    # 5. Submit Request (Rectangle)
    rect_req = patches.FancyBboxPatch((1.5, 4.1), 2.0, 0.7, boxstyle="round,pad=0.05", fc='#ffffff', ec='#1e3a8a', lw=1.2)
    ax.add_patch(rect_req)
    ax.text(2.5, 4.45, "ยื่นขอยืม (Durable)\nหรือเบิกวัสดุ (Consumable)", ha='center', va='center', fontsize=8)

    # Arrow User 2
    ax.annotate("", xy=(2.5, 3.1), xytext=(2.5, 4.0), arrowprops=dict(arrowstyle="->", color='#475569', lw=1.2))

    # 6. Check Status (Diamond)
    diamond_pts_u = [[2.5, 3.0], [3.5, 2.4], [2.5, 1.8], [1.5, 2.4]]
    polygon_status = patches.Polygon(diamond_pts_u, closed=True, fc='#fffbeb', ec='#d97706', lw=1.2)
    ax.add_patch(polygon_status)
    ax.text(2.5, 2.4, "แอดมินอนุมัติ?", ha='center', va='center', fontsize=8, weight='bold')

    # Arrow User No (Rejected)
    ax.annotate("", xy=(0.8, 2.4), xytext=(1.4, 2.4), arrowprops=dict(arrowstyle="->", color='#ef4444', lw=1.2))
    ax.text(1.1, 2.5, "ปฏิเสธ", ha='center', va='bottom', fontsize=8, color='#ef4444')
    # Reject box
    rect_rej = patches.FancyBboxPatch((0.1, 2.1), 0.7, 0.6, boxstyle="round,pad=0.05", fc='#fef2f2', ec='#ef4444', lw=1.2)
    ax.add_patch(rect_rej)
    ax.text(0.45, 2.4, "ส่งเมลแจ้งเตือน\n(ถูกปฏิเสธ)", ha='center', va='center', fontsize=7, color='#ef4444')

    # Arrow User Yes (Approved)
    ax.annotate("", xy=(2.5, 1.0), xytext=(2.5, 1.7), arrowprops=dict(arrowstyle="->", color='#10b981', lw=1.2))
    ax.text(2.65, 1.4, "อนุมัติ", ha='left', va='center', fontsize=8, color='#10b981')
    
    # 7. Take & Return (Rectangle)
    rect_take = patches.FancyBboxPatch((1.5, 0.3), 2.0, 0.6, boxstyle="round,pad=0.05", fc='#ffffff', ec='#10b981', lw=1.2)
    ax.add_patch(rect_take)
    ax.text(2.5, 0.6, "รับของไปใช้ -> กดคืนรูปถ่าย\n(รอแอดมินรับคืนคลัง)", ha='center', va='center', fontsize=8)

    # --- Admin Path ---
    # 8. Manage & Approve (Rectangle)
    rect_adm_dash = patches.FancyBboxPatch((6.5, 5.8), 2.0, 0.6, boxstyle="round,pad=0.05", fc='#ffffff', ec='#0ea5e9', lw=1.2)
    ax.add_patch(rect_adm_dash)
    ax.text(7.5, 6.1, "จัดการคำขอ (Dashboard)\n& ระบบสต็อกอุปกรณ์", ha='center', va='center', fontsize=8)

    # Arrow Admin 1
    ax.annotate("", xy=(7.5, 4.9), xytext=(7.5, 5.7), arrowprops=dict(arrowstyle="->", color='#475569', lw=1.2))

    # 9. Send Warnings / Notify (Rectangle)
    rect_warn = patches.FancyBboxPatch((6.5, 4.1), 2.0, 0.7, boxstyle="round,pad=0.05", fc='#ffffff', ec='#ef4444', lw=1.2)
    ax.add_patch(rect_warn)
    ax.text(7.5, 4.45, "ตรวจสอบรายการค้างส่งคืน\nส่งอีเมลเตือนด่วน 🚨", ha='center', va='center', fontsize=8, color='#b91c1c')

    # Arrow Admin -> User Status Decision (Connecting Line)
    ax.annotate("", xy=(3.6, 2.4), xytext=(6.4, 6.1),
                arrowprops=dict(arrowstyle="->", color='#0284c7', lw=1.2, connectionstyle="arc3,rad=-0.15"))
    ax.text(5.0, 4.6, "พิจารณาอนุมัติ", ha='center', va='bottom', fontsize=8, color='#0284c7')

    # Connect Reject and Return to End
    # 10. End (Oval)
    ellipse_end = patches.Ellipse((5, 0.6), 1.5, 0.6, fc='#f1f5f9', ec='#475569', lw=1.5)
    ax.add_patch(ellipse_end)
    ax.text(5, 0.6, "สิ้นสุด (End)", ha='center', va='center', weight='bold', fontsize=9)

    # Arrow from Reject to End
    ax.annotate("", xy=(4.2, 0.6), xytext=(0.45, 2.0),
                arrowprops=dict(arrowstyle="->", color='#475569', lw=1.0, connectionstyle="arc3,rad=-0.4"))

    # Arrow from Return to End
    ax.annotate("", xy=(4.2, 0.6), xytext=(3.6, 0.6), arrowprops=dict(arrowstyle="->", color='#475569', lw=1.2))

    # Arrow from Admin Warning to End
    ax.annotate("", xy=(5.8, 0.6), xytext=(7.5, 4.0),
                arrowprops=dict(arrowstyle="->", color='#475569', lw=1.0, connectionstyle="arc3,rad=0.3"))

    save_fig(fig, "system_flowchart.png")
    plt.close(fig)

if __name__ == "__main__":
    print("🎨 Rendering system diagrams using matplotlib...")
    draw_context_diagram()
    draw_er_diagram()
    draw_system_flowchart()
    print("✨ Rendering complete! Files saved successfully.")
