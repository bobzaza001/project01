import os

HTML_CONTENT = """<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <title>เอกสารระบบ LAB Equipment System (บทที่ 3)</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, 'TH Sarabun New', CordiaUPC, AngsanaUPC, sans-serif;
            line-height: 1.6;
            color: #333333;
            max-width: 900px;
            margin: 0 auto;
            padding: 25px;
            background-color: #ffffff;
        }
        h1 {
            color: #1e3a8a;
            border-bottom: 2px solid #0ea5e9;
            padding-bottom: 10px;
            font-size: 22pt;
            text-align: center;
        }
        h2 {
            color: #0f172a;
            margin-top: 30px;
            border-bottom: 1px solid #cbd5e1;
            padding-bottom: 5px;
            font-size: 16pt;
        }
        h3 {
            color: #0369a1;
            font-size: 13pt;
            margin-top: 20px;
        }
        h4 {
            color: #334155;
            font-size: 12pt;
            margin-top: 15px;
        }
        p, li {
            font-size: 12pt;
            text-align: justify;
        }
        ul {
            margin-top: 5px;
            margin-bottom: 15px;
            padding-left: 25px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 12px;
            margin-bottom: 20px;
            font-size: 11pt;
        }
        th, td {
            border: 1px solid #94a3b8;
            padding: 8px 10px;
            text-align: left;
            vertical-align: middle;
        }
        th {
            background-color: #f1f5f9;
            color: #0f172a;
            font-weight: bold;
            text-align: center;
        }
        tr:nth-child(even) {
            background-color: #f8fafc;
        }
        .text-center {
            text-align: center;
        }
        .caption {
            text-align: center;
            font-style: italic;
            color: #64748b;
            font-size: 10.5pt;
            margin-top: 5px;
            margin-bottom: 15px;
        }
        .notice {
            background-color: #eff6ff;
            border-left: 4px solid #3b82f6;
            padding: 15px;
            margin: 20px 0;
            font-size: 11pt;
            color: #1e40af;
            border-radius: 4px;
        }
        .badge-pk {
            background-color: #fee2e2;
            color: #991b1b;
            font-weight: bold;
            padding: 2px 6px;
            border-radius: 4px;
        }
        .badge-fk {
            background-color: #e0e7ff;
            color: #3730a3;
            font-weight: bold;
            padding: 2px 6px;
            border-radius: 4px;
        }
        .badge-unique {
            background-color: #fef3c7;
            color: #92400e;
            font-weight: bold;
            padding: 2px 6px;
            border-radius: 4px;
        }
    </style>
</head>
<body>

    <h1>บทที่ 3<br>วิธีการดำเนินงานโครงงาน</h1>
    
    <div class="notice">
        <strong>💡 คำแนะนำสำหรับการคัดลอกลงเล่มรายงาน (Google Docs / MS Word):</strong><br>
        กด <strong>Ctrl + A</strong> (เลือกทั้งหมด) &gt; <strong>Ctrl + C</strong> (คัดลอก) &gt; วาง <strong>Ctrl + V</strong> ใน Google Docs หรือ Microsoft Word จะได้เนื้อหาและตารางที่จัดฟอร์แมตสวยงามพร้อมใช้งานทันทีครับ
    </div>

    <p>โครงงาน ระบบการยืมอุปกรณ์ห้องคอมพิวเตอร์ มีวิธีการดำเนินงาน ในการพัฒนา เว็บแอพพลิเคชัน ซึ่งได้ใช้หลักการ SDLC (Software Development Life Cycle) ซึ่งประกอบไปด้วย 7 ขั้นตอน ดังนี้</p>
    <ul>
        <li>3.1 การกำหนดปัญหาและการวางแผน</li>
        <li>3.2 การวิเคราะห์ความต้องการของระบบ</li>
        <li>3.3 การออกแบบระบบ</li>
        <li>3.4 การพัฒนาระบบ</li>
        <li>3.5 การทดสอบระบบ</li>
        <li>3.6 การติดตั้งและการนำไปใช้</li>
        <li>3.7 การบำรุงรักษาและการประเมินผล</li>
    </ul>

    <h2>3.1 การกำหนดปัญหาและการวางแผน</h2>
    
    <h3>3.1.1 การศึกษาและรวบรวมข้อมูล</h3>
    <p>ผู้จัดทำโครงงานได้ดำเนินการศึกษาและรวบรวมข้อมูลเพื่อวิเคราะห์ปัญหาของระบบงานเดิม โดยใช้เครื่องมือและวิธีการดังต่อไปนี้:</p>
    <ul>
        <li><strong>วิธีสัมภาษณ์ (Interview):</strong> ผู้จัดทำได้สัมภาษณ์เจ้าหน้าที่ดูแลห้องปฏิบัติการคอมพิวเตอร์จำนวน 2 คน และนักศึกษาที่เข้าใช้บริการห้องปฏิบัติการจำนวน 3 คน เพื่อสอบถามเกี่ยวกับขั้นตอน ปัญหา และความยากลำบากในการดำเนินการยืม-คืนครุภัณฑ์ในรูปแบบเดิม<br>
        <em>*ปัญหาที่พบจากการสัมภาษณ์:*</em> พบปัญหาว่าสมุดบันทึกข้อมูลมักสูญหายหรือค้นหาประวัติได้ยาก, นักศึกษาไม่ทราบจำนวนของคงเหลือที่ว่างให้ยืมจริงในคลัง ณ เวลานั้น, เจ้าหน้าที่ไม่สามารถควบคุมกำหนดส่งคืนได้สะดวกเพราะไม่มีระบบเตือน และเมื่อเกิดกรณีอุปกรณ์ชำรุดเสียหายมักไม่มีหลักฐานยืนยันสภาพอุปกรณ์ขณะส่งคืน</li>
        <li><strong>วิธีศึกษาเอกสารเดิม (Document Analysis):</strong> ผู้จัดทำได้ทำการรวบรวมและวิเคราะห์เอกสารที่เกี่ยวข้องในระบบงานเดิม เช่น สมุดจดบันทึกการยืม-คืนครุภัณฑ์ประจำห้องปฏิบัติการคอมพิวเตอร์, ไฟล์ตารางบันทึกรายชื่ออุปกรณ์ในโปรแกรม Microsoft Excel และใบคำร้องขอยืมอุปกรณ์แบบกระดาษ เพื่อทำความเข้าใจรูปแบบข้อมูลและนำมาใช้วิเคราะห์เพื่อออกแบบโครงสร้างระบบฐานข้อมูลใหม่ให้สอดคล้องกับการใช้งานจริง</li>
    </ul>

    <h3>3.1.2 การกำหนดขอบเขตระบบ</h3>
    <p>ระบบจัดการยืม-คืนครุภัณฑ์ห้องปฏิบัติการคอมพิวเตอร์ ได้แบ่งสิทธิ์การทำงานของผู้ใช้งานออกเป็น 2 กลุ่มอย่างชัดเจน ดังนี้:</p>
    
    <h4>3.1.2.1 ผู้ใช้งานทั่วไป / นักศึกษาและอาจารย์ (User)</h4>
    <ul>
        <li>สามารถสมัครสมาชิก เข้าสู่ระบบ และแก้ไขข้อมูลส่วนตัวรวมถึงภาพโปรไฟล์ของตนเองได้</li>
        <li>สามารถค้นหา คัดกรองข้อมูลครุภัณฑ์และวัสดุตามประเภท (ครุภัณฑ์ยืม-คืน หรือ วัสดุสิ้นเปลือง), หมวดหมู่ หรือสถานที่จัดเก็บ (อาคาร/ชั้น/เลขห้องปฏิบัติการ) ได้</li>
        <li>สามารถยื่นขอยืมครุภัณฑ์ (ยืม-คืนแบบกำหนดวันมารับและส่งคืน) หรือยื่นขอเบิกวัสดุสิ้นเปลือง (ตัดสต็อกทันทีและไม่ต้องนำมาคืน) ได้</li>
        <li>สามารถแจ้งส่งคืนครุภัณฑ์โดยการอัปโหลดไฟล์รูปถ่ายสภาพอุปกรณ์ขณะส่งคืน เพื่อใช้เป็นหลักฐานส่งให้ผู้ดูแลระบบตรวจสอบสภาพของก่อนรับคืน</li>
        <li>สามารถตรวจสอบประวัติการทำรายการยืม-คืน และติดตามสถานะคำร้อง (รออนุมัติ / อนุมัติแล้ว / รอรับคืน / คืนแล้ว / ปฏิเสธ) ของตนเองได้</li>
        <li>สามารถยื่นคำขอแจ้งซ่อมครุภัณฑ์เมื่อพบว่าอุปกรณ์ชำรุดเสียหาย พร้อมเขียนบันทึกอาการเบื้องต้นในระบบได้</li>
    </ul>

    <h4>3.1.2.2 ผู้ดูแลระบบ (Admin / Owner)</h4>
    <ul>
        <li>สามารถจัดการข้อมูลครุภัณฑ์และวัสดุ (เพิ่มคลังสินค้า, แก้ไขชื่อ, ปรับรหัสครุภัณฑ์, อัปเดตสถานะ, และอัปโหลดรูปภาพอุปกรณ์) ได้</li>
        <li>สามารถจัดการข้อมูลสถานที่จัดเก็บครุภัณฑ์ (เพิ่ม/ลบ/แก้ไขข้อมูลรายชื่ออาคาร, ชั้นเรียน, และห้องปฏิบัติการต่าง ๆ) ได้</li>
        <li>สามารถตรวจสอบรายละเอียดคำร้องและจัดการคำขอยืม-คืน (กดอนุมัติการยืม, ปฏิเสธคำขอพร้อมระบุเหตุผล, และกดอนุมัติการรับของคืนเข้าคลังหลังตรวจสอบความถูกต้องจากภาพถ่ายหลักฐานส่งคืน) ได้</li>
        <li>สามารถส่งอีเมลแจ้งเตือนถึงผู้ยืมได้โดยตรง ทั้งการกดส่งเมลแจ้งเตือนด่วนรายคน หรือการกดรันคำสั่งตรวจสอบค้างส่งคืน (Daily Scheduler) เพื่อให้อีเมลแจ้งเตือนภัยด่วนสีแดงที่มีสัญลักษณ์ส่งไปยังอีเมลผู้ยืมที่ค้างส่งครุภัณฑ์เกินกำหนดโดยอัตโนมัติ</li>
        <li>สามารถจัดการระบบคลังเก็บใบแจ้งซ่อมครุภัณฑ์ ตรวจสอบปัญหา และทำการอัปเดตสถานะการซ่อมบำรุงในระบบได้</li>
    </ul>

    <h2>3.2 การวิเคราะห์ความต้องการของระบบ</h2>

    <h3>3.2.1 แผนภาพขั้นตอนการทำงานของระบบ (System Flowchart)</h3>
    <p class="caption">ภาพที่ 3-1 แผนภาพขั้นตอนการทำงานของระบบ (System Flowchart)</p>
    <p>จากรูปที่ 3-1 แสดงขั้นตอนการทำงานเริ่มต้นจากการเข้าสู่ระบบ (Login) โดยระบุรหัสประจำตัว จากนั้นระบบจะทำการตรวจสอบสิทธิ์การเข้าใช้งาน (Check Role) เพื่อแยกการประมวลผล หากเข้าใช้งานในสิทธิ์ผู้ใช้ทั่วไป (User: นักศึกษา/อาจารย์) จะเข้าสู่การค้นหาและตรวจสอบครุภัณฑ์คงเหลือในคลัง แล้วกดยื่นเรื่องขอยืมครุภัณฑ์ (Durable) หรือขอกดเบิกวัสดุสิ้นเปลือง (Consumable) เพื่อส่งเรื่องให้แอดมินพิจารณาคำขอ หากระบบแจ้งผลปฏิเสธจะทำการส่งอีเมลและสิ้นสุดการทำงานทันที หากได้รับการอนุมัติ ผู้ยืมจะรับอุปกรณ์ไปใช้งาน และเมื่อต้องการส่งคืน ผู้ใช้จะต้องกดยื่นเรื่องส่งคืนพร้อมส่งภาพถ่ายหลักฐานสภาพการคืน เมื่อแอดมินกดยืนยันรับของเข้าคลังจึงจะเสร็จสิ้นการทำงาน ในทางกลับกัน หากเป็นสิทธิ์ผู้ดูแลระบบ (Admin) จะสามารถจัดการหน้าแดชบอร์ด จัดการคลังอุปกรณ์/สถานที่ และตรวจสอบรายการค้างส่งคืนเพื่อส่งจดหมายแจ้งเตือนเร่งคืนครุภัณฑ์โดยตรง</p>

    <h3>3.2.2 แผนภาพบริบท (Context Diagram)</h3>
    <p class="caption">ภาพที่ 3-2 แผนภาพบริบทของระบบการยืมอุปกรณ์ห้องคอมพิวเตอร์</p>
    <p>จากภาพที่ 3-2 แสดงแผนภาพบริบทของระบบจัดการยืม-คืนครุภัณฑ์ห้องปฏิบัติการคอมพิวเตอร์กับผู้ที่เกี่ยวข้องภายนอก ได้แก่ ผู้ใช้งานทั่วไป (User: นักศึกษา/อาจารย์), ผู้ดูแลระบบ (Admin) และระบบส่งอีเมล (SMTP Mail Server) โดยระบบนี้ทำหน้าที่เป็นศูนย์กลางในการรับข้อมูลคำขอยืมครุภัณฑ์หรือเบิกวัสดุสิ้นเปลือง และภาพหลักฐานส่งคืนครุภัณฑ์จากผู้ใช้งาน พร้อมทำหน้าที่ส่งข้อมูลรายงานสถิติและใบคำขอส่งถึงแอดมิน เพื่อพิจารณาอนุมัติหรือปฏิเสธคำขอ ตลอดจนทำหน้าที่ส่งคำขอส่งอีเมลไปยัง SMTP Server เพื่อดำเนินการส่งจดหมายแจ้งเตือนสถานะอนุมัติ/ปฏิเสธ หรือส่งอีเมลเตือนส่งคืนครุภัณฑ์เกินกำหนดด่วนพิเศษไปยังผู้ใช้งานโดยตรง</p>

    <h2>3.3 การออกแบบระบบ</h2>

    <h3>3.3.1 การออกแบบฐานข้อมูล</h3>

    <h4>3.3.1.1 แผนภาพความสัมพันธ์ของข้อมูล (ER-Diagram)</h4>
    <p class="caption">ภาพที่ 3-3 แผนภาพแสดงความสัมพันธ์ของระบบการยืมอุปกรณ์ห้องคอมพิวเตอร์</p>
    <p>จากภาพที่ 3-3 แสดงความสัมพันธ์ระหว่างเอนทิตี (Entities) ต่างๆ ในฐานข้อมูลของระบบจัดการยืม-คืนครุภัณฑ์ ตัวอย่างเช่น:</p>
    <ul>
        <li><strong>1. ความสัมพันธ์ระหว่างเอนทิตี User และ BorrowRequest:</strong> ผ่านความสัมพันธ์ 'ยื่นคำขอ' โดยเป็นความสัมพันธ์รูปแบบหนึ่งต่อกลุ่ม (One-to-Many หรือ 1:N) ซึ่งอธิบายได้ว่า ผู้ใช้งาน 1 คน สามารถส่งเรื่องขอยืม-คืนครุภัณฑ์ได้หลายรายการ ทั้งนี้ เอนทิตี User ประกอบด้วยคุณลักษณะ id (คีย์หลัก), username, full_name, email, password_hash, role, profile_image และ created_at ในขณะที่เอนทิตี BorrowRequest ประกอบด้วยคุณลักษณะ id (คีย์หลัก), status, borrow_datetime, return_due_datetime, borrow_days, quantity, damage_status, damage_note, return_image_filename, warning_message, overdue_notified, hidden_by_user, hidden_by_admin และมี user_id เป็นคีย์นอก (Foreign Key)</li>
        <li><strong>2. ความสัมพันธ์ระหว่างเอนทิตี Equipment และ BorrowRequest:</strong> ผ่านความสัมพันธ์ 'ถูกยืม' โดยเป็นความสัมพันธ์รูปแบบหนึ่งต่อกลุ่ม (One-to-Many หรือ 1:N) ซึ่งอธิบายได้ว่า อุปกรณ์ครุภัณฑ์ 1 ชิ้น สามารถมีประวัติการถูกยืมในคำขอต่าง ๆ ได้หลายรายการ ทั้งนี้ เอนทิตี Equipment ประกอบด้วยคุณลักษณะ id (คีย์หลัก), equipment_code, name, description, category, image_filename, total_quantity, available_quantity, item_type, is_borrowable, status และมี room_id เป็นคีย์นอก (Foreign Key) ในขณะที่เอนทิตี BorrowRequest มี equipment_id เป็นคีย์นอก (Foreign Key)</li>
        <li><strong>3. ความสัมพันธ์ระหว่างเอนทิตี Room และ Equipment:</strong> ผ่านความสัมพันธ์ 'เก็บรักษา' โดยเป็นความสัมพันธ์รูปแบบหนึ่งต่อกลุ่ม (One-to-Many หรือ 1:N) ซึ่งอธิบายได้ว่า ห้องปฏิบัติการคอมพิวเตอร์ 1 ห้อง สามารถใช้จัดเก็บครุภัณฑ์ได้หลายชิ้น ทั้งนี้ เอนทิตี Room ประกอบด้วยคุณลักษณะ id (คีย์หลัก), name และมี floor_id เป็นคีย์นอก (Foreign Key) ในขณะที่เอนทิตี Equipment มี room_id เป็นคีย์นอก (Foreign Key)</li>
        <li><strong>4. ความสัมพันธ์ของตารางแผนผังสถานที่ (Building, Floor, Room):</strong> ตาราง Building (id, name) มีความสัมพันธ์แบบ 1:N ไปยัง Floor (id, name, building_id) และตาราง Floor มีความสัมพันธ์แบบ 1:N ไปยัง Room (id, name, floor_id)</li>
        <li><strong>5. ความสัมพันธ์ของการแจ้งซ่อม (RepairRequest):</strong> ตาราง RepairRequest ประกอบด้วยคุณลักษณะ id (คีย์หลัก), issue_description, status, reported_at, resolved_at, admin_note และมีความสัมพันธ์เชื่อมโยงกับผู้แจ้งผ่าน user_id (FK) และอุปกรณ์ที่ชำรุดผ่าน equipment_id (FK) แบบ 1:N</li>
    </ul>

    <h4>3.3.1.2 พจนานุกรมข้อมูล (Data Dictionary)</h4>
    <p>ในการสร้างฐานข้อมูลนั้นสิ่งที่จำเป็นในการจัดทำ คือการกำหนดรายละเอียดของข้อมูลให้ชัดเจนโดยการทำพจนานุกรมข้อมูล เพื่อช่วยให้ผู้พัฒนาสามารถทำความเข้าใจข้อมูลที่เกี่ยวข้องได้ง่ายขึ้น ซึ่งจากแผนภาพความสัมพันธ์ระหว่างกลุ่มข้อมูลสามารถจำแนกข้อมูลออกมาเป็นตาราง 7 ตาราง ดังแสดงในตารางที่ 3-1 – 3-7 (โดยในส่วนของรหัสประจำตัวหรือ id ของแต่ละตาราง กำหนดชนิดข้อมูลเป็น VARCHAR เพื่อรองรับการเก็บข้อมูลได้ทั้งตัวเลขและตัวอักษร Alphanumeric):</p>

    <h3>ตารางที่ 3-1 โครงสร้างตาราง User (ข้อมูลสมาชิก / ผู้ใช้งานระบบ)</h3>
    <table>
        <thead>
            <tr>
                <th style="width: 8%;">No.</th>
                <th style="width: 20%;">Column</th>
                <th style="width: 15%;">Type</th>
                <th style="width: 10%;">Size</th>
                <th style="width: 35%;">Comment</th>
                <th style="width: 12%;">Role</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="text-center">1</td>
                <td><strong>id</strong></td>
                <td class="text-center">VARCHAR</td>
                <td class="text-center">50</td>
                <td>รหัสนักศึกษา (สำหรับ นศ.) / รหัสบัตร ปชช (สำหรับ ครู / บุคคล)</td>
                <td class="text-center"><span class="badge-pk">PK</span></td>
            </tr>
            <tr>
                <td class="text-center">2</td>
                <td><strong>username</strong></td>
                <td class="text-center">VARCHAR</td>
                <td class="text-center">150</td>
                <td>ชื่อผู้ใช้งานสำหรับเข้าสู่ระบบ</td>
                <td class="text-center"><span class="badge-unique">Unique</span></td>
            </tr>
            <tr>
                <td class="text-center">3</td>
                <td><strong>full_name</strong></td>
                <td class="text-center">VARCHAR</td>
                <td class="text-center">200</td>
                <td>ชื่อ-นามสกุลจริงของผู้ใช้งาน</td>
                <td class="text-center">-</td>
            </tr>
            <tr>
                <td class="text-center">4</td>
                <td><strong>email</strong></td>
                <td class="text-center">VARCHAR</td>
                <td class="text-center">150</td>
                <td>อีเมลแอดเดรสสำหรับการส่งแจ้งเตือน</td>
                <td class="text-center"><span class="badge-unique">Unique</span></td>
            </tr>
            <tr>
                <td class="text-center">5</td>
                <td><strong>password_hash</strong></td>
                <td class="text-center">VARCHAR</td>
                <td class="text-center">256</td>
                <td>รหัสผ่านที่ผ่านการแฮชความปลอดภัย</td>
                <td class="text-center">-</td>
            </tr>
            <tr>
                <td class="text-center">6</td>
                <td><strong>role</strong></td>
                <td class="text-center">VARCHAR</td>
                <td class="text-center">20</td>
                <td>สิทธิ์การใช้งาน (admin หรือ user)</td>
                <td class="text-center">-</td>
            </tr>
            <tr>
                <td class="text-center">7</td>
                <td><strong>student_id</strong></td>
                <td class="text-center">VARCHAR</td>
                <td class="text-center">20</td>
                <td>รหัสนักศึกษา 11 หลัก (เฉพาะกลุ่มผู้ใช้นักศึกษา)</td>
                <td class="text-center"><span class="badge-unique">Index</span></td>
            </tr>
            <tr>
                <td class="text-center">8</td>
                <td><strong>profile_image</strong></td>
                <td class="text-center">TEXT</td>
                <td class="text-center">-</td>
                <td>ข้อมูลรูปภาพโปรไฟล์ (Base64 Data URL หรือชื่อไฟล์)</td>
                <td class="text-center">-</td>
            </tr>
            <tr>
                <td class="text-center">9</td>
                <td><strong>created_at</strong></td>
                <td class="text-center">DATETIME</td>
                <td class="text-center">-</td>
                <td>วันและเวลาที่สร้างบัญชี</td>
                <td class="text-center">-</td>
            </tr>
        </tbody>
    </table>

    <h3>ตารางที่ 3-2 โครงสร้างตาราง Equipment (ข้อมูลครุภัณฑ์/วัสดุ)</h3>
    <table>
        <thead>
            <tr>
                <th style="width: 8%;">No.</th>
                <th style="width: 20%;">Column</th>
                <th style="width: 15%;">Type</th>
                <th style="width: 10%;">Size</th>
                <th style="width: 35%;">Comment</th>
                <th style="width: 12%;">Role</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="text-center">1</td>
                <td><strong>id</strong></td>
                <td class="text-center">VARCHAR</td>
                <td class="text-center">50</td>
                <td>รหัสประจำตัวอุปกรณ์ / ครุภัณฑ์</td>
                <td class="text-center"><span class="badge-pk">PK</span></td>
            </tr>
            <tr>
                <td class="text-center">2</td>
                <td><strong>equipment_code</strong></td>
                <td class="text-center">VARCHAR</td>
                <td class="text-center">100</td>
                <td>เลขครุภัณฑ์ (รหัสสติ๊กเกอร์ครุภัณฑ์เพื่อการตรวจสอบ)</td>
                <td class="text-center"><span class="badge-unique">Unique</span></td>
            </tr>
            <tr>
                <td class="text-center">3</td>
                <td><strong>name</strong></td>
                <td class="text-center">VARCHAR</td>
                <td class="text-center">200</td>
                <td>ชื่อของอุปกรณ์ / ครุภัณฑ์ / วัสดุ</td>
                <td class="text-center">-</td>
            </tr>
            <tr>
                <td class="text-center">4</td>
                <td><strong>description</strong></td>
                <td class="text-center">TEXT</td>
                <td class="text-center">-</td>
                <td>รายละเอียดและคุณสมบัติของอุปกรณ์</td>
                <td class="text-center">-</td>
            </tr>
            <tr>
                <td class="text-center">5</td>
                <td><strong>category</strong></td>
                <td class="text-center">VARCHAR</td>
                <td class="text-center">100</td>
                <td>หมวดหมู่ครุภัณฑ์ (เช่น ไอที, เครื่องใช้ไฟฟ้า, ทั่วไป)</td>
                <td class="text-center">-</td>
            </tr>
            <tr>
                <td class="text-center">6</td>
                <td><strong>image_filename</strong></td>
                <td class="text-center">TEXT</td>
                <td class="text-center">-</td>
                <td>ข้อมูลรูปภาพอุปกรณ์ (Base64 Data URL หรือชื่อไฟล์)</td>
                <td class="text-center">-</td>
            </tr>
            <tr>
                <td class="text-center">7</td>
                <td><strong>status</strong></td>
                <td class="text-center">VARCHAR</td>
                <td class="text-center">50</td>
                <td>สถานะอุปกรณ์ (available: พร้อมใช้งาน/ว่าง, borrowed: ถูกยืม, maintenance: ส่งซ่อม/ชำรุด, disposed: ตัดจำหน่าย)</td>
                <td class="text-center">-</td>
            </tr>
            <tr>
                <td class="text-center">8</td>
                <td><strong>total_quantity</strong></td>
                <td class="text-center">INT</td>
                <td class="text-center">-</td>
                <td>จำนวนรวมทั้งหมดที่มีในระบบคลัง</td>
                <td class="text-center">-</td>
            </tr>
            <tr>
                <td class="text-center">9</td>
                <td><strong>available_quantity</strong></td>
                <td class="text-center">INT</td>
                <td class="text-center">-</td>
                <td>จำนวนครุภัณฑ์ที่พร้อมให้กดยืมได้จริง</td>
                <td class="text-center">-</td>
            </tr>
            <tr>
                <td class="text-center">10</td>
                <td><strong>item_type</strong></td>
                <td class="text-center">VARCHAR</td>
                <td class="text-center">50</td>
                <td>ประเภทอุปกรณ์ (durable: ครุภัณฑ์ ยืม-คืน หรือ consumable: วัสดุสิ้นเปลือง เบิกจ่าย)</td>
                <td class="text-center">-</td>
            </tr>
            <tr>
                <td class="text-center">11</td>
                <td><strong>is_borrowable</strong></td>
                <td class="text-center">BOOLEAN</td>
                <td class="text-center">-</td>
                <td>สิทธิ์ในการกดยืม (True: ยืมได้ / False: ยืมไม่ได้)</td>
                <td class="text-center">-</td>
            </tr>
            <tr>
                <td class="text-center">12</td>
                <td><strong>room_id</strong></td>
                <td class="text-center">VARCHAR</td>
                <td class="text-center">50</td>
                <td>รหัสเชื่อมโยงห้องเก็บครุภัณฑ์ (เชื่อมโยงตาราง Room)</td>
                <td class="text-center"><span class="badge-fk">FK</span></td>
            </tr>
        </tbody>
    </table>

    <h3>ตารางที่ 3-3 โครงสร้างตาราง BorrowRequest (borrow_requests - ข้อมูลคำขอยืม-คืนครุภัณฑ์และเบิกวัสดุ)</h3>
    <table>
        <thead>
            <tr>
                <th style="width: 8%;">No.</th>
                <th style="width: 20%;">Column</th>
                <th style="width: 15%;">Type</th>
                <th style="width: 10%;">Size</th>
                <th style="width: 35%;">Comment</th>
                <th style="width: 12%;">Role</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="text-center">1</td>
                <td><strong>id</strong></td>
                <td class="text-center">VARCHAR</td>
                <td class="text-center">50</td>
                <td>รหัสใบทำรายการคำร้อง (รหัสคำขอยืม-คืน)</td>
                <td class="text-center"><span class="badge-pk">PK</span></td>
            </tr>
            <tr>
                <td class="text-center">2</td>
                <td><strong>user_id</strong></td>
                <td class="text-center">VARCHAR</td>
                <td class="text-center">50</td>
                <td>รหัสผู้ใช้งานที่ยื่นคำขอยืมหรือเบิก (เชื่อมโยงตาราง User)</td>
                <td class="text-center"><span class="badge-fk">FK</span></td>
            </tr>
            <tr>
                <td class="text-center">3</td>
                <td><strong>equipment_id</strong></td>
                <td class="text-center">VARCHAR</td>
                <td class="text-center">50</td>
                <td>รหัสครุภัณฑ์หรือวัสดุที่ต้องการยืม (เชื่อมโยงตาราง Equipment)</td>
                <td class="text-center"><span class="badge-fk">FK</span></td>
            </tr>
            <tr>
                <td class="text-center">4</td>
                <td><strong>status</strong></td>
                <td class="text-center">VARCHAR</td>
                <td class="text-center">50</td>
                <td>สถานะคำขอ (pending: รออนุมัติ, approved: อนุมัติแล้ว/กำลังยืม, return_pending: รอรับคืน, returned: คืนแล้ว, rejected: ปฏิเสธ)</td>
                <td class="text-center">-</td>
            </tr>
            <tr>
                <td class="text-center">5</td>
                <td><strong>requested_at</strong></td>
                <td class="text-center">DATETIME</td>
                <td class="text-center">-</td>
                <td>วันและเวลาที่ส่งคำร้องเข้ามาในระบบ</td>
                <td class="text-center">-</td>
            </tr>
            <tr>
                <td class="text-center">6</td>
                <td><strong>borrow_datetime</strong></td>
                <td class="text-center">DATETIME</td>
                <td class="text-center">-</td>
                <td>วันและเวลาที่ต้องการยืมหรือรับมอบอุปกรณ์</td>
                <td class="text-center">-</td>
            </tr>
            <tr>
                <td class="text-center">7</td>
                <td><strong>return_due_datetime</strong></td>
                <td class="text-center">DATETIME</td>
                <td class="text-center">-</td>
                <td>กำหนดวันและเวลาที่ต้องนำมาส่งคืน</td>
                <td class="text-center">-</td>
            </tr>
            <tr>
                <td class="text-center">8</td>
                <td><strong>approved_at</strong></td>
                <td class="text-center">DATETIME</td>
                <td class="text-center">-</td>
                <td>วันและเวลาที่แอดมินอนุมัติคำขอ</td>
                <td class="text-center">-</td>
            </tr>
            <tr>
                <td class="text-center">9</td>
                <td><strong>returned_at</strong></td>
                <td class="text-center">DATETIME</td>
                <td class="text-center">-</td>
                <td>วันและเวลาที่ส่งคืนอุปกรณ์เข้าคลังจริง</td>
                <td class="text-center">-</td>
            </tr>
            <tr>
                <td class="text-center">10</td>
                <td><strong>borrow_days</strong></td>
                <td class="text-center">INT</td>
                <td class="text-center">-</td>
                <td>จำนวนวันยืมอุปกรณ์ (ระบุโดยผู้ยืม 1-30 วัน)</td>
                <td class="text-center">-</td>
            </tr>
            <tr>
                <td class="text-center">11</td>
                <td><strong>quantity</strong></td>
                <td class="text-center">INT</td>
                <td class="text-center">-</td>
                <td>จำนวนที่ขอเบิก (สำหรับวัสดุสิ้นเปลือง)</td>
                <td class="text-center">-</td>
            </tr>
            <tr>
                <td class="text-center">12</td>
                <td><strong>damage_status</strong></td>
                <td class="text-center">VARCHAR</td>
                <td class="text-center">20</td>
                <td>สภาพความชำรุดของครุภัณฑ์หลังส่งคืน (normal: ปกติ, damaged: ชำรุด)</td>
                <td class="text-center">-</td>
            </tr>
            <tr>
                <td class="text-center">13</td>
                <td><strong>damage_note</strong></td>
                <td class="text-center">TEXT</td>
                <td class="text-center">-</td>
                <td>รายละเอียดอาการชำรุดเสียหายที่บันทึกตอนส่งคืน</td>
                <td class="text-center">-</td>
            </tr>
            <tr>
                <td class="text-center">14</td>
                <td><strong>return_image_filename</strong></td>
                <td class="text-center">TEXT</td>
                <td class="text-center">-</td>
                <td>ข้อมูลรูปภาพหลักฐานสภาพอุปกรณ์ตอนส่งคืน (Base64 Data URL หรือชื่อไฟล์)</td>
                <td class="text-center">-</td>
            </tr>
            <tr>
                <td class="text-center">15</td>
                <td><strong>warning_message</strong></td>
                <td class="text-center">TEXT</td>
                <td class="text-center">-</td>
                <td>ข้อความเตือนหรือเหตุผลการปฏิเสธจากผู้ดูแลระบบ</td>
                <td class="text-center">-</td>
            </tr>
            <tr>
                <td class="text-center">16</td>
                <td><strong>overdue_notified</strong></td>
                <td class="text-center">BOOLEAN</td>
                <td class="text-center">-</td>
                <td>เคยส่งอีเมลแจ้งเตือนค้างส่งเกินกำหนดแล้วหรือยัง (True/False)</td>
                <td class="text-center">-</td>
            </tr>
            <tr>
                <td class="text-center">17</td>
                <td><strong>hidden_by_user</strong></td>
                <td class="text-center">BOOLEAN</td>
                <td class="text-center">-</td>
                <td>ซ่อนรายการจากหน้าแดชบอร์ดของผู้ใช้ (True/False)</td>
                <td class="text-center">-</td>
            </tr>
            <tr>
                <td class="text-center">18</td>
                <td><strong>hidden_by_admin</strong></td>
                <td class="text-center">BOOLEAN</td>
                <td class="text-center">-</td>
                <td>ซ่อนรายการจากหน้าแดชบอร์ดของผู้ดูแลระบบ (True/False)</td>
                <td class="text-center">-</td>
            </tr>
        </tbody>
    </table>

    <h3>ตารางที่ 3-4 โครงสร้างตาราง RepairRequest (repair_requests - ข้อมูลคำขอแจ้งซ่อมครุภัณฑ์)</h3>
    <table>
        <thead>
            <tr>
                <th style="width: 8%;">No.</th>
                <th style="width: 20%;">Column</th>
                <th style="width: 15%;">Type</th>
                <th style="width: 10%;">Size</th>
                <th style="width: 35%;">Comment</th>
                <th style="width: 12%;">Role</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="text-center">1</td>
                <td><strong>id</strong></td>
                <td class="text-center">VARCHAR</td>
                <td class="text-center">50</td>
                <td>รหัสรายการแจ้งซ่อม</td>
                <td class="text-center"><span class="badge-pk">PK</span></td>
            </tr>
            <tr>
                <td class="text-center">2</td>
                <td><strong>equipment_id</strong></td>
                <td class="text-center">VARCHAR</td>
                <td class="text-center">50</td>
                <td>รหัสครุภัณฑ์ที่ต้องการแจ้งซ่อม (เชื่อมโยงตาราง Equipment)</td>
                <td class="text-center"><span class="badge-fk">FK</span></td>
            </tr>
            <tr>
                <td class="text-center">3</td>
                <td><strong>user_id</strong></td>
                <td class="text-center">VARCHAR</td>
                <td class="text-center">50</td>
                <td>รหัสผู้ใช้งานที่ยื่นเรื่องแจ้งซ่อม (เชื่อมโยงตาราง User)</td>
                <td class="text-center"><span class="badge-fk">FK</span></td>
            </tr>
            <tr>
                <td class="text-center">4</td>
                <td><strong>issue_description</strong></td>
                <td class="text-center">TEXT</td>
                <td class="text-center">-</td>
                <td>คำอธิบายรายละเอียดอาการชำรุดเสียหาย</td>
                <td class="text-center">-</td>
            </tr>
            <tr>
                <td class="text-center">5</td>
                <td><strong>status</strong></td>
                <td class="text-center">VARCHAR</td>
                <td class="text-center">50</td>
                <td>สถานะการแจ้งซ่อม (pending: รอดำเนินการ, in_progress: กำลังซ่อม, completed: ซ่อมเสร็จสิ้น)</td>
                <td class="text-center">-</td>
            </tr>
            <tr>
                <td class="text-center">6</td>
                <td><strong>reported_at</strong></td>
                <td class="text-center">DATETIME</td>
                <td class="text-center">-</td>
                <td>วันและเวลาที่ส่งรายงานแจ้งซ่อมเข้ามา</td>
                <td class="text-center">-</td>
            </tr>
            <tr>
                <td class="text-center">7</td>
                <td><strong>resolved_at</strong></td>
                <td class="text-center">DATETIME</td>
                <td class="text-center">-</td>
                <td>วันและเวลาที่ดำเนินการซ่อมแซมเสร็จสิ้น</td>
                <td class="text-center">-</td>
            </tr>
            <tr>
                <td class="text-center">8</td>
                <td><strong>admin_note</strong></td>
                <td class="text-center">TEXT</td>
                <td class="text-center">-</td>
                <td>บันทึกหมายเหตุเพิ่มเติมโดยแอดมินหรือช่างซ่อม</td>
                <td class="text-center">-</td>
            </tr>
        </tbody>
    </table>

    <h3>ตารางที่ 3-5 โครงสร้างตาราง Building (buildings - ข้อมูลอาคาร)</h3>
    <table>
        <thead>
            <tr>
                <th style="width: 8%;">No.</th>
                <th style="width: 20%;">Column</th>
                <th style="width: 15%;">Type</th>
                <th style="width: 10%;">Size</th>
                <th style="width: 35%;">Comment</th>
                <th style="width: 12%;">Role</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="text-center">1</td>
                <td><strong>id</strong></td>
                <td class="text-center">VARCHAR</td>
                <td class="text-center">50</td>
                <td>รหัสประจำตัวอาคาร</td>
                <td class="text-center"><span class="badge-pk">PK</span></td>
            </tr>
            <tr>
                <td class="text-center">2</td>
                <td><strong>name</strong></td>
                <td class="text-center">VARCHAR</td>
                <td class="text-center">100</td>
                <td>ชื่ออาคาร (เช่น อาคาร 1, อาคารปฏิบัติการคอมพิวเตอร์)</td>
                <td class="text-center">-</td>
            </tr>
        </tbody>
    </table>

    <h3>ตารางที่ 3-6 โครงสร้างตาราง Floor (floors - ข้อมูลชั้นของอาคาร)</h3>
    <table>
        <thead>
            <tr>
                <th style="width: 8%;">No.</th>
                <th style="width: 20%;">Column</th>
                <th style="width: 15%;">Type</th>
                <th style="width: 10%;">Size</th>
                <th style="width: 35%;">Comment</th>
                <th style="width: 12%;">Role</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="text-center">1</td>
                <td><strong>id</strong></td>
                <td class="text-center">VARCHAR</td>
                <td class="text-center">50</td>
                <td>รหัสประจำตัวชั้น</td>
                <td class="text-center"><span class="badge-pk">PK</span></td>
            </tr>
            <tr>
                <td class="text-center">2</td>
                <td><strong>name</strong></td>
                <td class="text-center">VARCHAR</td>
                <td class="text-center">50</td>
                <td>ชื่อหรือหมายเลขชั้น (เช่น ชั้น 1, ชั้น 2, ชั้น 3)</td>
                <td class="text-center">-</td>
            </tr>
            <tr>
                <td class="text-center">3</td>
                <td><strong>building_id</strong></td>
                <td class="text-center">VARCHAR</td>
                <td class="text-center">50</td>
                <td>รหัสอาคารที่ชั้นนี้สังกัดอยู่ (เชื่อมโยงตาราง Building)</td>
                <td class="text-center"><span class="badge-fk">FK</span></td>
            </tr>
        </tbody>
    </table>

    <h3>ตารางที่ 3-7 โครงสร้างตาราง Room (rooms - ข้อมูลห้องปฏิบัติการ/ห้องจัดเก็บ)</h3>
    <table>
        <thead>
            <tr>
                <th style="width: 8%;">No.</th>
                <th style="width: 20%;">Column</th>
                <th style="width: 15%;">Type</th>
                <th style="width: 10%;">Size</th>
                <th style="width: 35%;">Comment</th>
                <th style="width: 12%;">Role</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="text-center">1</td>
                <td><strong>id</strong></td>
                <td class="text-center">VARCHAR</td>
                <td class="text-center">50</td>
                <td>รหัสประจำตัวห้องปฏิบัติการ / ห้องจัดเก็บ</td>
                <td class="text-center"><span class="badge-pk">PK</span></td>
            </tr>
            <tr>
                <td class="text-center">2</td>
                <td><strong>name</strong></td>
                <td class="text-center">VARCHAR</td>
                <td class="text-center">100</td>
                <td>ชื่อหรือหมายเลขห้องปฏิบัติการ (เช่น Lab 301, Server Room)</td>
                <td class="text-center">-</td>
            </tr>
            <tr>
                <td class="text-center">3</td>
                <td><strong>floor_id</strong></td>
                <td class="text-center">VARCHAR</td>
                <td class="text-center">50</td>
                <td>รหัสชั้นที่ห้องนี้ตั้งอยู่ (เชื่อมโยงตาราง Floor)</td>
                <td class="text-center"><span class="badge-fk">FK</span></td>
            </tr>
        </tbody>
    </table>

    <h2>3.4 การพัฒนาระบบ</h2>
    <h3>3.4.1 เครื่องมือและเทคโนโลยีที่ใช้พัฒนา</h3>
    <ul>
        <li><strong>3.4.1.1 ภาษา Python (เวอร์ชัน 3.10+)</strong> ร่วมกับเฟรมเวิร์ก Flask สำหรับการประมวลผลระบบหลังบ้าน (Back-end) และใช้ HTML5, CSS3, JavaScript (ES6) ในการเขียนดีไซน์โครงสร้าง จัดแต่งรูปแบบความสวยงาม และฟังก์ชันการคัดกรองข้อมูลฝั่งหน้าบ้าน (Front-end)</li>
        <li><strong>3.4.1.2 ระบบจัดการฐานข้อมูลเชิงสัมพันธ์ PostgreSQL</strong> ผ่านคลาวด์เซอร์วิสของ Supabase Cloud Database เพื่อการเก็บรักษาความปลอดภัยของข้อมูลผู้ใช้งาน ข้อมูลพิกัดอุปกรณ์ และบันทึกคำร้องต่าง ๆ</li>
        <li><strong>3.4.1.3 Visual Studio Code</strong> (IDE สำหรับแก้ไขและเขียนซอร์สโค้ด), Git และ GitHub (ระบบควมคุมเวอร์ชันซอฟต์แวร์แบบแจกจ่าย), Vercel (คลาวด์โฮสติ้งในการปรับใช้งานจริง), และ Figma (สำหรับวางกรอบจำลองและดีไซน์อินเตอร์เฟสความสวยงามล่วงหน้า)</li>
    </ul>

    <h3>3.4.2 ตัวอย่างโครงสร้างการพัฒนาระบบ</h3>
    <p class="caption">ภาพที่ 3-11 สถาปัตยกรรมของระบบการยืมอุปกรณ์ห้องคอมพิวเตอร์</p>
    <p>จากภาพที่ 3-11: แสดงแผนภาพสถาปัตยกรรมระบบจัดการยืม-คืนครุภัณฑ์ห้องปฏิบัติการคอมพิวเตอร์แบบ 3 ระดับ (3-Tier Architecture) ที่ประกอบด้วยส่วนแสดงผลหน้าจอ (Presentation Layer) บนอุปกรณ์ที่หลากหลายทั้งคอมพิวเตอร์ แท็บเล็ต และสมาร์ทโฟน ผ่านเทคโนโลยี HTML5, CSS3, JavaScript, ส่วนประมวลผลคำสั่งระบบ (Application Layer) ผ่านเว็บเซิร์ฟเวอร์ด้วยภาษา Python และ Flask Framework โฮสต์บนคลาวด์ Vercel, และส่วนจัดการฐานข้อมูล (Data Layer) ด้วยระบบ PostgreSQL บนบริการ Supabase โดยทั้งสามส่วนทำงานประสานกันและรับส่งข้อมูลผ่านโปรโตคอล HTTPS และคำสั่ง SQL Query อย่างเป็นระบบเพื่อรองรับการทำงานทั้งหมดของโครงการ</p>

        <h2>3.5 การทดสอบระบบ (System Testing)</h2>
    <h3>3.5.1 ตารางกรณีทดสอบ (Test Case Table)</h3>
    <p class="caption">ตารางที่ 3-8 ตารางกรณีทดสอบระบบแยกตามกลุ่มบทบาทผู้ใช้งาน (Admin, Teacher, User)</p>
    <table>
        <thead>
            <tr>
                <th style="width: 8%;">รหัส</th>
                <th style="width: 14%;">กลุ่มผู้ใช้ / สิทธิ์</th>
                <th style="width: 18%;">ฟังก์ชันที่ทดสอบ</th>
                <th style="width: 20%;">ข้อมูลนำเข้า (Input)</th>
                <th style="width: 20%;">ผลลัพธ์ที่คาดหวัง</th>
                <th style="width: 20%;">ผลการทดสอบ</th>
            </tr>
        </thead>
        <tbody>
            <!-- กลุ่มที่ 1: การเข้าสู่ระบบและการควบคุมสิทธิ์ -->
            <tr style="background-color: #e2e8f0; font-weight: bold;">
                <td colspan="6" style="color: #0f172a;">1. การทดสอบการเข้าสู่ระบบและการควบคุมสิทธิ์ (Authentication & Role-Based Access Control)</td>
            </tr>
            <tr>
                <td class="text-center">TC-01</td>
                <td><strong style="color: #ef4444;">Admin</strong><br>(ผู้ดูแลระบบ)</td>
                <td>เข้าสู่ระบบผู้ดูแลระบบ<br>(Positive)</td>
                <td>username: admin1<br>password: admin1234</td>
                <td>ระบบยืนยันตัวตนสำเร็จ และนำทางไปยังหน้า <strong>Admin Dashboard</strong> มีเมนูจัดการคลัง, อนุมัติคำขอ, สรุปสถิติ, จัดการอาคาร/ห้อง</td>
                <td style="color: #059669; font-weight: bold;">ผ่าน (Pass)<br><span style="font-size: 0.8rem; font-weight: normal; color: #475569;">เข้าสู่หน้า Admin Dashboard พร้อมสิทธิ์จัดการทั้งหมด</span></td>
            </tr>
            <tr>
                <td class="text-center">TC-02</td>
                <td><strong style="color: #8b5cf6;">Teacher</strong><br>(อาจารย์/บุคลากร)</td>
                <td>เข้าสู่ระบบอาจารย์<br>(Positive)</td>
                <td>username: teacher<br>password: password123</td>
                <td>ระบบยืนยันตัวตนสำเร็จ และนำทางไปยังหน้า <strong>User Dashboard</strong> แสดงสถานะอาจารย์ มีสิทธิ์ยืมครุภัณฑ์เพื่อการเรียนการสอน, เบิกวัสดุ, แจ้งซ่อม</td>
                <td style="color: #059669; font-weight: bold;">ผ่าน (Pass)<br><span style="font-size: 0.8rem; font-weight: normal; color: #475569;">เข้าสู่หน้า Dashboard แสดงสิทธิ์อาจารย์ถูกต้อง</span></td>
            </tr>
            <tr>
                <td class="text-center">TC-03</td>
                <td><strong style="color: #0284c7;">User</strong><br>(นักเรียน/นักศึกษา)</td>
                <td>เข้าสู่ระบบนักศึกษา<br>(Positive)</td>
                <td>username: user1<br>password: user1234</td>
                <td>ระบบยืนยันตัวตนสำเร็จ และนำทางไปยังหน้า <strong>User Dashboard</strong> มีสิทธิ์ค้นหาอุปกรณ์, ขอยืมครุภัณฑ์, ขอเบิกวัสดุ, ส่งคืนพร้อมแนบรูป, ติดตามสถานะ</td>
                <td style="color: #059669; font-weight: bold;">ผ่าน (Pass)<br><span style="font-size: 0.8rem; font-weight: normal; color: #475569;">เข้าสู่หน้า Dashboard แสดงสถานะคำขอของนักศึกษา</span></td>
            </tr>
            <tr>
                <td class="text-center">TC-04</td>
                <td>ทุกกลุ่มผู้ใช้</td>
                <td>เข้าสู่ระบบด้วยรหัสผ่านผิด<br>(Negative)</td>
                <td>username: user1<br>password: wrong_pass</td>
                <td>ระบบปฏิเสธการเข้าใช้งาน พร้อมแสดงข้อความแจ้งเตือน <em>"ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง"</em> และคงอยู่ที่หน้าล็อกอินเดิม</td>
                <td style="color: #059669; font-weight: bold;">ผ่าน (Pass)<br><span style="font-size: 0.8rem; font-weight: normal; color: #475569;">ระบบบล็อกไม่ให้เข้า พร้อมแจ้งเตือนถูกต้อง</span></td>
            </tr>
            <tr>
                <td class="text-center">TC-05</td>
                <td>User / Teacher</td>
                <td>ป้องกันการเข้าถึงข้ามสิทธิ์<br>(Security Test)</td>
                <td>ล็อกอิน User/Teacher แล้วพิมพ์ URL ตรงเข้า <code>/admin/dashboard</code></td>
                <td>ระบบตรวจสอบสิทธิ์และปฏิเสธการเข้าถึง (Access Denied) โดย Redirect กลับไปยังหน้า User Dashboard พร้อมแจ้งเตือน</td>
                <td style="color: #059669; font-weight: bold;">ผ่าน (Pass)<br><span style="font-size: 0.8rem; font-weight: normal; color: #475569;">ระบบป้องกันการเข้าถึงหน้าแอดมินโดยไม่ได้รับอนุญาต 100%</span></td>
            </tr>

            <!-- กลุ่มที่ 2: ฟังก์ชันการทำงานของผู้ใช้งาน (User & Teacher) -->
            <tr style="background-color: #e2e8f0; font-weight: bold;">
                <td colspan="6" style="color: #0f172a;">2. การทดสอบฟังก์ชันการทำงานของผู้ใช้งาน (User & Teacher Functional Testing)</td>
            </tr>
            <tr>
                <td class="text-center">TC-06</td>
                <td>User / Teacher</td>
                <td>ค้นหาและคัดกรองอุปกรณ์<br>(Search & Filter)</td>
                <td>พิมพ์คำค้นหา <em>"กล้อง"</em> หรือเลือกตัวกรองตามอาคาร/ห้อง</td>
                <td>ตัวกรองจาวาสคริปต์กรองการ์ดอุปกรณ์ให้แสดงเฉพาะรายการที่ตรงเงื่อนไขอย่างรวดเร็ว (Debounce Filter)</td>
                <td style="color: #059669; font-weight: bold;">ผ่าน (Pass)<br><span style="font-size: 0.8rem; font-weight: normal; color: #475569;">แสดงรายการอุปกรณ์ถูกต้อง ไม่มีความหน่วง</span></td>
            </tr>
            <tr>
                <td class="text-center">TC-07</td>
                <td><strong style="color: #0284c7;">User</strong> (นักศึกษา)</td>
                <td>ยื่นคำขอยืมครุภัณฑ์<br>(Student Borrow)</td>
                <td>เลือกกล้อง DSLR, ระบุวันเวลารับของ และจำนวนวันยืม 3 วัน</td>
                <td>คำขอยืมถูกส่งเข้าระบบ สถานะเป็น <strong>'รอการอนุมัติ (Pending)'</strong> และแสดงในหน้ารายการคำขอของนักศึกษา</td>
                <td style="color: #059669; font-weight: bold;">ผ่าน (Pass)<br><span style="font-size: 0.8rem; font-weight: normal; color: #475569;">บันทึกคำขอลงฐานข้อมูล สถานะ Pending ถูกต้อง</span></td>
            </tr>
            <tr>
                <td class="text-center">TC-08</td>
                <td><strong style="color: #8b5cf6;">Teacher</strong> (อาจารย์)</td>
                <td>ยื่นขอยืมอุปกรณ์เพื่อการสอน<br>(Teacher Borrow)</td>
                <td>เลือกโปรเจกเตอร์/แล็ปท็อปเพื่อการสอน ระบุจำนวน 7 วัน</td>
                <td>คำขอถูกส่งเข้าระบบ พร้อมระบุวัตถุประสงค์การใช้เพื่อการเรียนการสอน สถานะเป็น <strong>'รอการอนุมัติ'</strong></td>
                <td style="color: #059669; font-weight: bold;">ผ่าน (Pass)<br><span style="font-size: 0.8rem; font-weight: normal; color: #475569;">บันทึกข้อมูลและส่งเรื่องให้อนุมัติถูกต้อง</span></td>
            </tr>
            <tr>
                <td class="text-center">TC-09</td>
                <td>User / Teacher</td>
                <td>ยื่นคำขอเบิกวัสดุสิ้นเปลือง<br>(Consumable Request)</td>
                <td>เลือกกระดาษพิมพ์/หมึก ระบุจำนวน 2 ชุด</td>
                <td>คำขอเบิกถูกส่งเข้าระบบ สถานะเป็น <strong>'รอการอนุมัติ'</strong> เพื่อรอแอดมินพิจารณาตัดสต็อก</td>
                <td style="color: #059669; font-weight: bold;">ผ่าน (Pass)<br><span style="font-size: 0.8rem; font-weight: normal; color: #475569;">บันทึกคำขอเบิกวัสดุเรียบร้อย</span></td>
            </tr>
            <tr>
                <td class="text-center">TC-10</td>
                <td>User / Teacher</td>
                <td>ยื่นขอยืมอุปกรณ์ที่ของหมดคลัง<br>(Negative)</td>
                <td>อุปกรณ์: แล็ปท็อป (สต็อกคงเหลือ = 0)</td>
                <td>ระบบบล็อกไม่ให้ทำรายการ และแจ้งเตือน <em>'ครุภัณฑ์ชิ้นนี้ไม่ว่างในขณะนี้'</em></td>
                <td style="color: #059669; font-weight: bold;">ผ่าน (Pass)<br><span style="font-size: 0.8rem; font-weight: normal; color: #475569;">ระบบป้องกันการยืมอุปกรณ์เกินสต็อก</span></td>
            </tr>
            <tr>
                <td class="text-center">TC-11</td>
                <td>User / Teacher</td>
                <td>ยื่นขอยืมซ้ำซ้อนในอุปกรณ์เดิม<br>(Negative)</td>
                <td>กดยื่นขอยืมอุปกรณ์ชิ้นที่ตนเองมีสถานะ 'รออนุมัติ' ค้างอยู่แล้ว</td>
                <td>ระบบบล็อกการทำงาน และแจ้งเตือน <em>'คุณมีคำขอที่อยู่ระหว่างรออนุมัติแล้ว'</em></td>
                <td style="color: #059669; font-weight: bold;">ผ่าน (Pass)<br><span style="font-size: 0.8rem; font-weight: normal; color: #475569;">ระบบป้องกันการส่งคำขอซ้ำซ้อนสำเร็จ</span></td>
            </tr>
            <tr>
                <td class="text-center">TC-12</td>
                <td>User / Teacher</td>
                <td>ยื่นขอยืมโดยไม่ระบุวันเวลา<br>(Negative)</td>
                <td>วันเวลายืม: [ว่าง], จำนวนวัน: 5 วัน</td>
                <td>ระบบบล็อกไม่ให้ส่งคำขอ และแจ้งเตือน <em>'กรุณาระบุวันและเวลาที่ต้องการยืม'</em></td>
                <td style="color: #059669; font-weight: bold;">ผ่าน (Pass)<br><span style="font-size: 0.8rem; font-weight: normal; color: #475569;">ระบบตรวจสอบความถูกต้องของข้อมูล (Validation)</span></td>
            </tr>
            <tr>
                <td class="text-center">TC-13</td>
                <td>User / Teacher</td>
                <td>แจ้งส่งคืนครุภัณฑ์พร้อมแนบรูป<br>(Return with Photo)</td>
                <td>กดคืนอุปกรณ์ + แนบไฟล์รูปถ่ายสภาพอุปกรณ์ตอนส่งคืน</td>
                <td>สถานะเปลี่ยนเป็น <strong>'รอรับคืน (Return pending)'</strong> รูปภาพถูกบันทึกลงฐานข้อมูล (Base64) และส่งไปยังหน้าแอดมิน</td>
                <td style="color: #059669; font-weight: bold;">ผ่าน (Pass)<br><span style="font-size: 0.8rem; font-weight: normal; color: #475569;">สถานะเปลี่ยนเป็นรอรับคืนและบันทึกภาพหลักฐานสำเร็จ</span></td>
            </tr>
            <tr>
                <td class="text-center">TC-14</td>
                <td>User / Teacher</td>
                <td>ส่งคืนโดยไม่แนบรูปถ่ายหลักฐาน<br>(Negative)</td>
                <td>กดส่งคืนอุปกรณ์โดยไม่เลือกไฟล์ภาพ</td>
                <td>ระบบบล็อกไม่ยอมให้ส่งคืน พร้อมแสดงข้อความเตือนให้แนบรูปภาพสภาพอุปกรณ์ก่อน</td>
                <td style="color: #059669; font-weight: bold;">ผ่าน (Pass)<br><span style="font-size: 0.8rem; font-weight: normal; color: #475569;">ระบบบังคับแนบรูปถ่ายสภาพของก่อนส่งคืน</span></td>
            </tr>
            <tr>
                <td class="text-center">TC-15</td>
                <td>User / Teacher</td>
                <td>ยื่นคำขอแจ้งซ่อมครุภัณฑ์<br>(Repair Request)</td>
                <td>เลือกอุปกรณ์ชำรุด + กรอกรายละเอียดอาการชำรุดเสียหาย</td>
                <td>ระบบบันทึกรายการแจ้งซ่อม สถานะเป็น <strong>'รอดำเนินการ (Pending)'</strong> และแจ้งเตือนในระบบคลังใบแจ้งซ่อมของแอดมิน</td>
                <td style="color: #059669; font-weight: bold;">ผ่าน (Pass)<br><span style="font-size: 0.8rem; font-weight: normal; color: #475569;">บันทึกรายการแจ้งซ่อมเข้าระบบเรียบร้อย</span></td>
            </tr>

            <!-- กลุ่มที่ 3: การบริหารจัดการของผู้ดูแลระบบ (Admin) -->
            <tr style="background-color: #e2e8f0; font-weight: bold;">
                <td colspan="6" style="color: #0f172a;">3. การทดสอบการบริหารจัดการของผู้ดูแลระบบ (Admin Management Testing)</td>
            </tr>
            <tr>
                <td class="text-center">TC-16</td>
                <td><strong style="color: #ef4444;">Admin</strong></td>
                <td>อนุมัติคำขอยืมครุภัณฑ์<br>(Approve Borrow)</td>
                <td>แอดมินกดปุ่มอนุมัติคำขอยืม (เช็คผ่าน POST)</td>
                <td>สถานะคำขอเปลี่ยนเป็น <strong>'อนุมัติแล้ว (Approved)'</strong>, สต็อกอุปกรณ์ที่พร้อมให้ยืมลดลง 1 ชิ้น, ระบบส่งอีเมลแจ้งเตือนไปยังผู้ยืมทันที</td>
                <td style="color: #059669; font-weight: bold;">ผ่าน (Pass)<br><span style="font-size: 0.8rem; font-weight: normal; color: #475569;">สถานะเปลี่ยนเป็นอนุมัติแล้ว ตัดสต็อก และส่งอีเมลสำเร็จ</span></td>
            </tr>
            <tr>
                <td class="text-center">TC-17</td>
                <td><strong style="color: #ef4444;">Admin</strong></td>
                <td>ปฏิเสธคำขอยืมพร้อมระบุเหตุผล<br>(Reject Borrow)</td>
                <td>แอดมินกดปฏิเสธคำขอ + ระบุเหตุผลการปฏิเสธ</td>
                <td>สถานะคำขอเปลี่ยนเป็น <strong>'ปฏิเสธ (Rejected)'</strong> และส่งอีเมลแจ้งเหตุผลไปยังผู้ยืม</td>
                <td style="color: #059669; font-weight: bold;">ผ่าน (Pass)<br><span style="font-size: 0.8rem; font-weight: normal; color: #475569;">สถานะเปลี่ยนเป็นปฏิเสธ และบันทึกเหตุผลในระบบ</span></td>
            </tr>
            <tr>
                <td class="text-center">TC-18</td>
                <td><strong style="color: #ef4444;">Admin</strong></td>
                <td>ตรวจสอบภาพและยืนยันรับของคืน<br>(Approve Return)</td>
                <td>แอดมินตรวจรูปภาพหลักฐานสภาพของ และกดยืนยันรับของคืนเข้าคลัง</td>
                <td>สถานะคำขอเปลี่ยนเป็น <strong>'คืนแล้ว (Returned)'</strong> และสต็อกอุปกรณ์ที่พร้อมให้ยืมเพิ่มคืนเข้าคลัง 1 ชิ้น</td>
                <td style="color: #059669; font-weight: bold;">ผ่าน (Pass)<br><span style="font-size: 0.8rem; font-weight: normal; color: #475569;">คืนสต็อกอุปกรณ์เข้าคลังและปิดรายการสมบูรณ์</span></td>
            </tr>
            <tr>
                <td class="text-center">TC-19</td>
                <td><strong style="color: #ef4444;">Admin</strong></td>
                <td>จัดการครุภัณฑ์และสถานที่<br>(CRUD Management)</td>
                <td>เพิ่มครุภัณฑ์ใหม่, แก้ไขข้อมูล, เพิ่มอาคาร/ชั้น/ห้อง พร้อมอัปโหลดรูปภาพ</td>
                <td>ข้อมูลและรูปภาพ (Base64) ถูกบันทึกลงฐานข้อมูล และแสดงผลในหน้าคลังอุปกรณ์ทันที</td>
                <td style="color: #059669; font-weight: bold;">ผ่าน (Pass)<br><span style="font-size: 0.8rem; font-weight: normal; color: #475569;">บันทึกข้อมูลและอัปโหลดรูปภาพแสดงผลสมบูรณ์</span></td>
            </tr>
            <tr>
                <td class="text-center">TC-20</td>
                <td><strong style="color: #ef4444;">Admin</strong></td>
                <td>ส่งออกรายงานสรุปข้อมูล<br>(Export Report)</td>
                <td>เลือกประเภทรายงานและช่วงเวลา กดดาวน์โหลด Excel หรือเปิดพิมพ์ PDF</td>
                <td>ระบบสร้างไฟล์ Excel (.xlsx) และหน้าพิมพ์เอกสาร PDF ได้อย่างถูกต้องตามช่วงเวลาที่เลือก</td>
                <td style="color: #059669; font-weight: bold;">ผ่าน (Pass)<br><span style="font-size: 0.8rem; font-weight: normal; color: #475569;">ดาวน์โหลด Excel และเปิดพิมพ์รายงาน PDF สำเร็จ 100%</span></td>
            </tr>
        </tbody>
    </table>

    <h2>3.6 การติดตั้งและการนำไปใช้</h2>
    <h3>3.6.1 สภาพแวดล้อมและคุณสมบัติขั้นต่ำของระบบ</h3>
    <h4>3.6.1.1 สำหรับเครื่องผู้ให้บริการ (Server Requirements):</h4>
    <ul>
        <li><strong>ระบบปฏิบัติการ:</strong> ใช้สภาพแวดล้อมระบบคลาวด์แบบ Serverless Node/Python Environment ของ Vercel (ฝั่งประมวลผลแอปพลิเคชัน) และระบบคลาวด์ Supabase (ฝั่งระบบจัดการฐานข้อมูล)</li>
        <li><strong>การประมวลผลและแพ็กเกจ:</strong> รองรับภาษา Python เวอร์ชัน 3.10+ พร้อมแพ็กเกจไลบรารี Flask, SQLAlchemy (ORM), pg8000 (โมดูลเชื่อมต่อฐานข้อมูล PostgreSQL) และระบบเซิร์ฟเวอร์ SMTP (สำหรับส่งเมลเตือนคืนเกินกำหนด)</li>
    </ul>

    <h4>3.6.1.2 สำหรับเครื่องผู้ใช้งาน (Client Requirements):</h4>
    <ul>
        <li><strong>อุปกรณ์หลัก:</strong> คอมพิวเตอร์ส่วนบุคคล (PC), แล็ปท็อป (Notebook), แท็บเล็ต (Tablet) หรือสมาร์ตโฟน (Smartphone)</li>
        <li><strong>เว็บเบราว์เซอร์:</strong> Google Chrome, Microsoft Edge, Mozilla Firefox หรือ Apple Safari (เวอร์ชันปัจจุบันที่อัปเดตล่าสุด)</li>
    </ul>

    <h3>3.6.2 การจัดทำคู่มือและฝึกอบรม</h3>
    <p>ผู้จัดทำได้จัดทำเอกสารแนะนำขั้นตอนการใช้งานระบบยืม-คืนอย่างละเอียด เพื่อแบ่งการใช้งานให้ผู้ที่เกี่ยวข้องศึกษาก่อนปฏิบัติงานจริง ดังนี้:</p>
    <ul>
        <li><strong>คู่มือการใช้งานสำหรับผู้ใช้ทั่วไป (User Manual):</strong> อธิบายวิธีการลงทะเบียนเข้าใช้ระบบ, วิธีการค้นหาครุภัณฑ์ตามแผนผังอาคาร/ชั้น/ห้องปฏิบัติการ, ขั้นตอนการกดยื่นคำขอยืมครุภัณฑ์หรือเบิกวัสดุสิ้นเปลือง และขั้นตอนการแนบถ่ายรูปหลักฐานขณะส่งของคืนผู้ดูแลระบบ</li>
        <li><strong>คู่มือการใช้งานสำหรับผู้ดูแลระบบ (Admin Manual):</strong> อธิบายการเข้าบริหารจัดการสต็อกครุภัณฑ์ (เพิ่ม/ลด/แก้ไข), การจัดการแผนผังสถานที่เก็บ, การตรวจหลักฐานภาพถ่าย และการยืนยันรับของคืน ตลอดจนการกดรันคำสั่ง Daily Schedule ส่งเมลแจ้งเตือนถึงผู้ยืมค้างกำหนด</li>
    </ul>

    <h2>3.7 การบำรุงรักษาและการประเมินผล</h2>
    <h3>3.7.1 การบำรุงรักษาและการสำรองข้อมูล</h3>
    <ul>
        <li><strong>การสำรองข้อมูลฐานข้อมูล (Database Backup Plan):</strong> กำหนดนโยบายความมั่นคงปลอดภัยในการสำรองข้อมูลเชิงสัมพันธ์ของระบบ (เช่น ข้อมูลบัญชีสมาชิก สต็อก และประวัติยืมคืน) โดยตั้งระบบอัตโนมัติบน Supabase Cloud ให้ทำการสำรองโครงสร้างข้อมูล (Database Snapshot & SQL Dump) ทุกวันอาทิตย์ เวลา 00.00 น. เพื่อรักษาระดับเสถียรภาพและป้องกันกรณีข้อมูลสูญหาย</li>
        <li><strong>การบำรุงรักษาประวัติระบบ (Log Maintenance & System Audit):</strong> กำหนดให้มีแผนการตรวจสอบสถิติการใช้งานและไฟล์บันทึกประวัติการส่งคำร้อง (Vercel Server Logs) ทุกสิ้นเดือน เพื่อลบไฟล์ประวัติขยะบนแคช ค้นหาจุดเกิดปัญหา (Errors) เพื่อปรับปรุงโครงสร้างเซิร์ฟเวอร์ให้อัตราความหน่วงต่ำที่สุดอย่างสม่ำเสมอ</li>
    </ul>

    <h3>3.7.2 การประเมินผลความพึงพอใจของระบบ</h3>
    <ul>
        <li><strong>กลุ่มตัวอย่างประเมิน:</strong> กลุ่มผู้ทดลองใช้งานระบบจัดการยืม-คืนจริง ได้แก่ นักเรียน/นักศึกษาสาขาคอมพิวเตอร์จำนวน 30 คน และผู้ดูแลระบบ/อาจารย์ประจำห้องปฏิบัติการคอมพิวเตอร์จำนวน 2 คน</li>
        <li><strong>เครื่องมือประเมินผล:</strong> ใช้แบบสอบถามวัดระดับความพึงพอใจ (Satisfaction Survey) ผ่านระบบออนไลน์ Google Forms โดยแบ่งหัวข้อการประเมินประสิทธิภาพออกเป็น 4 ด้านหลัก ได้แก่: (1) ด้านความสอดคล้องการทำงานตามความต้องการระบบ (Functional Requirements) (2) ด้านความง่ายต่อการเรียนรู้และเข้าใจในการใช้งาน (Usability & User-friendliness) (3) ด้านการออกแบบสไตล์ ความสวยงาม และการรองรับการแสดงผลโหมดมืด (User Interface Design) (4) ด้านความเร็ว ความเสถียร และอัตราการตอบสนองที่ไม่หน่วงค้าง (System Performance)</li>
        <li><strong>สถิติที่ใช้คิดคะแนน:</strong> ใช้ค่าเฉลี่ยเลขคณิต (Mean: x̄) และส่วนเบี่ยงเบนมาตรฐาน (Standard Deviation: S.D.) ในการคำนวณและแปลงระดับคะแนนความพึงพอใจออกเป็นเกณฑ์ 5 ระดับของ Likert Scale (พึงพอใจมากที่สุด - พึงพอใจน้อยที่สุด) เพื่อสรุปคุณภาพโครงงาน</li>
    </ul>

</body>
</html>
"""

def main():
    out_path = os.path.join(os.path.dirname(__file__), "..", "scratch", "system_documentation.html")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT)
    print(f"Generated {out_path} successfully!")

if __name__ == "__main__":
    main()
