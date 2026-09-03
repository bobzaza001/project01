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
    
    // --- ระบบ Toast Notifications อัตโนมัติ (ลบ DOM ป้องกัน Memory Leak) ---
    const toastItems = document.querySelectorAll('.toast-item');
    toastItems.forEach(function(toast) {
        setTimeout(function() {
            dismissToast(toast);
        }, 4000);
    });
    
    // --- เพิ่ม animation ให้ตาราง rows ทีละแถว ---
    const rows = document.querySelectorAll('.fade-in');
    rows.forEach(function(row, index) {
        row.style.animationDelay = (index * 0.04) + 's';
    });

    // --- รัน Count-Up Animation สำหรับตัวเลขสถิติ (Hardware-Accelerated 60fps) ---
    initCountUpNumbers();

    // --- คลิกที่รูปภาพเพื่อเปิด Lightbox ขยายดูภาพเต็มตา ---
    initImageLightboxListeners();
});

// ==================== ระบบ Toast Notifications ====================
function dismissToast(el) {
    if (!el || el._isDismissing) return;
    el._isDismissing = true;
    el.classList.add('toast-dismissing');
    setTimeout(function() {
        if (el.parentNode) {
            el.parentNode.removeChild(el);
        }
    }, 350);
}

// ==================== ระบบ Image Lightbox (ขยายดูภาพคมชัด) ====================
function openLightbox(src, caption) {
    const modal = document.getElementById('imageLightboxModal');
    const img = document.getElementById('lightboxImg');
    const cap = document.getElementById('lightboxCaption');
    if (!modal || !img) return;

    img.src = src;
    img.alt = caption || 'Equipment Preview';
    if (cap) cap.innerText = caption || '';
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
}

function closeLightbox() {
    const modal = document.getElementById('imageLightboxModal');
    if (!modal) return;
    modal.style.display = 'none';
    document.body.style.overflow = '';
}

// ปิด Lightbox เมื่อกดปุ่ม ESC
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeLightbox();
    }
});

function initImageLightboxListeners() {
    document.addEventListener('click', function(e) {
        const target = e.target;
        if (target.tagName === 'IMG' && (target.classList.contains('eq-img') || target.classList.contains('table-img') || target.hasAttribute('data-preview'))) {
            openLightbox(target.src, target.alt || target.getAttribute('data-caption') || 'ภาพขยาย');
        }
    });
}

// ==================== ระบบ Count-Up Animation ตัวเลขสถิติ ====================
function initCountUpNumbers() {
    const counters = document.querySelectorAll('.count-up, .stat-number');
    counters.forEach(function(counter) {
        const target = parseInt(counter.getAttribute('data-target') || counter.innerText.replace(/[^0-9]/g, ''), 10);
        if (isNaN(target) || target <= 0) return;

        let start = 0;
        const duration = 1000; // 1 วินาที
        const startTime = performance.now();

        function updateNumber(now) {
            const elapsed = now - startTime;
            const progress = Math.min(elapsed / duration, 1);
            // Ease-Out Cubic formula
            const easeProgress = 1 - Math.pow(1 - progress, 3);
            const current = Math.floor(easeProgress * target);
            counter.innerText = current;

            if (progress < 1) {
                requestAnimationFrame(updateNumber);
            } else {
                counter.innerText = target;
            }
        }
        requestAnimationFrame(updateNumber);
    });
}

// ==================== ฟังก์ชันช่วยเหลือ ====================

function showFormError(message) {
    /** แสดงข้อความ error แบบ Toast Notification ชั่วคราว */
    const alertDiv = document.createElement('div');
    alertDiv.className = 'flash-message flash-danger toast-item';
    alertDiv.innerHTML = `
        <div class="toast-icon-wrapper">
            <i class="fas fa-circle-xmark"></i>
        </div>
        <div class="toast-text">${message}</div>
        <button type="button" class="flash-close">&times;</button>
        <div class="toast-timer-bar"></div>
    `;
    alertDiv.onclick = function() { dismissToast(this); };
    
    let container = document.getElementById('toastContainer');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toastContainer';
        container.className = 'flash-container';
        document.body.appendChild(container);
    }
    container.appendChild(alertDiv);
    
    setTimeout(function() {
        dismissToast(alertDiv);
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

// ==================== ระบบบีบอัดรูปภาพอัตโนมัติก่อนส่ง (Client-Side Image Auto-Compressor) ====================
/**
 * บีบอัดและปรับขนาดรูปภาพอัตโนมัติในเบราว์เซอร์ก่อนส่งขึ้น Server
 * ป้องกันปัญหา 413: PAYLOAD_TOO_LARGE ของ Vercel Serverless (ที่จำกัดขนาด 4.5MB)
 * รองรับกล้องมือถือความละเอียดสูง 10MB - 30MB ให้เหลือขนาดกะทัดรัด (~200KB - 400KB) โดยยังคมชัด 100%
 */
async function compressImageFile(file, maxWidth = 1280, maxHeight = 1280, quality = 0.82) {
    if (!file || !file.type.startsWith('image/')) return file;
    // ถ้าไฟล์เล็กกว่า 500KB อยู่แล้ว ไม่ต้องบีบอัดซ้ำ
    if (file.size <= 500 * 1024) return file;

    return new Promise((resolve) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = function(event) {
            const img = new Image();
            img.src = event.target.result;
            img.onload = function() {
                let width = img.width;
                let height = img.height;

                if (width > height) {
                    if (width > maxWidth) {
                        height = Math.round((height * maxWidth) / width);
                        width = maxWidth;
                    }
                } else {
                    if (height > maxHeight) {
                        width = Math.round((width * maxHeight) / height);
                        height = maxHeight;
                    }
                }

                const canvas = document.createElement('canvas');
                canvas.width = width;
                canvas.height = height;
                const ctx = canvas.getContext('2d');
                ctx.drawImage(img, 0, 0, width, height);

                canvas.toBlob(function(blob) {
                    if (!blob) {
                        resolve(file);
                        return;
                    }
                    const cleanName = file.name.replace(/\.[^/.]+$/, "") + ".jpg";
                    const compressedFile = new File([blob], cleanName, {
                        type: 'image/jpeg',
                        lastModified: Date.now()
                    });
                    resolve(compressedFile);
                }, 'image/jpeg', quality);
            };
            img.onerror = function() {
                resolve(file);
            };
        };
        reader.onerror = function() {
            resolve(file);
        };
    });
}

/** ผูกระบบบีบอัดเข้ากับ input[type="file"] ทุกช่องในระบบแบบอัตโนมัติ */
document.addEventListener('change', async function(e) {
    const input = e.target;
    if (input.tagName === 'INPUT' && input.type === 'file' && input.files && input.files[0]) {
        const file = input.files[0];
        if (file.type.startsWith('image/') && file.size > 500 * 1024) {
            // แสดง Toast แจ้งเตือนว่ากำลังปรับขนาดรูปภาพ
            const originalSizeMb = (file.size / (1024 * 1024)).toFixed(1);
            const compressed = await compressImageFile(file);
            const newSizeKb = Math.round(compressed.size / 1024);

            if (window.DataTransfer) {
                const dt = new DataTransfer();
                dt.items.add(compressed);
                input.files = dt.files;
            }
            console.log(`[Image Auto-Compress] ${file.name}: ${originalSizeMb}MB -> ${newSizeKb}KB`);
        }
    }
});

/** ดักจับตอน submit form เพื่อความปลอดภัย 100% ว่าไม่มีไฟล์รูปเกินขนาดหลุดขึ้น Serverless */
document.addEventListener('submit', async function(e) {
    const form = e.target;
    if (form.getAttribute('data-submitting') === 'true') return;
    
    const fileInputs = form.querySelectorAll('input[type="file"]');
    if (!fileInputs || fileInputs.length === 0) return;

    let hasOversized = false;
    for (const input of fileInputs) {
        if (input.files && input.files[0]) {
            const file = input.files[0];
            if (file.type.startsWith('image/') && file.size > 500 * 1024) {
                hasOversized = true;
                break;
            }
        }
    }

    if (hasOversized) {
        e.preventDefault();
        const submitBtn = form.querySelector('button[type="submit"]');
        let originalBtnHtml = '';
        if (submitBtn) {
            originalBtnHtml = submitBtn.innerHTML;
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> กำลังประมวลผลรูป...';
        }

        for (const input of fileInputs) {
            if (input.files && input.files[0]) {
                const file = input.files[0];
                if (file.type.startsWith('image/') && file.size > 500 * 1024) {
                    const compressed = await compressImageFile(file);
                    if (window.DataTransfer) {
                        const dt = new DataTransfer();
                        dt.items.add(compressed);
                        input.files = dt.files;
                    }
                }
            }
        }

        form.setAttribute('data-submitting', 'true');
        form.submit();
    }
}, true);
