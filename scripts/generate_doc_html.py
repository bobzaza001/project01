import os

HTML_CONTENT = """<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <title>เอกสารระบบ LAB Equipment System</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, CordiaUPC, AngsanaUPC, sans-serif;
            line-height: 1.6;
            color: #333333;
            max-width: 850px;
            margin: 0 auto;
            padding: 20px;
        }
        h1 {
            color: #1e3a8a;
            border-bottom: 2px solid #0ea5e9;
            padding-bottom: 10px;
            font-size: 24pt;
        }
        h2 {
            color: #0f172a;
            margin-top: 30px;
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 5px;
            font-size: 18pt;
        }
        h3 {
            color: #0369a1;
            font-size: 14pt;
        }
        p {
            font-size: 12pt;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
            margin-bottom: 15px;
            font-size: 11pt;
        }
        th, td {
            border: 1px solid #cbd5e1;
            padding: 10px;
            text-align: left;
            vertical-align: top;
        }
        th {
            background-color: #f1f5f9;
            color: #1e3a8a;
            font-weight: bold;
        }
        tr:nth-child(even) {
            background-color: #f8fafc;
        }
        img {
            max-width: 100%;
            height: auto;
            display: block;
            margin: 20px auto;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }
        .caption {
            text-align: center;
            font-style: italic;
            color: #64748b;
            font-size: 10pt;
            margin-top: -10px;
            margin-bottom: 20px;
        }
        .notice {
            background-color: #fffbeb;
            border-left: 4px solid #f59e0b;
            padding: 15px;
            margin: 20px 0;
            font-size: 11pt;
            color: #78350f;
            border-radius: 4px;
        }
        .badge-pass {
            background-color: #d1fae5;
            color: #065f46;
            padding: 2px 8px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 9pt;
            display: inline-block;
        }
    </style>
</head>
<body>

    <h1>📊 เอกสารแผนภาพ ข้อมูล และการทดสอบระบบ (LAB Equipment System)</h1>
    <div class="notice">
        <strong>💡 คำแนะนำสำหรับการนำเข้า Google Docs:</strong><br>
        1. เปิดไฟล์นี้ในเว็บเบราว์เซอร์ของคุณ (เช่น Google Chrome)<br>
        2. กดปุ่มคีย์ลัด <strong>Ctrl + A</strong> (เลือกทั้งหมด) จากนั้นกด <strong>Ctrl + C</strong> (คัดลอก)<br>
        3. เปิดหน้าเอกสารว่างใน <strong>Google Docs</strong> แล้วกด <strong>Ctrl + V</strong> (วาง)<br>
        * ระบบจะดึงแผนภาพ ตารางพจนานุกรมข้อมูล และตารางกรณีทดสอบระบบทั้งหมดเข้าไปอยู่ใน Google Docs ของคุณพร้อมจัดหน้าอัตโนมัติทันทีครับ!
    </div>

    <hr>

    <h2>1. แผนภาพบริบท (Context Diagram)</h2>
    <p>แผนภาพระดับบนสุด (DFD Level 0) แสดงขอบเขตการทำงานของระบบและการแลกเปลี่ยนกระแสข้อมูลระหว่างระบบจัดการครุภัณฑ์ห้องปฏิบัติการคอมพิวเตอร์กับหน่วยงานภายนอก (Entities) ได้แก่ ผู้ใช้ทั่วไป, ผู้ดูแลระบบ (Admin) และระบบส่งเมลเซิร์ฟเวอร์ (SMTP Server)</p>
    
    <img src="https://project01-psi-plum.vercel.app/static/img/diagrams/context_diagram.png" alt="Context Diagram">
    <p class="caption">รูปที่ 1.1: แผนภาพบริบทของระบบ (Context Diagram)</p>

    <h2>2. แผนภาพขั้นตอนการทำงานของระบบ (System Flowchart)</h2>
    <p>แผนภาพแสดงขั้นตอนการทำงาน ลำดับความคิด และทิศทางข้อมูลของระบบทั้งหมด ตั้งแต่การตรวจสอบสิทธิ์การเข้าใช้งาน การกดยื่นคำขอของนักศึกษา/อาจารย์ และขั้นตอนการพิจารณาตรวจสอบการยืม-คืนของแอดมิน</p>
    
    <img src="https://project01-psi-plum.vercel.app/static/img/diagrams/system_flowchart.png" alt="System Flowchart">
    <p class="caption">รูปที่ 2.1: แผนภาพขั้นตอนการทำงานของระบบ (System Flowchart)</p>

    <h2>3. แผนภาพความสัมพันธ์ของข้อมูล (ER Diagram)</h2>
    <p>แผนภาพแสดงสถาปัตยกรรมความสัมพันธ์ของฐานข้อมูลเชิงสัมพันธ์แบบ One-to-Many (1:N) ระหว่างข้อมูลผู้ใช้ ข้อมูลครุภัณฑ์และวัสดุ ข้อมูลใบคำร้องยืมคืน ข้อมูลประวัติการซ่อมแซม และข้อมูลแผนผังห้องปฏิบัติการ</p>
    
    <img src="https://project01-psi-plum.vercel.app/static/img/diagrams/er_diagram.png" alt="ER Diagram">
    <p class="caption">รูปที่ 3.1: แผนภาพแสดงความสัมพันธ์ของฐานข้อมูล (ER Diagram)</p>

    <h2>4. สถาปัตยกรรมระบบ (System Architecture - 3-Tier)</h2>
    <p>แผนภาพแสดงสถาปัตยกรรมโครงสร้างการพัฒนาระบบยืม-คืนครุภัณฑ์ โดยแบ่งเป็น 3 ชั้น (3-Tier Architecture) ได้แก่ Presentation Layer (ส่วนติดต่อผู้ใช้), Application Layer (เซิร์ฟเวอร์ประมวลผล Python/Flask โฮสต์บน Vercel), และ Data Layer (ส่วนจัดเก็บข้อมูลระบบ Supabase PostgreSQL)</p>
    
    <img src="https://project01-psi-plum.vercel.app/static/img/diagrams/system_architecture.png" alt="System Architecture">
    <p class="caption">รูปที่ 4.1: แผนภาพแสดงสถาปัตยกรรมการพัฒนาระบบแบบ 3-Tier (System Architecture)</p>

    <hr>

    <h2>5. พจนานุกรมข้อมูล (Data Dictionary) พร้อมตัวอย่างข้อมูล</h2>

    <h3>ตาราง 5.1: โครงสร้างตาราง User (ข้อมูลสมาชิก)</h3>
    <table>
        <thead>
            <tr>
                <th>ลำดับ</th>
                <th>ชื่อคอลัมน์ (Field)</th>
                <th>ประเภทข้อมูล (Type)</th>
                <th>คีย์ (Key)</th>
                <th>คำอธิบาย (Description)</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>1</td>
                <td>id</td>
                <td>INT</td>
                <td>PK</td>
                <td>รหัสรันอัตโนมัติประจำตัวผู้ใช้งาน</td>
            </tr>
            <tr>
                <td>2</td>
                <td>username</td>
                <td>VARCHAR(150)</td>
                <td>Unique</td>
                <td>ชื่อผู้ใช้งานสำหรับเข้าระบบ</td>
            </tr>
            <tr>
                <td>3</td>
                <td>full_name</td>
                <td>VARCHAR(200)</td>
                <td>-</td>
                <td>ชื่อ-นามสกุลจริงของผู้ใช้งาน</td>
            </tr>
            <tr>
                <td>4</td>
                <td>email</td>
                <td>VARCHAR(150)</td>
                <td>Unique</td>
                <td>อีเมลแอดเดรสสำหรับการส่งแจ้งเตือน</td>
            </tr>
            <tr>
                <td>5</td>
                <td>password_hash</td>
                <td>VARCHAR(256)</td>
                <td>-</td>
                <td>รหัสผ่านที่ผ่านการแฮชความปลอดภัย</td>
            </tr>
            <tr>
                <td>6</td>
                <td>role</td>
                <td>VARCHAR(20)</td>
                <td>-</td>
                <td>สิทธิ์การใช้งาน (admin หรือ user)</td>
            </tr>
            <tr>
                <td>7</td>
                <td>profile_image</td>
                <td>VARCHAR(200)</td>
                <td>-</td>
                <td>ชื่อไฟล์รูปโปรไฟล์</td>
            </tr>
            <tr>
                <td>8</td>
                <td>created_at</td>
                <td>DATETIME</td>
                <td>-</td>
                <td>วันและเวลาที่สร้างบัญชี</td>
            </tr>
        </tbody>
    </table>

    <p><strong>ตัวอย่างข้อมูลตาราง User:</strong></p>
    <table>
        <thead>
            <tr>
                <th>id</th>
                <th>username</th>
                <th>full_name</th>
                <th>email</th>
                <th>role</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>1</td>
                <td>admin1</td>
                <td>สมชาย ผู้ดูแลระบบ</td>
                <td>admin1@lab.ac.th</td>
                <td>admin</td>
            </tr>
            <tr>
                <td>2</td>
                <td>user1</td>
                <td>สมหญิง นักศึกษา</td>
                <td>user1@student.ac.th</td>
                <td>user</td>
            </tr>
            <tr>
                <td>3</td>
                <td>user2</td>
                <td>สมศักดิ์ บุคลากร</td>
                <td>user2@student.ac.th</td>
                <td>user</td>
            </tr>
            <tr>
                <td>4</td>
                <td>เอกวุฒิ</td>
                <td>เอกวุฒิ วงศ์มี</td>
                <td>68302040047@atcc.ac.th</td>
                <td>user</td>
            </tr>
            <tr>
                <td>5</td>
                <td>ธีรวัฒน์ ชินรัมย์</td>
                <td>ธีรวัฒน์ ชินรัมย์</td>
                <td>68302040056@atcc.ac.th</td>
                <td>user</td>
            </tr>
        </tbody>
    </table>

    <h3>ตาราง 5.2: โครงสร้างตาราง Equipment (ข้อมูลครุภัณฑ์/วัสดุ)</h3>
    <table>
        <thead>
            <tr>
                <th>ลำดับ</th>
                <th>ชื่อคอลัมน์ (Field)</th>
                <th>ประเภทข้อมูล (Type)</th>
                <th>คีย์ (Key)</th>
                <th>คำอธิบาย (Description)</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>1</td>
                <td>id</td>
                <td>INT</td>
                <td>PK</td>
                <td>รหัสรันอัตโนมัติประจำตัวอุปกรณ์</td>
            </tr>
            <tr>
                <td>2</td>
                <td>equipment_code</td>
                <td>VARCHAR(100)</td>
                <td>Unique</td>
                <td>รหัสสติ๊กเกอร์รหัสครุภัณฑ์เพื่อการตรวจสอบ</td>
            </tr>
            <tr>
                <td>3</td>
                <td>name</td>
                <td>VARCHAR(200)</td>
                <td>-</td>
                <td>ชื่อของอุปกรณ์ / ครุภัณฑ์</td>
            </tr>
            <tr>
                <td>4</td>
                <td>category</td>
                <td>VARCHAR(100)</td>
                <td>-</td>
                <td>หมวดหมู่ เช่น ไอที, เครื่องใช้ไฟฟ้า, ทั่วไป</td>
            </tr>
            <tr>
                <td>5</td>
                <td>status</td>
                <td>VARCHAR(50)</td>
                <td>-</td>
                <td>สถานะอุปกรณ์ (available, borrowed, maintenance)</td>
            </tr>
            <tr>
                <td>6</td>
                <td>total_quantity</td>
                <td>INT</td>
                <td>-</td>
                <td>จำนวนรวมทั้งหมดที่มีในระบบคลัง</td>
            </tr>
            <tr>
                <td>7</td>
                <td>available_quantity</td>
                <td>INT</td>
                <td>-</td>
                <td>จำนวนครุภัณฑ์ที่พร้อมให้กดยืมได้จริง</td>
            </tr>
            <tr>
                <td>8</td>
                <td>item_type</td>
                <td>VARCHAR(50)</td>
                <td>-</td>
                <td>ประเภทอุปกรณ์ (durable หรือ consumable)</td>
            </tr>
            <tr>
                <td>9</td>
                <td>is_borrowable</td>
                <td>BOOLEAN</td>
                <td>-</td>
                <td>สิทธิ์ในการกดยืมกลับบ้านได้ (True/False)</td>
            </tr>
            <tr>
                <td>10</td>
                <td>room_id</td>
                <td>INT</td>
                <td>FK</td>
                <td>รหัสเชื่อมโยงห้องเก็บครุภัณฑ์</td>
            </tr>
        </tbody>
    </table>

    <p><strong>ตัวอย่างข้อมูลตาราง Equipment:</strong></p>
    <table>
        <thead>
            <tr>
                <th>id</th>
                <th>equipment_code</th>
                <th>name</th>
                <th>status</th>
                <th>total_quantity</th>
                <th>available_quantity</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>2000</td>
                <td>EQ-248-011</td>
                <td>ชุดเครื่องคอมพิวเตอร์ ยี่ห้อ AR THUR CPU I5 4440 RAM 4 HD 500 GB</td>
                <td>available</td>
                <td>44</td>
                <td>44</td>
            </tr>
            <tr>
                <td>2001</td>
                <td>EQ-248-012</td>
                <td>ชุดเครื่องคอมพิวเตอร์ ยี่ห้อ HP รุ่น Compaq 8200 CPU I5 2500 RAM 4 HD 500 GB</td>
                <td>available</td>
                <td>1</td>
                <td>1</td>
            </tr>
            <tr>
                <td>2002</td>
                <td>EQ-248-013</td>
                <td>ชุดเครื่องคอมพิวเตอร์ ยี่ห้อ HP รุ่น Prodesk 400 g3 mt CPU I5-6500 RAM 12 HD 233 GB</td>
                <td>available</td>
                <td>1</td>
                <td>1</td>
            </tr>
            <tr>
                <td>2004</td>
                <td>EQ-248-015</td>
                <td>Monitor ยี่ห้อ HP ขนาด 20 นิ้ว สี ดำ</td>
                <td>available</td>
                <td>23</td>
                <td>23</td>
            </tr>
        </tbody>
    </table>

    <h3>ตาราง 5.3: โครงสร้างตาราง BorrowRequest (ประวัติการยืม-คืน)</h3>
    <table>
        <thead>
            <tr>
                <th>ลำดับ</th>
                <th>ชื่อคอลัมน์ (Field)</th>
                <th>ประเภทข้อมูล (Type)</th>
                <th>คีย์ (Key)</th>
                <th>คำอธิบาย (Description)</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>1</td>
                <td>id</td>
                <td>INT</td>
                <td>PK</td>
                <td>รหัสใบทำรายการคำร้อง</td>
            </tr>
            <tr>
                <td>2</td>
                <td>user_id</td>
                <td>INT</td>
                <td>FK</td>
                <td>รหัสผู้ทำรายการยืม</td>
            </tr>
            <tr>
                <td>3</td>
                <td>equipment_id</td>
                <td>INT</td>
                <td>FK</td>
                <td>รหัสครุภัณฑ์ที่ยืม</td>
            </tr>
            <tr>
                <td>4</td>
                <td>status</td>
                <td>VARCHAR(50)</td>
                <td>-</td>
                <td>สถานะการทำงาน (pending, approved, returned, etc.)</td>
            </tr>
            <tr>
                <td>5</td>
                <td>requested_at</td>
                <td>DATETIME</td>
                <td>-</td>
                <td>วันเวลาที่ส่งคำร้องเข้ามา</td>
            </tr>
            <tr>
                <td>6</td>
                <td>borrow_datetime</td>
                <td>DATETIME</td>
                <td>-</td>
                <td>วันเวลาที่แอดมินส่งมอบอุปกรณ์</td>
            </tr>
            <tr>
                <td>7</td>
                <td>return_due_datetime</td>
                <td>DATETIME</td>
                <td>-</td>
                <td>กำหนดส่งคืนอุปกรณ์</td>
            </tr>
            <tr>
                <td>8</td>
                <td>returned_at</td>
                <td>DATETIME</td>
                <td>-</td>
                <td>วันเวลาที่ส่งคืนจริงในคลัง</td>
            </tr>
            <tr>
                <td>9</td>
                <td>quantity</td>
                <td>INT</td>
                <td>-</td>
                <td>จำนวนที่ขอรับ</td>
            </tr>
            <tr>
                <td>10</td>
                <td>return_image_filename</td>
                <td>VARCHAR(200)</td>
                <td>-</td>
                <td>ชื่อรูปถ่ายหลักฐานยืนยันตอนส่งคืน</td>
            </tr>
        </tbody>
    </table>

    <p><strong>ตัวอย่างข้อมูลตาราง BorrowRequest:</strong></p>
    <table>
        <thead>
            <tr>
                <th>id</th>
                <th>user_id</th>
                <th>equipment_id</th>
                <th>quantity</th>
                <th>status</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>7</td>
                <td>2 (สมหญิง)</td>
                <td>1526</td>
                <td>1</td>
                <td>returned</td>
            </tr>
            <tr>
                <td>8</td>
                <td>2 (สมหญิง)</td>
                <td>1526</td>
                <td>1</td>
                <td>returned</td>
            </tr>
            <tr>
                <td>9</td>
                <td>2 (สมหญิง)</td>
                <td>1539</td>
                <td>1</td>
                <td>rejected</td>
            </tr>
            <tr>
                <td>10</td>
                <td>2 (สมหญิง)</td>
                <td>1530</td>
                <td>1</td>
                <td>returned</td>
            </tr>
        </tbody>
    </table>

    <hr>

    <h2>6. การทดสอบระบบ (System Testing - Black-box Testing)</h2>
    <p>ตารางทดสอบฟังก์ชันงานหลักของระบบด้วยวิธีการทดสอบแบบกล่องดำ (Black-box Testing) โดยครอบคลุมทั้งกรณีทดสอบปกติ (Positive Cases) และกรณีที่กรอกข้อมูลผิดพลาด/เกิดเงื่อนไขขัดแย้ง (Negative Cases)</p>

    <h3>ตาราง 6.1: กรณีทดสอบระบบ (Test Cases Table)</h3>
    <table>
        <thead>
            <tr>
                <th style="width: 8%;">ID</th>
                <th style="width: 15%;">ฟังก์ชันงาน (Feature)</th>
                <th style="width: 20%;">วัตถุประสงค์การทดสอบ</th>
                <th style="width: 17%;">ข้อมูลนำเข้า (Inputs)</th>
                <th style="width: 22%;">ผลลัพธ์ที่คาดหวัง (Expected)</th>
                <th style="width: 10%;">ผลการทดสอบจริง</th>
                <th style="width: 8%;">สถานะ</th>
            </tr>
        </thead>
        <tbody>
            <!-- Login -->
            <tr>
                <td>TC-01</td>
                <td>เข้าสู่ระบบ (Login)</td>
                <td>ทดสอบล็อกอินด้วยรหัสผ่านแอดมินที่ถูกต้อง (Positive)</td>
                <td>username: <code>admin1</code><br>password: <code>admin1234</code></td>
                <td>ระบบล็อกอินผ่าน และพาไปที่หน้า Admin Dashboard</td>
                <td>ล็อกอินผ่านสำเร็จและพาไปหน้าแอดมินแดชบอร์ด</td>
                <td><span class="badge-pass">PASS</span></td>
            </tr>
            <tr>
                <td>TC-02</td>
                <td>เข้าสู่ระบบ (Login)</td>
                <td>ทดสอบล็อกอินด้วยรหัสผ่านผู้ใช้งานที่ไม่ถูกต้อง (Negative)</td>
                <td>username: <code>user1</code><br>password: <code>wrong_pass</code></td>
                <td>ระบบไม่ให้เข้า พร้อมแสดงแจ้งเตือนรหัสผ่านไม่ถูกต้อง และค้างอยู่หน้าเดิม</td>
                <td>แสดงข้อความสีแดงเตือนชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง</td>
                <td><span class="badge-pass">PASS</span></td>
            </tr>
            
            <!-- Borrow Durable -->
            <tr>
                <td>TC-03</td>
                <td>ขอยืมครุภัณฑ์ (Borrow)</td>
                <td>ยื่นคำขอยืมครุภัณฑ์ (Durable) ข้อมูลถูกต้องครบถ้วน (Positive)</td>
                <td>อุปกรณ์: กล้อง Canon EOS<br>วันเวลายืม: <code>20/08/2026 09:00</code><br>จำนวนวัน: <code>3 วัน</code></td>
                <td>คำขอถูกส่งเข้าระบบ สถานะเป็น 'รอการอนุมัติ' (Pending)</td>
                <td>บันทึกคำขอเข้าระบบและเปลี่ยนการ์ดเป็นปุ่มรออนุมัติสีส้ม</td>
                <td><span class="badge-pass">PASS</span></td>
            </tr>
            <tr>
                <td>TC-04</td>
                <td>ขอยืมครุภัณฑ์ (Borrow)</td>
                <td>ยื่นคำขอยืมครุภัณฑ์ที่ของหมดคลังชั่วคราว (Negative)</td>
                <td>อุปกรณ์: แล็ปท็อป (สต็อกคงเหลือ = 0)</td>
                <td>ระบบไม่ให้ทำรายการ และแจ้งเตือน 'ครุภัณฑ์ชิ้นนี้ไม่ว่างในขณะนี้'</td>
                <td>แสดง Flash Warning ป้องกันไม่ให้กดส่งคำขอได้สำเร็จ</td>
                <td><span class="badge-pass">PASS</span></td>
            </tr>
            <tr>
                <td>TC-05</td>
                <td>ขอยืมครุภัณฑ์ (Borrow)</td>
                <td>ทดสอบการกดยื่นขอยืมซ้ำซ้อนในอุปกรณ์ชิ้นเดิม (Negative)</td>
                <td>กดยื่นขอยืมอุปกรณ์ชิ้นที่ตนเองมีสถานะ 'รออนุมัติ' ค้างอยู่แล้ว</td>
                <td>ระบบบล็อกการทำงาน และแจ้งเตือนคุณมีคำขอที่อยู่ระหว่างรออนุมัติแล้ว</td>
                <td>ระบบป้องกันไม่ให้ส่งคำขอซ้ำและแสดงข้อความแจ้งเตือน</td>
                <td><span class="badge-pass">PASS</span></td>
            </tr>
            <tr>
                <td>TC-06</td>
                <td>ขอยืมครุภัณฑ์ (Borrow)</td>
                <td>ทดสอบยื่นขอยืมโดยไม่ระบุวันเวลาเดินทางมารับของ (Negative)</td>
                <td>วันเวลายืม: <code>[ว่าง]</code><br>จำนวนวัน: <code>5 วัน</code></td>
                <td>ระบบบล็อกไม่ให้ส่ง และแสดงเตือน 'กรุณาระบุวันและเวลาที่ต้องการยืม'</td>
                <td>แสดง Flash Warning แจ้งเตือนเรื่องการกรอกวันเวลา</td>
                <td><span class="badge-pass">PASS</span></td>
            </tr>

            <!-- Approve Request -->
            <tr>
                <td>TC-07</td>
                <td>อนุมัติคำขอ (Approve)</td>
                <td>แอดมินกดอนุมัติคำขอยืมครุภัณฑ์ (Positive)</td>
                <td>กดปุ่มอนุมัติ (เช็คผ่าน POST)</td>
                <td>สถานะใบยืมเปลี่ยนเป็น 'อนุมัติแล้ว' (Approved), สต็อกอุปกรณ์ที่พร้อมให้ยืมลดลง 1 เครื่อง, ส่งอีเมลอนุมัติไปยังผู้ยืมทันที</td>
                <td>สถานะเปลี่ยน สต็อกคงเหลือลดลง และส่งเมลแจ้งอนุมัติสำเร็จ</td>
                <td><span class="badge-pass">PASS</span></td>
            </tr>
            
            <!-- Return Equipment -->
            <tr>
                <td>TC-08</td>
                <td>ส่งคืนครุภัณฑ์ (Return)</td>
                <td>ผู้ใช้กดคืนครุภัณฑ์โดยแนบไฟล์รูปถ่ายหลักฐานถูกต้อง (Positive)</td>
                <td>ไฟล์ภาพ: <code>receipt.png</code> (อัปโหลดหลักฐานส่งคืน)</td>
                <td>สถานะเปลี่ยนเป็น 'รอรับคืน' (Return pending), ชื่อไฟล์ภาพถูกจัดเก็บลงฐานข้อมูล, นำภาพไปแสดงในหน้าแอดมิน</td>
                <td>ระบบรับไฟล์รูป บันทึกลง Supabase และขึ้นแจ้งเตือนรอรับคืนฝั่งแอดมิน</td>
                <td><span class="badge-pass">PASS</span></td>
            </tr>
            <tr>
                <td>TC-09</td>
                <td>ส่งคืนครุภัณฑ์ (Return)</td>
                <td>ผู้ใช้กดส่งคืนโดยไม่เลือกอัปโหลดรูปภาพหลักฐาน (Negative)</td>
                <td>ไฟล์ภาพ: <code>[ว่าง]</code></td>
                <td>ระบบล็อกไม่ยอมให้ส่งคืน พร้อมแสดงข้อความเตือนให้แนบรูปภาพก่อน</td>
                <td>แสดงคำเตือนสีส้มระบุว่าจำเป็นต้องแนบไฟล์รูปหลักฐาน</td>
                <td><span class="badge-pass">PASS</span></td>
            </tr>

            <!-- Confirm Return -->
            <tr>
                <td>TC-10</td>
                <td>รับคืนเข้าคลัง (Confirm)</td>
                <td>แอดมินตรวจสอบรูปหลักฐานและกดยืนยันรับของเข้าคลัง (Positive)</td>
                <td>กดปุ่มรับของคืน (เช็คผ่าน POST)</td>
                <td>สถานะใบยืมเป็น 'คืนเรียบร้อย' (Returned), บันทึกเวลาคืนจริง, สต็อกครุภัณฑ์บวกกลับคืนคลัง 1 ชิ้น</td>
                <td>สถานะเปลี่ยน สต็อกเพิ่มกลับคืนคลัง และบันทึกเวลาส่งคืนสำเร็จ</td>
                <td><span class="badge-pass">PASS</span></td>
            </tr>

            <!-- Search and Filter -->
            <tr>
                <td>TC-11</td>
                <td>ค้นหาครุภัณฑ์ (Search)</td>
                <td>พิมพ์คำค้นหาชื่ออุปกรณ์ที่ต้องการค้นหา (Positive)</td>
                <td>คำค้นหา: <code>"กล้อง"</code></td>
                <td>ตัวกรองจาวาสคริปต์กรองการ์ดให้แสดงเฉพาะกล้อง โดยไม่มีความหน่วงขณะพิมพ์ (พิมพ์ลื่นไหลด้วยระบบ Debounce)</td>
                <td>หน้าจอกรองแสดงเฉพาะกล้องอย่างรวดเร็วและ Snappy ไม่หน่วงคอมพิวเตอร์</td>
                <td><span class="badge-pass">PASS</span></td>
            </tr>
            <tr>
                <td>TC-12</td>
                <td>ค้นหาครุภัณฑ์ (Search)</td>
                <td>พิมพ์ชื่ออุปกรณ์ที่ไม่มีอยู่ในระบบคลัง (Negative)</td>
                <td>คำค้นหา: <code>"ตู้เย็น"</code></td>
                <td>หน้าจอซ่อนการ์ดครุภัณฑ์ทั้งหมด และไม่แสดงรายการใดๆ</td>
                <td>การ์ดอุปกรณ์ทุกใบถูกซ่อนและไม่มีรายการแสดงผล</td>
                <td><span class="badge-pass">PASS</span></td>
            </tr>
        </tbody>
    </table>

</body>
</html>
"""

def generate_html_document():
    os.makedirs("scratch", exist_ok=True)
    file_path = "scratch/system_documentation.html"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT)
    print(f"Generated HTML Document at: {file_path}")

if __name__ == "__main__":
    generate_html_document()
