import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Set Font and Style
plt.rcParams['font.family'] = 'Tahoma'  # Tahoma is standard on Windows and supports Thai
plt.rcParams['figure.facecolor'] = '#ffffff'
plt.rcParams['axes.facecolor'] = '#ffffff'

# Create output directories
os.makedirs("static/img/diagrams", exist_ok=True)
os.makedirs("C:/Users/ACER/.gemini/antigravity/brain/b500e698-6452-4be9-bee4-08259588db82", exist_ok=True)

def draw_system_architecture():
    fig, ax = plt.subplots(figsize=(11, 10))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Title
    ax.text(5.5, 9.6, "โครงสร้างการพัฒนาระบบ (System Development Architecture - MVC Architecture)", 
            ha='center', va='center', fontsize=13, weight='bold', color='#0f172a')
    ax.text(5.5, 9.3, "ระบบจัดการยืม-คืนครุภัณฑ์ห้องปฏิบัติการคอมพิวเตอร์ (LAB Equipment Management System)", 
            ha='center', va='center', fontsize=9, color='#475569')

    # Styles
    box_color_user = '#f1f5f9'
    box_color_server = '#e0f2fe'
    box_color_db = '#dcfce7'
    box_color_ext = '#fef3c7'
    text_color = '#1e293b'
    line_color = '#64748b'

    # Helper function to draw simple icons
    def draw_box(x, y, w, h, title, subtitle="", color='#cbd5e1', is_header=False):
        rect = patches.FancyBboxPatch((x, y-h), w, h, boxstyle="round,pad=0.04",
                                      fc=color, ec=line_color, lw=1.2, zorder=3)
        ax.add_patch(rect)
        ax.text(x + w/2, y - 0.22, title, ha='center', va='center', fontsize=9, weight='bold', color=text_color, zorder=4)
        if subtitle:
            ax.text(x + w/2, y - 0.5, subtitle, ha='center', va='center', fontsize=7.5, color='#475569', zorder=4)

    # Helper function to draw speech bubble note
    def draw_note(x, y, w, h, title, items, color='#f8fafc', border_color='#94a3b8'):
        rect = patches.FancyBboxPatch((x, y-h), w, h, boxstyle="round,pad=0.04",
                                      fc=color, ec=border_color, lw=1, zorder=4)
        ax.add_patch(rect)
        ax.text(x + 0.15, y - 0.25, title, ha='left', va='center', fontsize=8, weight='bold', color='#0f172a', zorder=5)
        for i, item in enumerate(items):
            ax.text(x + 0.15, y - 0.55 - (i * 0.22), item, ha='left', va='center', fontsize=7.5, color='#475569', zorder=5)

    # Helper function for cloud connection labels
    def draw_cloud_connection(x, y, text_top, text_bottom):
        # Draw small cloud representation
        ellipse1 = patches.Ellipse((x, y), 0.7, 0.4, fc='#f1f5f9', ec=line_color, lw=0.8, zorder=3)
        ellipse2 = patches.Ellipse((x-0.2, y-0.1), 0.5, 0.3, fc='#f1f5f9', ec=line_color, lw=0.8, zorder=3)
        ellipse3 = patches.Ellipse((x+0.2, y-0.1), 0.5, 0.3, fc='#f1f5f9', ec=line_color, lw=0.8, zorder=3)
        ax.add_patch(ellipse1)
        ax.add_patch(ellipse2)
        ax.add_patch(ellipse3)
        # Bidirectional arrows
        ax.annotate("", xy=(x-0.45, y), xytext=(x+0.45, y), arrowprops=dict(arrowstyle="<->", color=line_color, lw=1))
        # Text
        ax.text(x, y+0.28, text_top, ha='center', va='bottom', fontsize=7, color='#475569')
        ax.text(x, y-0.28, text_bottom, ha='center', va='top', fontsize=7, color='#475569')

    # Draw Connections
    # PC Monitor <-> Web Server
    draw_cloud_connection(3.6, 7.3, "Request Message", "Response Message")
    # Admin <-> Web Server
    draw_cloud_connection(3.6, 5.0, "Request Message", "Response Message")
    # SmartPhone <-> Google OAuth
    draw_cloud_connection(3.6, 2.7, "Auth Token", "User Info")
    # Web Server <-> Database
    draw_cloud_connection(7.2, 7.3, "Request Message", "Response Message")
    # Web Server <-> SMTP
    draw_cloud_connection(7.2, 2.7, "Request Message", "Response Message")

    # 1. Actors & Devices (Left Column)
    # Users -> Monitor
    ax.text(1.2, 8.9, "ผู้ใช้งานทั่วไป\n(นักศึกษา / อาจารย์)", ha='center', va='center', fontsize=8, weight='bold')
    ax.annotate("", xy=(1.2, 8.1), xytext=(1.2, 8.5), arrowprops=dict(arrowstyle="->", color=line_color, lw=1))
    
    draw_box(0.4, 8.0, 1.6, 0.7, "Monitor", "Web Interface (PC)", box_color_user)
    
    # Website Admin -> Server
    ax.text(1.2, 5.6, "ผู้ดูแลระบบ\n(Website Admin)", ha='center', va='center', fontsize=8, weight='bold')
    ax.annotate("", xy=(1.2, 5.0), xytext=(1.2, 5.3), arrowprops=dict(arrowstyle="->", color=line_color, lw=1))
    
    # Smartphone User -> Smartphone Device
    ax.text(1.2, 3.4, "ผู้ใช้งานเคลื่อนที่\n(Mobile User)", ha='center', va='center', fontsize=8, weight='bold')
    ax.annotate("", xy=(1.2, 2.7), xytext=(1.2, 3.1), arrowprops=dict(arrowstyle="->", color=line_color, lw=1))
    
    draw_box(0.4, 2.6, 1.6, 0.7, "SmartPhone", "Mobile Web Page", box_color_user)

    # 2. Main Web Server (Center Column)
    draw_box(4.7, 7.8, 1.6, 1.2, "Web Server", "Vercel / Flask Server", box_color_server)
    ax.text(5.5, 7.2, "Application Layer", ha='center', va='center', fontsize=7, color='#64748b', style='italic')

    # Draw lines connecting devices to server
    # Monitor -> Server
    ax.plot([2.0, 2.8], [7.65, 7.65], color=line_color, lw=1)
    ax.plot([4.4, 4.7], [7.3, 7.3], color=line_color, lw=1)
    
    # Admin -> Server
    ax.plot([2.0, 2.8], [4.65, 4.65], color=line_color, lw=1)
    ax.plot([4.4, 4.7], [4.65, 4.65], color=line_color, lw=1)
    
    # Connect Admin line to server (vertical connection)
    ax.plot([4.7, 4.7], [4.65, 6.6], color=line_color, lw=1)

    # Mobile -> OAuth
    ax.plot([2.0, 2.8], [2.25, 2.25], color=line_color, lw=1)
    ax.plot([4.4, 4.7], [2.25, 2.25], color=line_color, lw=1)

    # 3. Database & Services (Right Column)
    draw_box(8.8, 7.8, 1.6, 1.2, "Database", "Supabase PostgreSQL", box_color_db)
    ax.text(9.6, 7.2, "Data Layer", ha='center', va='center', fontsize=7, color='#64748b', style='italic')
    
    # Server -> Database lines
    ax.plot([6.3, 6.4], [7.3, 7.3], color=line_color, lw=1)
    ax.plot([8.0, 8.8], [7.3, 7.3], color=line_color, lw=1)

    # External APIs (Bottom Right)
    draw_box(8.8, 3.2, 1.6, 1.2, "SMTP Mail Server", "Gmail SMTP Service", box_color_ext)
    
    # Server -> SMTP lines
    ax.plot([6.3, 6.4], [2.7, 2.7], color=line_color, lw=1)
    ax.plot([8.0, 8.8], [2.7, 2.7], color=line_color, lw=1)
    # Vertical connecting lines from Server down to SMTP line
    ax.plot([6.4, 6.4], [7.3, 2.7], color=line_color, lw=1)

    # External OAuth (Bottom Center)
    draw_box(4.7, 3.2, 1.6, 1.2, "Google OAuth", "Identity Provider", box_color_ext)

    # Note Popups (Speech bubbles matching original diagram)
    # Controller Note (Top Center)
    draw_note(4.5, 9.0, 2.0, 1.0, "AuthController", [
        "BorrowController",
        "RepairController",
        "EquipmentController"
    ], color='#f0fdfa', border_color='#5eead4')
    
    # Model Note (Top Right)
    draw_note(8.6, 9.0, 2.0, 1.0, "UserModel", [
        "EquipmentModel",
        "BorrowRequestModel",
        "RepairRequestModel"
    ], color='#f0fdfa', border_color='#5eead4')

    # OAuth Model Note (Bottom Center)
    draw_note(4.5, 1.8, 2.0, 0.7, "OAuth Controller", [
        "Google Sign-In API"
    ], color='#fffbeb', border_color='#fde047')

    # SMTP Controller Note (Bottom Right)
    draw_note(8.6, 1.8, 2.0, 0.7, "SMTP Controller", [
        "Mail Notification Service"
    ], color='#fffbeb', border_color='#fde047')

    # Save to local image paths and brain artifacts directory
    local_paths = [
        "static/img/diagrams/system_architecture.png",
        "static/img/diagrams/system_architecture_infographic.png",
        "static/img/diagrams/system_architecture_infographic.jpg"
    ]
    artifact_paths = [
        "C:/Users/ACER/.gemini/antigravity/brain/b500e698-6452-4be9-bee4-08259588db82/system_architecture.png",
        "C:/Users/ACER/.gemini/antigravity/brain/b500e698-6452-4be9-bee4-08259588db82/system_architecture_infographic.png"
    ]
    
    # Save fig helper
    for path in local_paths:
        fig.savefig(path, bbox_inches='tight', dpi=300)
    for path in artifact_paths:
        fig.savefig(path, bbox_inches='tight', dpi=300)
        
    print(f"Generated System Architecture Diagram successfully.")
    plt.close(fig)

if __name__ == "__main__":
    draw_system_architecture()
