// Mock Data with Images
let equipmentData = [
    { 
        id: 1, 
        name: 'Laptop Dell XPS 13', 
        description: 'แล็ปท็อปประสิทธิภาพสูง เหมาะสำหรับงานเขียนโปรแกรมและนำเสนอ', 
        total_quantity: 5, 
        available_quantity: 5,
        image: 'https://images.unsplash.com/photo-1593642632823-8f785ba67e45?auto=format&fit=crop&w=600&q=80'
    },
    { 
        id: 2, 
        name: 'Projector Epson', 
        description: 'โปรเจคเตอร์ 1080p ความสว่าง 3300 lumens เหมาะสำหรับห้องประชุม', 
        total_quantity: 2, 
        available_quantity: 2,
        image: 'https://images.unsplash.com/photo-1574717024653-61fd2cf4d44d?auto=format&fit=crop&w=600&q=80'
    },
    { 
        id: 3, 
        name: 'iPad Pro 12.9"', 
        description: 'แท็บเล็ตสำหรับนำเสนองาน พร้อม Apple Pencil', 
        total_quantity: 3, 
        available_quantity: 3,
        image: 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?auto=format&fit=crop&w=600&q=80'
    },
    { 
        id: 4, 
        name: 'Camera Canon EOS', 
        description: 'กล้อง DSLR บันทึกวิดีโอ 4K สำหรับงานกิจกรรม', 
        total_quantity: 1, 
        available_quantity: 1,
        image: 'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&w=600&q=80'
    },
    { 
        id: 5, 
        name: 'HDMI Cable (2m)', 
        description: 'สายสัญญาณ HDMI หัวทองเหลือง', 
        total_quantity: 20, 
        available_quantity: 20,
        image: 'https://images.unsplash.com/photo-1537498425277-c283d32ef9db?auto=format&fit=crop&w=600&q=80'
    }
];

let transactionsData = [];
let transactionIdCounter = 1;

document.addEventListener('DOMContentLoaded', () => {
    loadEquipment();
    loadTransactions();

    const borrowForm = document.getElementById('borrow-form');
    borrowForm.addEventListener('submit', handleBorrow);

    // Close modal when clicking outside of it
    window.onclick = function(event) {
        const modal = document.getElementById('equipment-modal');
        if (event.target == modal) {
            closeModal();
        }
    }
});

function loadEquipment() {
    const grid = document.getElementById('equipment-grid');
    const select = document.getElementById('equipment-select');
    
    grid.innerHTML = '';
    select.innerHTML = '<option value="">-- กรุณาเลือกอุปกรณ์ --</option>';

    equipmentData.forEach(eq => {
        // Populate Grid
        const item = document.createElement('div');
        item.className = 'equipment-item';
        // Add onclick to open modal
        item.onclick = () => openModal(eq.id);

        const isAvailable = eq.available_quantity > 0;
        const badgeClass = isAvailable ? 'available' : 'unavailable';
        const statusText = isAvailable ? `ว่าง: ${eq.available_quantity}/${eq.total_quantity}` : 'หมด';

        item.innerHTML = `
            <div class="eq-img-wrapper">
                <img src="${eq.image}" alt="${eq.name}">
            </div>
            <div class="eq-content">
                <h3>${eq.name}</h3>
                <p class="desc">${eq.description}</p>
                <div>
                    <span class="badge ${badgeClass}">${statusText}</span>
                </div>
            </div>
        `;
        grid.appendChild(item);

        // Populate Select (only if available)
        if (isAvailable) {
            const option = document.createElement('option');
            option.value = eq.id;
            option.textContent = `${eq.name} (ว่าง: ${eq.available_quantity})`;
            select.appendChild(option);
        }
    });
}

function loadTransactions() {
    const tbody = document.getElementById('transactions-body');
    tbody.innerHTML = '';

    const sortedTransactions = [...transactionsData].sort((a, b) => b.borrow_date - a.borrow_date);

    sortedTransactions.forEach(t => {
        const tr = document.createElement('tr');
        
        const borrowDate = t.borrow_date.toLocaleString('th-TH');
        const returnDate = t.return_date ? t.return_date.toLocaleString('th-TH') : '-';
        
        let statusHtml = '';
        if (t.status === 'borrowed') {
            statusHtml = `<button onclick="handleReturn(${t.id})" class="btn btn-small btn-return"><i class="fa-solid fa-rotate-left"></i> คืนอุปกรณ์</button>`;
        } else {
            statusHtml = `<span style="color: #137333; font-weight: bold;"><i class="fa-solid fa-check-circle"></i> คืนแล้ว<br><small style="color: #666;">${returnDate}</small></span>`;
        }

        const eq = equipmentData.find(e => e.id === t.equipment_id);
        const eqName = eq ? eq.name : 'Unknown';

        tr.innerHTML = `
            <td>#${t.id}</td>
            <td><strong>${eqName}</strong></td>
            <td>${t.borrower_name}</td>
            <td>${borrowDate}</td>
            <td>${statusHtml}</td>
        `;
        tbody.appendChild(tr);
    });
}

function handleBorrow(e) {
    e.preventDefault();
    
    const borrowerName = document.getElementById('borrower-name').value;
    const equipmentId = parseInt(document.getElementById('equipment-select').value);
    const msgDiv = document.getElementById('borrow-message');

    if (!equipmentId) {
        showMessage(msgDiv, 'กรุณาเลือกอุปกรณ์', 'error');
        return;
    }

    const eq = equipmentData.find(e => e.id === equipmentId);
    if (!eq || eq.available_quantity <= 0) {
        showMessage(msgDiv, 'อุปกรณ์ไม่ว่าง', 'error');
        return;
    }

    eq.available_quantity -= 1;
    
    transactionsData.push({
        id: transactionIdCounter++,
        equipment_id: equipmentId,
        borrower_name: borrowerName,
        borrow_date: new Date(),
        return_date: null,
        status: 'borrowed'
    });

    showMessage(msgDiv, 'ทำรายการยืมสำเร็จ!', 'success');
    document.getElementById('borrow-form').reset();
    
    loadEquipment();
    loadTransactions();
}

window.handleReturn = function(transactionId) {
    if (!confirm('ยืนยันการคืนอุปกรณ์?')) return;

    const t = transactionsData.find(tr => tr.id === transactionId);
    if (!t || t.status === 'returned') {
        alert('เกิดข้อผิดพลาด หรืออุปกรณ์ถูกคืนไปแล้ว');
        return;
    }

    t.status = 'returned';
    t.return_date = new Date();

    const eq = equipmentData.find(e => e.id === t.equipment_id);
    if (eq) {
        eq.available_quantity += 1;
    }

    alert('คืนอุปกรณ์สำเร็จ');
    loadEquipment();
    loadTransactions();
};

function showMessage(element, text, type) {
    element.innerHTML = type === 'success' ? `<i class="fa-solid fa-circle-check"></i> ${text}` : `<i class="fa-solid fa-circle-exclamation"></i> ${text}`;
    element.className = `message ${type}`;
    element.style.display = 'block';
    setTimeout(() => {
        element.style.display = 'none';
        element.className = 'message';
    }, 3000);
}

// Modal Functions
window.openModal = function(equipmentId) {
    const eq = equipmentData.find(e => e.id === equipmentId);
    if (!eq) return;

    document.getElementById('modal-image').src = eq.image;
    document.getElementById('modal-title').textContent = eq.name;
    document.getElementById('modal-desc').textContent = eq.description;
    
    const badge = document.getElementById('modal-badge');
    const isAvailable = eq.available_quantity > 0;
    badge.className = `badge ${isAvailable ? 'available' : 'unavailable'}`;
    badge.textContent = isAvailable ? `ว่างให้ยืม: ${eq.available_quantity} / ${eq.total_quantity} ชิ้น` : 'ถูกยืมจนหมดแล้ว';

    const modal = document.getElementById('equipment-modal');
    modal.style.display = 'flex';
    // Small delay to allow display:flex to apply before adding show class for animation
    setTimeout(() => {
        modal.classList.add('show');
    }, 10);
};

window.closeModal = function() {
    const modal = document.getElementById('equipment-modal');
    modal.classList.remove('show');
    // Wait for animation to finish before hiding
    setTimeout(() => {
        modal.style.display = 'none';
    }, 300);
};
