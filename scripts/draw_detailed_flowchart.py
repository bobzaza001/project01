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

    # Color Constants
    c_blue = '#0284c7'      # Process
    c_orange = '#ea580c'    # Decision
    c_green = '#16a34a'     # Success / Return
    c_red = '#dc2626'       # Warning / Reject
    c_gray = '#4b5563'      # Start / End
    c_text = '#1f2937'

    # Helper function to draw Start/End (Oval)
    def draw_start_end(x, y, text):
        el = patches.Ellipse((x, y), 2.0, 0.6, fc='#f3f4f6', ec=c_gray, lw=2, zorder=3)
        ax.add_patch(el)
        ax.text(x, y, text, ha='center', va='center', color=c_text, weight='bold', fontsize=10, zorder=4)

    # Helper function to draw Process (Rectangle)
    def draw_process(x, y, w, h, text, border_color=c_blue, bg='#ffffff'):
        rect = patches.FancyBboxPatch((x-w/2, y-h/2), w, h, boxstyle="round,pad=0.03", fc=bg, ec=border_color, lw=1.8, zorder=3)
        ax.add_patch(rect)
        ax.text(x, y, text, ha='center', va='center', color=c_text, fontsize=9, zorder=4)

    # Helper function to draw Decision (Diamond)
    def draw_decision(x, y, text, border_color=c_orange):
        pts = [[x, y+0.65], [x+1.3, y], [x, y-0.65], [x-1.3, y]]
        poly = patches.Polygon(pts, closed=True, fc='#fffbeb', ec=border_color, lw=1.8, zorder=3)
        ax.add_patch(poly)
        ax.text(x, y, text, ha='center', va='center', color=c_text, weight='bold', fontsize=8.5, zorder=4)

    # Title
    ax.text(6, 15.5, "แผนภาพขั้นตอนการทำงานของระบบ (System Flowchart)", 
            ha='center', va='center', fontsize=14, weight='bold', color='#1e3a8a')

    # --- Draw Elements ---
    # 1. Start (14.8)
    draw_start_end(6, 14.8, "เริ่มต้น (Start)")
    
    # 2. Login (13.7)
    draw_process(6, 13.7, 2.8, 0.6, "เข้าสู่ระบบ (Login)\n(ระบุรหัสประจำตัว)")
    
    # 3. Role Check (12.3)
    draw_decision(6, 12.3, "ตรวจสอบสิทธิ์?")

    # --- Student Path (Left side, x=2.5) ---
    # 4. View Equipment (10.7)
    draw_process(2.5, 10.7, 3.2, 0.7, "เข้าหน้าจอคลังอุปกรณ์\n(ค้นหา/กรองตามห้อง/หมวดหมู่)")
    
    # 5. Select type (9.3)
    draw_decision(2.5, 9.3, "ประเภทการทำรายการ?")
    
    # 5a. Consumable Branch (Left of Left, x=0.8)
    draw_process(0.8, 8.0, 2.2, 0.6, "ยื่นคำขอเบิกวัสดุ\n(ระบุจำนวนเบิก)")
    draw_decision(0.8, 6.7, "แอดมินอนุมัติ?")
    draw_process(0.8, 5.3, 2.2, 0.6, "ตัดสต็อกคงเหลือทันที\n(สถานะ: เบิกเรียบร้อย)", border_color=c_green)
    
    # 5b. Durable Branch (Right of Left, x=3.8)
    draw_process(3.8, 8.0, 2.5, 0.7, "ยื่นคำขอยืมครุภัณฑ์\n(ระบุวันเวลายืม + จำนวนวัน)")
    draw_decision(3.8, 6.7, "แอดมินอนุมัติ?")
    
    # Durable Reject (x=5.6, y=6.7)
    draw_process(5.6, 6.7, 1.8, 0.6, "ส่งเมลแจ้งเตือนภัย\n(ถูกปฏิเสธ)", border_color=c_red, bg='#fef2f2')
    
    # Durable Approved
    draw_process(3.8, 5.3, 2.3, 0.6, "หักสต็อกที่ว่างพร้อมยืม\nส่งเมลแจ้งผลอนุมัติ", border_color=c_green)
    draw_process(3.8, 4.1, 2.3, 0.6, "ผู้ใช้รับอุปกรณ์ไปใช้งาน")
    draw_process(3.8, 2.9, 2.4, 0.7, "กดยื่นแจ้งส่งคืนในระบบ\nพร้อมอัปโหลดรูปหลักฐานการคืน")
    draw_decision(3.8, 1.7, "แอดมินยืนยันคืน?")
    draw_process(3.8, 0.6, 2.4, 0.6, "บวกสต็อกกลับคืนคลัง\n(สถานะ: คืนเรียบร้อย)", border_color=c_green)

    # --- Admin Path (Right side, x=9.5) ---
    # 6. Admin Dash (10.7)
    draw_process(9.5, 10.7, 2.8, 0.6, "เข้าหน้าแดชบอร์ดแอดมิน\n(Admin Dashboard)")
    
    # 7. Admin Action (9.3)
    draw_decision(9.5, 9.3, "เลือกการทำงาน?")
    
    # Admin Options
    draw_process(7.6, 8.0, 2.0, 0.6, "จัดการอุปกรณ์\n(เพิ่ม/แก้ไข/ลบ)")
    draw_process(9.5, 8.0, 2.0, 0.6, "จัดการสถานที่\n(อาคาร/ชั้น/ห้อง)")
    draw_process(11.3, 8.0, 2.0, 0.6, "ตรวจสอบค้างส่ง\n& ส่งเมลเตือนด่วน", border_color=c_red)

    # 8. End (Bottom center, x=7.0, y=0.6)
    draw_start_end(7.2, 0.6, "สิ้นสุด (End)")

    # --- Connecting Arrows (Lines) ---
    # Helper to draw arrow line
    def draw_arrow(x1, y1, x2, y2, color=c_gray, text="", ha='center', va='bottom', rad=0):
        if rad == 0:
            ax.annotate(text, xy=(x2, y2), xytext=(x1, y1),
                        arrowprops=dict(arrowstyle="->", color=color, lw=1.2),
                        color=color, fontsize=8, ha=ha, va=va)
        else:
            ax.annotate(text, xy=(x2, y2), xytext=(x1, y1),
                        arrowprops=dict(arrowstyle="->", color=color, lw=1.2, connectionstyle=f"arc3,rad={rad}"),
                        color=color, fontsize=8, ha=ha, va=va)

    # Start -> Login
    draw_arrow(6, 14.5, 6, 14.0)
    # Login -> Role
    draw_arrow(6, 13.4, 6, 13.0)
    
    # Role -> Student Path
    ax.plot([6, 2.5, 2.5], [12.3, 12.3, 11.1], color=c_gray, lw=1.2)
    ax.annotate("นักศึกษา / อาจารย์", xy=(2.5, 11.1), xytext=(4.25, 12.4),
                arrowprops=dict(arrowstyle="->", color=c_gray, lw=1.2),
                color=c_text, fontsize=8, ha='center', va='bottom')
                
    # Role -> Admin Path
    ax.plot([6, 9.5, 9.5], [12.3, 12.3, 11.1], color=c_gray, lw=1.2)
    ax.annotate("ผู้ดูแลระบบ (Admin)", xy=(9.5, 11.1), xytext=(7.75, 12.4),
                arrowprops=dict(arrowstyle="->", color=c_gray, lw=1.2),
                color=c_text, fontsize=8, ha='center', va='bottom')

    # Student View -> Select Type
    draw_arrow(2.5, 10.35, 2.5, 10.0)
    
    # Select Type -> Consumable
    ax.plot([2.5, 0.8, 0.8], [9.3, 9.3, 8.35], color=c_gray, lw=1.2)
    ax.annotate("เบิกวัสดุ", xy=(0.8, 8.35), xytext=(1.65, 9.4),
                arrowprops=dict(arrowstyle="->", color=c_gray, lw=1.2),
                color=c_text, fontsize=7.5, ha='center', va='bottom')

    # Select Type -> Durable
    ax.plot([2.5, 3.8, 3.8], [9.3, 9.3, 8.35], color=c_gray, lw=1.2)
    ax.annotate("ยืมครุภัณฑ์", xy=(3.8, 8.35), xytext=(3.15, 9.4),
                arrowprops=dict(arrowstyle="->", color=c_gray, lw=1.2),
                color=c_text, fontsize=7.5, ha='center', va='bottom')

    # Consumable Path
    draw_arrow(0.8, 7.7, 0.8, 7.4)
    draw_arrow(0.8, 6.05, 0.8, 5.6, color=c_green, text="อนุมัติ", ha='left', va='center')
    ax.annotate("ปฏิเสธ", xy=(1.9, 5.3), xytext=(0.8, 6.7),
                arrowprops=dict(arrowstyle="->", color=c_red, lw=1.2, connectionstyle="arc3,rad=-0.4"),
                color=c_red, fontsize=7.5, ha='center', va='bottom')
    
    # Durable Path
    draw_arrow(3.8, 7.65, 3.8, 7.4)
    draw_arrow(3.8, 6.05, 3.8, 5.6, color=c_green, text="อนุมัติ", ha='left', va='center')
    draw_arrow(4.8, 6.7, 5.0, 6.7, color=c_red, text="ปฏิเสธ", ha='center', va='bottom')
    
    draw_arrow(3.8, 5.0, 3.8, 4.4)
    draw_arrow(3.8, 3.8, 3.8, 3.3)
    draw_arrow(3.8, 2.55, 3.8, 2.4)
    draw_arrow(3.8, 1.05, 3.8, 0.9, color=c_green, text="ยืนยัน", ha='left', va='center')
    
    # Admin Path
    draw_arrow(9.5, 10.4, 9.5, 10.0)
    
    # Actions branches
    ax.plot([9.5, 7.6, 7.6], [9.3, 9.3, 8.35], color=c_gray, lw=1.2)
    draw_arrow(7.6, 9.3, 7.6, 8.35, color=c_gray)
    
    ax.plot([9.5, 9.5], [9.3, 8.35], color=c_gray, lw=1.2)
    draw_arrow(9.5, 9.3, 9.5, 8.35, color=c_gray)
    
    ax.plot([9.5, 11.3, 11.3], [9.3, 9.3, 8.35], color=c_gray, lw=1.2)
    draw_arrow(11.3, 9.3, 11.3, 8.35, color=c_gray)

    # Connections to End
    # Consumable success -> End
    ax.plot([0.8, 0.8, 6.2], [5.0, 0.3, 0.3], color=c_gray, lw=1.2)
    draw_arrow(6.2, 0.3, 6.2, 0.5, color=c_gray)
    
    # Durable success -> End
    draw_arrow(3.8, 0.3, 6.2, 0.5, color=c_gray)
    
    # Admin Actions -> End
    ax.plot([7.6, 7.6, 8.2], [7.7, 0.6, 0.6], color=c_gray, lw=1.2)
    draw_arrow(8.2, 0.6, 8.2, 0.6, color=c_gray)

    ax.plot([9.5, 9.5, 8.2], [7.7, 0.6, 0.6], color=c_gray, lw=1.2)
    ax.plot([11.3, 11.3, 8.2], [7.7, 0.6, 0.6], color=c_gray, lw=1.2)

    # Save to local and brain paths
    local_path = "static/img/diagrams/system_flowchart_detailed.png"
    artifact_path = "C:/Users/ACER/.gemini/antigravity/brain/b500e698-6452-4be9-bee4-08259588db82/system_flowchart_detailed.png"
    fig.savefig(local_path, bbox_inches='tight', dpi=300)
    fig.savefig(artifact_path, bbox_inches='tight', dpi=300)
    print(f"Generated Detailed Flowchart at: {local_path} and {artifact_path}")
    plt.close(fig)

if __name__ == "__main__":
    draw_detailed_flowchart()
