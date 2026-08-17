import os
import re

template_dir = r"d:\equipment test\templates"

replacements = [
    (r"url_for\('login'\)", r"url_for('auth.login')"),
    (r"url_for\('register'\)", r"url_for('auth.register')"),
    (r"url_for\('logout'\)", r"url_for('auth.logout')"),
    (r"url_for\('forgot_password'\)", r"url_for('auth.forgot_password')"),
    (r"url_for\('dashboard'\)", r"url_for('user.dashboard')"),
    (r"url_for\('equipment_list'\)", r"url_for('user.equipment_list')"),
    (r"url_for\('add_equipment'\)", r"url_for('admin.add_equipment')"),
    (r"url_for\('edit_equipment'", r"url_for('admin.edit_equipment'"),
    (r"url_for\('delete_equipment'", r"url_for('admin.delete_equipment'"),
    (r"url_for\('approve_borrow'", r"url_for('admin.approve_borrow'"),
    (r"url_for\('reject_borrow'", r"url_for('admin.reject_borrow'"),
    (r"url_for\('send_warning'", r"url_for('admin.send_warning'"),
    (r"url_for\('request_borrow'", r"url_for('user.request_borrow'"),
    (r"url_for\('return_equipment'", r"url_for('user.return_equipment'"),
]

for filename in os.listdir(template_dir):
    if filename.endswith(".html"):
        filepath = os.path.join(template_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        new_content = content
        for old, new in replacements:
            new_content = re.sub(old, new, new_content)
            
        if new_content != content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Updated {filename}")

print("Done")
