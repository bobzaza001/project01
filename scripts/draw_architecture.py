import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Set Font and Style
plt.rcParams['font.family'] = 'Tahoma'  # Tahoma is standard on Windows and supports Thai
plt.rcParams['figure.facecolor'] = '#f8fafc'
plt.rcParams['axes.facecolor'] = '#f8fafc'

# Create output directories
os.makedirs("static/img/diagrams", exist_ok=True)
os.makedirs("C:/Users/ACER/.gemini/antigravity/brain/b500e698-6452-4be9-bee4-08259588db82", exist_ok=True)

def draw_system_architecture():
    fig, ax = plt.subplots(figsize=(12, 9))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 9)
    ax.axis('off')

    # Title
    ax.text(6, 8.5, "สถาปัตยกรรมระบบจัดการยืม-คืนครุภัณฑ์ (LAB Equipment System) - 3-TIER", 
            ha='center', va='center', fontsize=14, weight='bold', color='#1e3a8a')
    ax.text(6, 8.1, "โครงงานระบบบริหารจัดการห้องปฏิบัติการคอมพิวเตอร์", 
            ha='center', va='center', fontsize=10, color='#64748b', style='italic')

    # Box styles
    fc_title = '#1e3a8a'
    fc_box = '#ffffff'
    border_blue = '#0ea5e9'
    border_indigo = '#4f46e5'
    border_emerald = '#10b981'

    # Helper function to draw layer boxes
    def draw_layer(x, y, w, h, title, details, color):
        # Layer outer boundary
        rect = patches.FancyBboxPatch((x, y-h), w, h, boxstyle="round,pad=0.08",
                                      fc=fc_box, ec=color, lw=2.5, zorder=2)
        ax.add_patch(rect)
        # Layer Header
        header = patches.FancyBboxPatch((x, y-0.45), w, 0.45, boxstyle="round,pad=0.08",
                                        fc=color, ec=color, zorder=3)
        ax.add_patch(header)
        ax.text(x + w/2, y-0.22, title, ha='center', va='center', color='white', weight='bold', fontsize=10, zorder=4)
        
        # Details text
        for i, text in enumerate(details):
            # Check if text is bold header or normal detail
            is_header = text.startswith("▶")
            fs = 8.5 if is_header else 8
            fw = 'bold' if is_header else 'normal'
            col = '#0f172a' if is_header else '#475569'
            ax.text(x + 0.15, y - 0.7 - (i * 0.28), text, ha='left', va='center', 
                    fontsize=fs, color=col, weight=fw, zorder=4)

    # 1. PRESENTATION LAYER (Client)
    layer1_details = [
        "▶ USER INTERFACE (ส่วนผู้ใช้งาน)",
        " - Responsive Web Design (รองรับมือถือ/PC)",
        " - หน้าจอระบบยืม-เบิกครุภัณฑ์ (User Dashboard)",
        " - หน้าจอตรวจสอบสต็อกและสถิติ (Admin Dashboard)",
        " - หน้าจอประวัติยืม-คืนแนบรูปหลักฐานการคืน",
        "",
        "▶ TECHNOLOGIES & TOOLS",
        " - HTML5 / CSS3 (ดีไซน์กระจกโปร่งแสง Glassmorphism)",
        " - JavaScript (ES6) / CSS Variables (โหมดมืด/สว่าง)",
        " - FontAwesome Icons (ระบบสัญลักษณ์แจ้งเตือน)",
        " - Web Browsers (Chrome, Edge, Safari)"
    ]
    draw_layer(0.3, 7.3, 3.5, 3.8, "1. PRESENTATION LAYER (CLIENT)", layer1_details, border_indigo)

    # 2. APPLICATION LAYER (Web Server)
    layer2_details = [
        "▶ WEB APP PROCESSING (ส่วนประมวลผลหลัก)",
        " - การประมวลผลระบบสิทธิ์ Admin และ User",
        " - อนุมัติยืม-คืน / ระบบล้างคิวค้างเพื่อลดการหน่วง (Debounce)",
        " - จัดการหมวดหมู่ ตึก ชั้น และเลขห้องปฏิบัติการ",
        " - การแจ้งปัญหาชำรุดครุภัณฑ์ (Repair System)",
        "",
        "▶ SYSTEM ARCHITECTURE & HOSTING",
        " - Python 3.10+ / Flask Framework",
        " - Vercel Cloud Hosting (Serverless Deployment)",
        " - SQLAlchemy (ORM) / Database Connection Pooler",
        " - SMTP Email Server (จำลองการแจ้งเตือนส่งจดหมายด่วน)"
    ]
    draw_layer(4.25, 7.3, 3.5, 3.8, "2. APPLICATION LAYER (WEB SERVER)", layer2_details, border_blue)

    # 3. DATA LAYER (Database Server)
    layer3_details = [
        "▶ DATABASE MANAGEMENT (ระบบข้อมูล)",
        " - Supabase Cloud Database (PostgreSQL)",
        " - เก็บประวัติการยืม-คืน (ตาราง BorrowRequest)",
        " - เก็บประวัติการแจ้งซ่อม (ตาราง RepairRequest)",
        " - เก็บแผนผังห้องเรียน (ตาราง Building/Floor/Room)",
        " - ล็อกอินผู้ใช้และแอดมิน (ตาราง User)",
        "",
        "▶ DATA DICTIONARY STRUCTURE",
        " - Table Users (เก็บรหัสผ่านเข้ารหัส HASH)",
        " - Table Equipment (แยกครุภัณฑ์ Durable/Consumable)",
        " - เชื่อมโยงความสัมพันธ์ข้อมูลแบบ 1-to-Many (1:N)"
    ]
    draw_layer(8.2, 7.3, 3.5, 3.8, "3. DATA LAYER (DATABASE SERVER)", layer3_details, border_emerald)

    # Connecting Arrows & Flows
    # L1 -> L2 (Request)
    ax.annotate("", xy=(4.15, 5.0), xytext=(3.9, 5.0),
                arrowprops=dict(arrowstyle="->", color='#4f46e5', lw=1.5))
    ax.text(4.025, 5.15, "HTTPS Request\n(GET/POST)", ha='center', va='bottom', fontsize=7, color='#4f46e5')

    # L2 -> L1 (Response)
    ax.annotate("", xy=(3.9, 4.4), xytext=(4.15, 4.4),
                arrowprops=dict(arrowstyle="->", color='#64748b', lw=1.5))
    ax.text(4.025, 4.25, "HTTPS Response\n(HTML/JSON)", ha='center', va='top', fontsize=7, color='#64748b')

    # L2 -> L3 (Query)
    ax.annotate("", xy=(8.1, 5.0), xytext=(7.85, 5.0),
                arrowprops=dict(arrowstyle="->", color='#0ea5e9', lw=1.5))
    ax.text(7.975, 5.15, "SQL Query\n(SQLAlchemy ORM)", ha='center', va='bottom', fontsize=7, color='#0ea5e9')

    # L3 -> L2 (Result Set)
    ax.annotate("", xy=(7.85, 4.4), xytext=(8.1, 4.4),
                arrowprops=dict(arrowstyle="->", color='#10b981', lw=1.5))
    ax.text(7.975, 4.25, "Result Set\n(Data Rows)", ha='center', va='top', fontsize=7, color='#10b981')

    # External Component (SMTP Service Box at bottom center)
    rect_ext = patches.FancyBboxPatch((4.5, 2.5), 3.0, 1.1, boxstyle="round,pad=0.05",
                                      fc='#f8fafc', ec='#ef4444', lw=1.5, zorder=2)
    ax.add_patch(rect_ext)
    ax.text(6.0, 3.3, "EXTERNAL EMAIL SERVICE", ha='center', va='center', color='#b91c1c', weight='bold', fontsize=8.5)
    ax.text(6.0, 2.9, "SMTP Server (Gmail / Outlook)\nส่งเมลแจ้งเตือนส่งคืนอุปกรณ์ด่วนพิเศษ", ha='center', va='center', color='#475569', fontsize=7.5)

    # Connecting Application to External Service
    ax.annotate("", xy=(6.0, 2.6), xytext=(6.0, 3.4),
                arrowprops=dict(arrowstyle="<-", color='#ef4444', lw=1.2))
    ax.text(6.1, 3.0, "ส่งคำขอส่งอีเมล", ha='left', va='center', fontsize=7, color='#ef4444')

    # Save to local image paths and brain artifacts directory
    local_path = "static/img/diagrams/system_architecture.png"
    artifact_path = "C:/Users/ACER/.gemini/antigravity/brain/b500e698-6452-4be9-bee4-08259588db82/system_architecture.png"
    fig.savefig(local_path, bbox_inches='tight', dpi=300)
    fig.savefig(artifact_path, bbox_inches='tight', dpi=300)
    print(f"Generated System Architecture at: {local_path} and {artifact_path}")
    plt.close(fig)

if __name__ == "__main__":
    draw_system_architecture()
