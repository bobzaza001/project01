/**
 * === สคริปต์สำหรับระบบยืม-คืนครุภัณฑ์ ===
 * จัดการ Client-side validation, Animation, Theme Toggle, และ UI interactions
 */

// ==================== ระบบสลับ Light / Dark Mode ====================

/** อัพเดตไอคอนปุ่ม toggle ให้ตรงกับ theme ปัจจุบัน */
function syncThemeIcons(theme) {
    var icons = document.querySelectorAll('.theme-icon');
    icons.forEach(function(icon) {
        if (theme === 'light') {
            icon.classList.remove('fa-moon');
            icon.classList.add('fa-sun');
        } else {
            icon.classList.remove('fa-sun');
            icon.classList.add('fa-moon');
        }
    });
}

/** สลับ theme พร้อม animation */
function toggleTheme() {
    var html = document.documentElement;
    var current = html.getAttribute('data-theme') || 'dark';
    var next = (current === 'dark') ? 'light' : 'dark';

    // เล่น animation หมุนไอคอน
    var icons = document.querySelectorAll('.theme-icon');
    icons.forEach(function(icon) {
        icon.classList.add('spin-out');
    });

    // หลัง animation spin-out เสร็จ → สลับ theme + เปลี่ยนไอคอน
    setTimeout(function() {
        html.setAttribute('data-theme', next);
        localStorage.setItem('theme', next);
        syncThemeIcons(next);

        icons.forEach(function(icon) {
            icon.classList.remove('spin-out');
            icon.classList.add('spin-in');
        });

        // ลบ class animation หลังเสร็จ
        setTimeout(function() {
            icons.forEach(function(icon) {
                icon.classList.remove('spin-in');
            });
        }, 500);
    }, 300);
}

// Sync icons & trigger Page Preloader Curtain Entrance
document.addEventListener('DOMContentLoaded', function() {
    var theme = document.documentElement.getAttribute('data-theme') || 'dark';
    syncThemeIcons(theme);

    // Initial Page Preloader Curtain Slide-up
    const preloader = document.getElementById('pagePreloader');
    if (preloader) {
        // ให้สายตามองเห็นโลโก้และหลอดโหลดประมาณ 650ms ก่อนเปิดม่าน
        setTimeout(function() {
            preloader.classList.add('slide-up');
            setTimeout(function() {
                preloader.style.display = 'none';
            }, 750);
        }, 650);
    }
});

// ==================== ระบบแสดง/ซ่อนรหัสผ่าน ====================
function togglePassword(fieldId) {
    /** สลับการแสดงผลรหัสผ่านระหว่าง text กับ password */
    const input = document.getElementById(fieldId);
    const icon = document.getElementById(fieldId + '-eye');
    
    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        input.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
}

// ==================== กรอกข้อมูลบัญชีทดสอบอัตโนมัติ (ลบออกเพื่อความปลอดภัย) ====================

// ==================== Validation ฟอร์ม ====================
document.addEventListener('DOMContentLoaded', function() {
    
    // --- ตรวจสอบฟอร์ม Login ---
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            const username = document.getElementById('username').value.trim();
            const password = document.getElementById('password').value;
            
            if (!username || !password) {
                e.preventDefault();
                showFormError('กรุณากรอกชื่อผู้ใช้และรหัสผ่าน');
                return;
            }
            
            // แสดง loading animation บนปุ่ม
            showLoading('loginBtn');
        });
    }
    
    // --- ตรวจสอบฟอร์มสมัครสมาชิก ---
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirm_password').value;
            const username = document.getElementById('username').value.trim();
            const email = document.getElementById('email').value.trim();
            const fullName = document.getElementById('full_name').value.trim();
            
            // ตรวจสอบว่ากรอกครบทุกช่อง
            if (!username || !email || !fullName || !password || !confirmPassword) {
                e.preventDefault();
                showFormError('กรุณากรอกข้อมูลให้ครบทุกช่อง');
                return;
            }
            
            // ตรวจสอบความยาวรหัสผ่าน
            if (password.length < 8) {
                e.preventDefault();
                showFormError('รหัสผ่านต้องมีอย่างน้อย 8 ตัวอักษร');
                return;
            }
            
            // ตรวจสอบรหัสผ่านตรงกัน
            if (password !== confirmPassword) {
                e.preventDefault();
                showFormError('รหัสผ่านและยืนยันรหัสผ่านไม่ตรงกัน');
                return;
            }
            
            // แสดง loading animation
            showLoading('registerBtn');
        });
        
        // --- แสดงความแข็งแรงของรหัสผ่านแบบ real-time ---
        const passwordInput = document.getElementById('password');
        if (passwordInput) {
            passwordInput.addEventListener('input', function() {
                updatePasswordStrength(this.value);
            });
        }
        
        // --- ตรวจสอบรหัสผ่านตรงกันแบบ real-time ---
        const confirmInput = document.getElementById('confirm_password');
        if (confirmInput) {
            confirmInput.addEventListener('input', function() {
                const password = document.getElementById('password').value;
                const matchDiv = document.getElementById('passwordMatch');
                
                if (this.value === '') {
                    matchDiv.textContent = '';
                } else if (this.value === password) {
                    matchDiv.textContent = '✅ รหัสผ่านตรงกัน';
                    matchDiv.style.color = '#16a34a';
                } else {
                    matchDiv.textContent = '❌ รหัสผ่านไม่ตรงกัน';
                    matchDiv.style.color = '#dc2626';
                }
            });
        }
    }
    
    // --- ปุ่ม Hamburger Menu (มือถือ) ---
    const navToggle = document.getElementById('navToggle');
    if (navToggle) {
        navToggle.addEventListener('click', function() {
            const navLinks = document.querySelector('.nav-links');
            navLinks.classList.toggle('active');
        });
    }
    
    // --- ซ่อน Flash Messages อัตโนมัติหลัง 5 วินาที ---
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(function(msg) {
        setTimeout(function() {
            msg.style.animation = 'slideIn 0.3s ease-out reverse';
            setTimeout(function() {
                msg.style.display = 'none';
            }, 300);
        }, 5000);
    });
    
    // --- เพิ่ม animation ให้ตาราง rows ทีละแถว ---
    const rows = document.querySelectorAll('.fade-in');
    rows.forEach(function(row, index) {
        row.style.animationDelay = (index * 0.05) + 's';
    });
});

// ==================== ฟังก์ชันช่วยเหลือ ====================

function showFormError(message) {
    /** แสดงข้อความ error แบบ alert ชั่วคราว */
    const alertDiv = document.createElement('div');
    alertDiv.className = 'flash-message flash-danger';
    alertDiv.innerHTML = '<i class="fas fa-exclamation-circle"></i> ' + message + '<span class="flash-close">&times;</span>';
    alertDiv.onclick = function() { this.remove(); };
    
    let container = document.querySelector('.flash-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'flash-container';
        document.body.appendChild(container);
    }
    container.appendChild(alertDiv);
    
    // ลบอัตโนมัติหลัง 4 วินาที
    setTimeout(function() {
        alertDiv.style.animation = 'slideIn 0.3s ease-out reverse';
        setTimeout(function() {
            alertDiv.remove();
        }, 300);
    }, 4000);
}

function showLoading(btnId) {
    /** แสดง loading spinner บนปุ่ม submit */
    const btn = document.getElementById(btnId);
    if (btn) {
        const btnText = btn.querySelector('.btn-text');
        const btnLoader = btn.querySelector('.btn-loader');
        if (btnText) btnText.style.display = 'none';
        if (btnLoader) btnLoader.style.display = 'inline-flex';
        btn.disabled = true;
        btn.style.opacity = '0.7';
    }
}

function hideLoading(btnId) {
    /** ซ่อน loading spinner บนปุ่ม submit */
    const btn = document.getElementById(btnId);
    if (btn) {
        const btnText = btn.querySelector('.btn-text');
        const btnLoader = btn.querySelector('.btn-loader');
        if (btnText) btnText.style.display = 'inline';
        if (btnLoader) btnLoader.style.display = 'none';
        btn.disabled = false;
        btn.style.opacity = '1';
    }
}


function updatePasswordStrength(password) {
    /** ประเมินและแสดงความแข็งแรงของรหัสผ่าน */
    const strengthDiv = document.getElementById('passwordStrength');
    if (!strengthDiv) return;
    
    let score = 0;
    if (password.length >= 8) score++;
    if (password.length >= 12) score++;
    if (/[A-Z]/.test(password)) score++;
    if (/[0-9]/.test(password)) score++;
    if (/[^A-Za-z0-9]/.test(password)) score++;
    
    const levels = [
        { color: '#dc2626', width: '20%' },
        { color: '#ea580c', width: '40%' },
        { color: '#eab308', width: '60%' },
        { color: '#16a34a', width: '80%' },
        { color: '#15803d', width: '100%' }
    ];
    
    if (password.length === 0) {
        strengthDiv.style.width = '0';
        return;
    }
    
    const level = levels[Math.min(score, levels.length - 1)];
    strengthDiv.style.width = level.width;
    strengthDiv.style.background = level.color;
    strengthDiv.style.height = '4px';
}
