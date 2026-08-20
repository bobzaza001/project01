import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Set Font and Style for Dark Theme
plt.rcParams['font.family'] = 'Tahoma'  # Tahoma supports Thai on Windows
plt.rcParams['figure.facecolor'] = '#121214'
plt.rcParams['axes.facecolor'] = '#121214'

os.makedirs("static/img/diagrams", exist_ok=True)
os.makedirs("C:/Users/ACER/.gemini/antigravity/brain/b500e698-6452-4be9-bee4-08259588db82", exist_ok=True)

def draw_dark_flowchart():
    fig, ax = plt.subplots(figsize=(16, 22))
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 22)
    ax.axis('off')

    # Color Constants (Dark Mode draw.io Theme)
    c_bg = '#121214'
    c_card_bg = '#1e1e24'
    c_card_border = '#3f4248'
    c_text = '#ffffff'
    c_text_muted = '#a1a1aa'
    
    # Accent colors
    c_blue = '#38bdf8'       # Process highlighting / Flow lines
    c_orange = '#f59e0b'     # Decision diamonds
    c_green = '#10b981'      # Approved/Returned
    c_red = '#f43f5e'        # Reject/Warning

    # Helper function to draw Start/End (Oval)
    def draw_oval(x, y, text):
        el = patches.Ellipse((x, y), 2.2, 0.6, fc=c_card_bg, ec=c_card_border, lw=2, zorder=3)
        ax.add_patch(el)
        ax.text(x, y, text, ha='center', va='center', color=c_text, weight='bold', fontsize=10, zorder=4)

    # Helper function to draw Process (Rectangle)
    def draw_process(x, y, w, h, text, border_color=c_card_border, bg=c_card_bg):
        rect = patches.FancyBboxPatch((x-w/2, y-h/2), w, h, boxstyle="round,pad=0.03", fc=bg, ec=border_color, lw=1.8, zorder=3)
        ax.add_patch(rect)
        ax.text(x, y, text, ha='center', va='center', color=c_text, fontsize=9.5, zorder=4)

    # Helper function to draw Decision (Diamond)
    def draw_decision(x, y, text, border_color=c_orange, bg=c_card_bg):
        pts = [[x, y+0.75], [x+1.6, y], [x, y-0.75], [x-1.6, y]]
        poly = patches.Polygon(pts, closed=True, fc=bg, ec=border_color, lw=1.8, zorder=3)
        ax.add_patch(poly)
        ax.text(x, y, text, ha='center', va='center', color=c_text, weight='bold', fontsize=9, zorder=4)

    # Helper to draw straight line segment paths
    def draw_path(pts, color=c_blue, arrow=True):
        for i in range(len(pts)-1):
            x1, y1 = pts[i]
            x2, y2 = pts[i+1]
            if arrow and i == len(pts)-2:
                # Last segment gets an arrow
                ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                            arrowprops=dict(arrowstyle="-|>", color=color, lw=1.5, mutation_scale=12, fc=color))
            else:
                ax.plot([x1, x2], [y1, y2], color=color, lw=1.5)

    # Helper to add text on lines
    def draw_line_text(x, y, text, color=c_text_muted, ha='center', va='center'):
        ax.text(x, y, text, color=color, fontsize=8.5, ha=ha, va=va,
                bbox=dict(facecolor=c_bg, edgecolor='none', pad=2))

    # --- Title ---
    ax.text(9, 21.4, "แผนภาพขั้นตอนการทำงานของระบบ (System Flowchart)", 
            ha='center', va='center', fontsize=16, weight='bold', color=c_blue)

    # --- Draw Elements ---
    
    # 1. Start (Center)
    draw_oval(9, 20.5, "เริ่มต้น")
    
    # 2. Login (Center)
    draw_process(9, 19.3, 3.2, 0.7, "เข้าสู่ระบบ Login\n(ระบุชื่อผู้ใช้/รหัสผ่าน)")
    
    # 3. Check Role (Center Diamond)
    draw_decision(9, 17.5, "ตรวจสอบสิทธิ์?")

    # --- Left Path: Student (X=4.0) ---
    draw_process(4.0, 15.6, 3.5, 0.7, "หน้าจอคลังอุปกรณ์ Equipment List")
    draw_process(4.0, 14.2, 3.6, 0.7, "ค้นหาและกรองอุปกรณ์ตามอาคาร ชั้น ห้อง\nหรือตามประเภทครุภัณฑ์/วัสดุ")
    draw_decision(4.0, 12.4, "เลือกประเภทการทำ?")
    
    # Consumable Path (Left of Student Path, X=1.5)
    draw_process(1.5, 10.7, 2.3, 0.7, "ยื่นคำขอเบิกวัสดุ\nConsumable")
    draw_decision(1.5, 9.2, "แอดมินอนุมัติ?")
    draw_process(0.8, 7.5, 1.8, 0.6, "หักจำนวนสะสมในคลัง\n(ไม่ต้องส่งคืน)", border_color=c_green)
    draw_process(2.4, 7.5, 1.8, 0.6, "ระบบยกเลิกคำขอ /\nแจ้งปฏิเสธการเบิก", border_color=c_red)

    # Durable Path (Right of Student Path, X=5.5)
    draw_process(5.5, 10.7, 2.6, 0.7, "ยื่นคำขอยืมครุภัณฑ์ Durable\n(ระบุวันเวลายืม + จำนวนวัน)")
    draw_decision(7.0, 9.2, "แอดมินอนุมัติ?")
    
    draw_process(5.5, 7.5, 1.8, 0.6, "ส่งเมลแจ้งปฏิเสธ\n(Rejected Email)", border_color=c_red)
    draw_process(7.5, 7.5, 2.0, 0.6, "หักสต็อกพร้อมยืมชั่วคราว\nส่งเมลแจ้งผลอนุมัติ", border_color=c_green)
    draw_process(7.5, 6.3, 2.0, 0.6, "ผู้ใช้รับอุปกรณ์ไปใช้งาน")
    draw_process(7.5, 5.1, 2.5, 0.7, "แจ้งส่งคืนผ่านระบบ\nพร้อมอัปโหลดภาพหลักฐาน")
    draw_decision(7.5, 3.5, "แอดมินอนุมัติคืน?")
    draw_process(7.5, 2.0, 2.5, 0.6, "บวกสต็อกกลับคืนคลัง\n(สถานะ: คืนเรียบร้อย)", border_color=c_green)

    # --- Right Path: Admin (X=14.0) ---
    draw_process(14.0, 15.6, 3.2, 0.7, "แดชบอร์ดแอดมิน\nAdmin Dashboard")
    draw_decision(14.0, 13.9, "เลือกการทำงาน?")

    # Admin actions
    # Action 1: Review Requests (Centered to connect back)
    draw_process(11.0, 12.3, 3.0, 0.7, "ตรวจสอบใบคำร้องยื่นยืม\nและ ตรวจรูปถ่ายสภาพการคืน")
    # Action 2: Manage Equipment
    draw_process(12.2, 10.7, 2.4, 0.6, "เพิ่ม / แก้ไข / ลบ\nข้อมูลอุปกรณ์และรูปภาพ")
    # Action 3: Manage Locations
    draw_process(14.8, 10.7, 2.4, 0.6, "จัดการพิกัดห้องเรียน\n(อาคาร / ชั้น / ห้อง)")
    # Action 4: Overdue Check
    draw_process(17.0, 10.7, 1.8, 0.6, "ส่งใบเตือนคืนของ\n(Overdue)")
    
    # Overdue Decision (Diamond)
    draw_decision(17.0, 9.2, "ค้างคืนครุภัณฑ์?")
    draw_process(16.0, 7.5, 2.2, 0.7, "ส่งอีเมลเตือนด่วนสีแดง\n(ตรวจเช็คค้างส่งอัตโนมัติ)", border_color=c_red)

    # 10. End (Bottom Center)
    draw_oval(9.0, 0.8, "สิ้นสุดการทำงาน")

    # --- Draw Connection Lines (Orthogonal Only) ---
    
    # Start -> Login
    draw_path([[9.0, 20.2], [9.0, 19.65]], arrow=True)
    # Login -> Role Check
    draw_path([[9.0, 18.95], [9.0, 18.25]], arrow=True)

    # Role Check -> Student Dashboard
    draw_path([[7.4, 17.5], [4.0, 17.5], [4.0, 15.95]], arrow=True)
    draw_line_text(5.7, 17.5, "นักศึกษา / อาจารย์", ha='center', va='bottom')

    # Role Check -> Admin Dashboard
    draw_path([[10.6, 17.5], [14.0, 17.5], [14.0, 15.95]], arrow=True)
    draw_line_text(12.3, 17.5, "ผู้ดูแลระบบ (Admin)", ha='center', va='bottom')

    # Student Dashboard -> Search & Filter
    draw_path([[4.0, 15.25], [4.0, 14.55]], arrow=True)
    # Search -> Select Type
    draw_path([[4.0, 13.85], [4.0, 13.15]], arrow=True)

    # Select Type -> Consumable
    draw_path([[2.4, 12.4], [1.5, 12.4], [1.5, 11.05]], arrow=True)
    draw_line_text(1.9, 12.4, "เบิกวัสดุ", ha='center', va='bottom')

    # Select Type -> Durable
    draw_path([[5.6, 12.4], [5.5, 12.4], [5.5, 11.05]], arrow=True)
    draw_line_text(5.5, 12.4, "ยืมครุภัณฑ์", ha='center', va='bottom')

    # --- Consumable Flow ---
    # Request -> Approve Diamond
    draw_path([[1.5, 10.35], [1.5, 9.95]], arrow=True)
    # Approve -> Yes (Left)
    draw_path([[1.5, 9.2], [0.8, 9.2], [0.8, 7.8]], arrow=True)
    draw_line_text(1.1, 9.2, "อนุมัติ", ha='center', va='bottom')
    # Approve -> No (Right)
    draw_path([[1.5, 9.2], [2.4, 9.2], [2.4, 7.8]], arrow=True)
    draw_line_text(2.0, 9.2, "ปฏิเสธ", ha='center', va='bottom')

    # Consumable Yes -> End
    draw_path([[0.8, 7.2], [0.8, 0.8], [7.9, 0.8]], arrow=True)
    # Consumable No -> End
    draw_path([[2.4, 7.2], [2.4, 1.2], [7.9, 1.2]], arrow=True)

    # --- Durable Flow ---
    # Request -> Approve Diamond (moves right and down)
    draw_path([[5.5, 10.35], [5.5, 9.2], [5.4, 9.2]], arrow=False)
    draw_path([[5.5, 9.2], [7.0, 9.2]], arrow=True)
    
    # Approve -> No (Left)
    draw_path([[7.0, 9.2], [5.5, 9.2], [5.5, 7.8]], arrow=True)
    draw_line_text(6.2, 9.2, "ปฏิเสธ", ha='center', va='bottom')
    # Approve -> Yes (Right)
    draw_path([[7.0, 9.2], [7.5, 9.2], [7.5, 7.8]], arrow=True)
    draw_line_text(7.25, 9.2, "อนุมัติ", ha='center', va='bottom')

    # Durable Rejected -> End
    draw_path([[5.5, 7.2], [5.5, 1.2], [7.9, 1.2]], arrow=False)

    # Durable Approved flow
    draw_path([[7.5, 7.2], [7.5, 6.6]], arrow=True)
    draw_path([[7.5, 6.0], [7.5, 5.45]], arrow=True)
    draw_path([[7.5, 4.75], [7.5, 4.25]], arrow=True)
    
    # Admin Approve Return -> Yes
    draw_path([[7.5, 2.75], [7.5, 2.3]], arrow=True)
    draw_line_text(7.5, 2.5, "ยืนยันรับคืน", ha='left', va='center')
    # Admin Approve Return -> No (Rejected return, loop back to "แจ้งส่งคืน")
    draw_path([[5.9, 3.5], [5.0, 3.5], [5.0, 5.1], [6.25, 5.1]], arrow=True, color=c_red)
    draw_line_text(5.4, 3.5, "ไม่อนุมัติ", color=c_red, ha='center', va='bottom')

    # Durable Finished -> End
    draw_path([[7.5, 1.7], [7.5, 0.8], [7.9, 0.8]], arrow=True)

    # --- Admin Flow ---
    # Dashboard -> Action Check
    draw_path([[14.0, 15.25], [14.0, 14.65]], arrow=True)

    # Action 1: Review Requests
    draw_path([[12.4, 13.9], [11.0, 13.9], [11.0, 12.65]], arrow=True)
    draw_line_text(11.7, 13.9, "อนุมัติยืม-คืน", ha='center', va='bottom')
    
    # Review Requests -> points to decision diamonds (connecting back to Student flow)
    # 1. points to Durable Approve Diamond at (7.0, 9.2)
    draw_path([[11.0, 11.95], [11.0, 9.2], [8.6, 9.2]], arrow=True, color=c_blue)
    # 2. points to Return Confirm Diamond at (7.5, 3.5)
    draw_path([[11.0, 11.95], [11.0, 3.5], [9.1, 3.5]], arrow=True, color=c_blue)

    # Action 2: Manage Equipment
    draw_path([[14.0, 13.9], [12.2, 13.9], [12.2, 11.05]], arrow=True)
    draw_line_text(12.9, 13.9, "จัดเก็บคลัง", ha='center', va='bottom')

    # Action 3: Manage Locations
    draw_path([[14.0, 13.9], [14.8, 13.9], [14.8, 11.05]], arrow=True)
    draw_line_text(14.5, 13.9, "พิกัดห้อง", ha='center', va='bottom')

    # Action 4: Overdue Check
    draw_path([[15.6, 13.9], [17.0, 13.9], [17.0, 11.05]], arrow=True)
    draw_line_text(16.3, 13.9, "เตือนส่งคืน", ha='center', va='bottom')

    # Overdue Check -> Decision
    draw_path([[17.0, 10.4], [17.0, 9.95]], arrow=True)
    # Decision -> Yes (Send Mail)
    draw_path([[17.0, 9.2], [17.0, 7.85]], arrow=False)
    draw_path([[17.0, 7.85], [17.1, 7.85]], arrow=False)
    draw_path([[17.0, 9.2], [16.0, 9.2], [16.0, 7.85]], arrow=True)
    draw_line_text(16.5, 9.2, "เกินกำหนด", ha='center', va='bottom')
    
    # Decision -> No (Normal)
    draw_path([[17.0, 9.2], [18.0, 9.2], [18.0, 0.8], [10.1, 0.8]], arrow=True)
    draw_line_text(17.5, 9.2, "ปกติ", ha='center', va='bottom')

    # Action Successes -> End (Connects back to End oval)
    # Manage Equipment to End
    draw_path([[12.2, 10.4], [12.2, 0.8], [10.1, 0.8]], arrow=False)
    # Manage Locations to End
    draw_path([[14.8, 10.4], [14.8, 0.8], [10.1, 0.8]], arrow=False)
    # Send Warn to End
    draw_path([[16.0, 7.15], [16.0, 0.8], [10.1, 0.8]], arrow=False)

    # Save both locally and to brain artifacts directory
    local_path = "static/img/diagrams/system_flowchart.png"
    artifact_path = "C:/Users/ACER/.gemini/antigravity/brain/b500e698-6452-4be9-bee4-08259588db82/system_flowchart.png"
    fig.savefig(local_path, bbox_inches='tight', dpi=300, facecolor=c_bg)
    fig.savefig(artifact_path, bbox_inches='tight', dpi=300, facecolor=c_bg)
    print(f"Generated EXACT Dark Theme Flowchart at: {local_path} and {artifact_path}")
    plt.close(fig)

if __name__ == "__main__":
    draw_dark_flowchart()
