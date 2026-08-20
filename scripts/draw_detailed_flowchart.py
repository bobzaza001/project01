import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Set Font and Style
plt.rcParams['font.family'] = 'Tahoma'  # Tahoma is standard on Windows and supports Thai
plt.rcParams['figure.facecolor'] = '#ffffff'
plt.rcParams['axes.facecolor'] = '#ffffff'

os.makedirs("static/img/diagrams", exist_ok=True)
os.makedirs("C:/Users/ACER/.gemini/antigravity/brain/b500e698-6452-4be9-bee4-08259588db82", exist_ok=True)

def draw_detailed_flowchart():
    fig, ax = plt.subplots(figsize=(12, 16))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 16)
    ax.axis('off')

    # Color Constants (Professional Flowchart Theme)
    c_blue = '#0f172a'      # Process border
    c_bg_proc = '#f8fafc'   # Process background
    c_orange = '#ea580c'    # Decision border
    c_bg_dec = '#fffbeb'     # Decision background
    c_green = '#15a34a'     # Approved/Returned
    c_bg_green = '#f0fdf4'
    c_red = '#dc2626'       # Rejected/Warning
    c_bg_red = '#fef2f2'
    c_gray = '#4b5563'      # Start/End
    c_text = '#0f172a'

    # Helper function to draw Start/End (Oval)
    def draw_start_end(x, y, text):
        el = patches.Ellipse((x, y), 2.2, 0.6, fc='#f1f5f9', ec=c_gray, lw=2, zorder=3)
        ax.add_patch(el)
        ax.text(x, y, text, ha='center', va='center', color=c_text, weight='bold', fontsize=10, zorder=4)

    # Helper function to draw Process (Rectangle)
    def draw_process(x, y, w, h, text, border_color=c_blue, bg=c_bg_proc):
        rect = patches.FancyBboxPatch((x-w/2, y-h/2), w, h, boxstyle="round,pad=0.03", fc=bg, ec=border_color, lw=1.8, zorder=3)
        ax.add_patch(rect)
        ax.text(x, y, text, ha='center', va='center', color=c_text, fontsize=9.5, zorder=4)

    # Helper function to draw Decision (Diamond)
    def draw_decision(x, y, text, border_color=c_orange, bg=c_bg_dec):
        pts = [[x, y+0.7], [x+1.5, y], [x, y-0.7], [x-1.5, y]]
        poly = patches.Polygon(pts, closed=True, fc=bg, ec=border_color, lw=1.8, zorder=3)
        ax.add_patch(poly)
        ax.text(x, y, text, ha='center', va='center', color=c_text, weight='bold', fontsize=9, zorder=4)

    # Title
    ax.text(6, 15.5, "แผนภาพขั้นตอนการทำงานของระบบ (System Flowchart)", 
            ha='center', va='center', fontsize=15, weight='bold', color='#1e3a8a')

    # --- Draw Elements ---
    # 1. Start
    draw_start_end(6, 14.7, "เริ่มต้น (Start)")
    
    # 2. Login
    draw_process(6, 13.6, 3.2, 0.7, "เข้าสู่ระบบ Login\n(ระบุรหัสประจำตัว/อีเมล)")
    
    # 3. Check Role
    draw_decision(6, 12.1, "ตรวจสอบสิทธิ์?")

    # --- Student Path (Left side, x=2.5) ---
    # 4. View Equipment (10.4)
    draw_process(2.5, 10.4, 3.4, 0.7, "ดูคลังครุภัณฑ์/ค้นหาอุปกรณ์\n(กรองตามสถานที่/หมวดหมู่)")
    
    # 5. Select type (8.9)
    draw_decision(2.5, 8.9, "เลือกประเภทการยื่น?")
    
    # 5a. Consumable Branch (Left, x=0.9)
    draw_process(0.9, 7.4, 2.3, 0.6, "ยื่นคำขอเบิกวัสดุ\nConsumable")
    draw_decision(0.9, 6.0, "แอดมินอนุมัติ?")
    draw_process(0.9, 4.6, 2.3, 0.6, "หักจำนวนสะสมในสต็อก\n(สถานะ: เบิกเรียบร้อย)", border_color=c_green, bg=c_bg_green)
    
    # 5b. Durable Branch (Right, x=4.1)
    draw_process(4.1, 7.4, 2.5, 0.7, "ยื่นคำขอยืมครุภัณฑ์ Durable\n(ระบุวันเวลายืม + จำนวนวัน)")
    draw_decision(4.1, 6.0, "แอดมินอนุมัติ?")
    
    # Durable Reject (x=5.8, y=6.0)
    draw_process(5.8, 6.0, 1.8, 0.6, "ส่งเมลแจ้งปฏิเสธ\n(Rejected)", border_color=c_red, bg=c_bg_red)
    
    # Durable Approved (x=4.1, y=4.6)
    draw_process(4.1, 4.6, 2.4, 0.6, "หักสต็อกพร้อมยืม\nส่งเมลแจ้งผลอนุมัติ", border_color=c_green, bg=c_bg_green)
    draw_process(4.1, 3.4, 2.4, 0.6, "ผู้ใช้รับอุปกรณ์ไปใช้งาน")
    draw_process(4.1, 2.2, 2.5, 0.7, "กดยื่นแจ้งส่งคืนในระบบ\nพร้อมอัปโหลดรูปหลักฐาน")
    draw_decision(4.1, 1.0, "แอนมินยืนยันคืน?")
    draw_process(4.1, 0.2, 2.5, 0.6, "บวกสต็อกกลับคืนคลัง\n(สถานะ: คืนเรียบร้อย)", border_color=c_green, bg=c_bg_green)

    # --- Admin Path (Right side, x=9.5) ---
    # 6. Admin Dash (10.4)
    draw_process(9.5, 10.4, 3.2, 0.7, "เข้าแดชบอร์ดแอดมิน\nAdmin Dashboard")
    
    # 7. Admin Action (8.9)
    draw_decision(9.5, 8.9, "เลือกการทำงาน?")
    
    # Admin Options
    draw_process(7.3, 7.4, 2.0, 0.6, "จัดการคลังอุปกรณ์\n(เพิ่ม/แก้ไข/ลบ)")
    draw_process(9.5, 7.4, 2.0, 0.6, "จัดการแผนผังห้อง\n(อาคาร/ชั้น/ห้อง)")
    draw_process(11.4, 7.4, 2.0, 0.6, "ตรวจสอบค้างส่ง\n& ส่งเมลเตือนด่วน", border_color=c_red, bg=c_bg_red)

    # 8. End (Bottom center, x=7.5, y=0.2)
    draw_start_end(7.5, 0.2, "สิ้นสุดการทำงาน")

    # --- Connecting Arrows (Orthogonal / Straight Lines Only) ---
    def draw_straight_arrow(x1, y1, x2, y2, color=c_gray, text="", ha='center', va='bottom', path='direct'):
        # Direct line
        if path == 'direct':
            ax.annotate(text, xy=(x2, y2), xytext=(x1, y1),
                        arrowprops=dict(arrowstyle="->", color=color, lw=1.5),
                        color=color, fontsize=8.5, ha=ha, va=va)
        elif path == 'h-v':
            # Horizontal first, then Vertical
            ax.plot([x1, x2], [y1, y1], color=color, lw=1.5)
            ax.annotate(text, xy=(x2, y2), xytext=(x2, y1),
                        arrowprops=dict(arrowstyle="->", color=color, lw=1.5),
                        color=color, fontsize=8.5, ha=ha, va=va)
        elif path == 'v-h':
            # Vertical first, then Horizontal
            ax.plot([x1, x1], [y1, y2], color=color, lw=1.5)
            ax.annotate(text, xy=(x2, y2), xytext=(x1, y2),
                        arrowprops=dict(arrowstyle="->", color=color, lw=1.5),
                        color=color, fontsize=8.5, ha=ha, va=va)

    # 1. Start -> Login
    draw_straight_arrow(6, 14.4, 6, 14.0)
    
    # 2. Login -> Role Check
    draw_straight_arrow(6, 13.25, 6, 12.8)
    
    # 3. Role Check -> Student View (h-v path)
    draw_straight_arrow(4.5, 12.1, 2.5, 10.75, path='h-v', text="นักศึกษา/อาจารย์  ", ha='right', va='center')
    
    # 4. Role Check -> Admin Dash (h-v path)
    draw_straight_arrow(7.5, 12.1, 9.5, 10.75, path='h-v', text="  ผู้ดูแลระบบ (Admin)", ha='left', va='center')

    # 5. Student View -> Select Type
    draw_straight_arrow(2.5, 10.05, 2.5, 9.6)
    
    # 6. Select Type -> Consumable (h-v path)
    draw_straight_arrow(1.0, 8.9, 0.9, 7.7, path='h-v', text="เบิกวัสดุ  ", ha='right', va='center')
    
    # 7. Select Type -> Durable (h-v path)
    draw_straight_arrow(4.0, 8.9, 4.1, 7.75, path='h-v', text="  ยืมครุภัณฑ์", ha='left', va='center')

    # --- Consumable Flow (Straight Vertical) ---
    draw_straight_arrow(0.9, 7.1, 0.9, 6.7)
    draw_straight_arrow(0.9, 5.3, 0.9, 4.9, color=c_green, text="อนุมัติ ", ha='right', va='center')
    
    # Consumable Reject -> End (h-v path)
    ax.plot([0.9, -0.2, -0.2, 7.5], [6.0, 6.0, -0.5, -0.5], color=c_red, lw=1.5)
    draw_straight_arrow(7.5, -0.5, 7.5, -0.1, color=c_red, path='direct', text="ปฏิเสธ", ha='center', va='bottom')
    
    # Consumable Success -> End (v-h-v path)
    ax.plot([0.9, 0.9, 5.5], [4.3, -0.3, -0.3], color=c_gray, lw=1.5)
    draw_straight_arrow(5.5, -0.3, 7.5, -0.3, color=c_gray, path='h-v')

    # --- Durable Flow (Straight Vertical) ---
    draw_straight_arrow(4.1, 7.05, 4.1, 6.7)
    draw_straight_arrow(4.1, 5.3, 4.1, 4.9, color=c_green, text="อนุมัติ ", ha='right', va='center')
    
    # Durable Reject -> Send Email
    draw_straight_arrow(5.6, 6.0, 4.9, 6.0, color=c_red, text="ปฏิเสธ", ha='center', va='bottom')
    # Reject email to end
    ax.plot([5.8, 5.8, 7.5], [5.7, -0.4, -0.4], color=c_gray, lw=1.5)

    # Durable Success steps
    draw_straight_arrow(4.1, 4.3, 4.1, 3.7)
    draw_straight_arrow(4.1, 3.1, 4.1, 2.55)
    draw_straight_arrow(4.1, 1.85, 4.1, 1.7)
    draw_straight_arrow(4.1, 0.3, 4.1, 0.5, color=c_green, text="ยืนยันรับคืน ", ha='right', va='center')
    
    # Confirm Return Reject -> Return to use
    ax.plot([2.6, 2.6, 4.1], [1.0, 3.4, 3.4], color=c_red, lw=1.5)
    draw_straight_arrow(4.1, 1.0, 2.6, 1.0, color=c_red, text="ไม่ใช่/ไม่อนุมัติ", ha='center', va='bottom')

    # Durable Finished -> End
    draw_straight_arrow(4.1, -0.1, 7.5, 0.2, path='h-v')

    # --- Admin Flow ---
    draw_straight_arrow(9.5, 10.05, 9.5, 9.6)
    
    # Admin Action Branches (h-v paths)
    draw_straight_arrow(7.3, 8.9, 7.3, 7.7, path='h-v')
    draw_straight_arrow(9.5, 8.9, 9.5, 7.7)
    draw_straight_arrow(11.4, 8.9, 11.4, 7.7, path='h-v')

    # Admin Actions -> End connection
    ax.plot([7.3, 7.3, 7.5], [7.1, 0.9, 0.9], color=c_gray, lw=1.5)
    ax.plot([9.5, 9.5, 7.5], [7.1, 0.9, 0.9], color=c_gray, lw=1.5)
    ax.plot([11.4, 11.4, 7.5], [7.1, 0.9, 0.9], color=c_gray, lw=1.5)
    draw_straight_arrow(7.5, 0.9, 7.5, 0.5)

    # Save to local and brain paths
    local_path = "static/img/diagrams/system_flowchart.png"
    artifact_path = "C:/Users/ACER/.gemini/antigravity/brain/b500e698-6452-4be9-bee4-08259588db82/system_flowchart.png"
    fig.savefig(local_path, bbox_inches='tight', dpi=300)
    fig.savefig(artifact_path, bbox_inches='tight', dpi=300)
    print(f"Updated Flowchart successfully with straight orthogonal lines at: {local_path}")
    plt.close(fig)

if __name__ == "__main__":
    draw_detailed_flowchart()
