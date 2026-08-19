import requests
import sys

BASE_URL = "https://project01-psi-plum.vercel.app"

def run_tests():
    print("🚀 Starting Web Verification Suite...")
    print(f"Target URL: {BASE_URL}\n")
    
    session = requests.Session()
    
    # Test 1: Check home page loading & redirect to login
    print("Test 1: Checking root path '/' loading and redirect to login...")
    try:
        r = session.get(f"{BASE_URL}/", allow_redirects=True)
        print(f"  [+] Status Code: {r.status_code}")
        print(f"  [+] Final URL: {r.url}")
        if r.status_code == 200 and "/login" in r.url:
            print("  ✅ PASS: Root path correctly redirects to login page.")
        else:
            print("  ❌ FAIL: Invalid redirect behavior.")
            return False
    except Exception as e:
        print(f"  ❌ FAIL: Connection error: {e}")
        return False
        
    # Test 2: Admin Login
    print("\nTest 2: Authenticating as Admin (admin1 / admin1234)...")
    try:
        login_data = {
            "username": "admin1",
            "password": "admin1234"
        }
        r = session.post(f"{BASE_URL}/login", data=login_data, allow_redirects=True)
        print(f"  [+] Login Response Status: {r.status_code}")
        print(f"  [+] Redirected URL: {r.url}")
        
        if r.status_code == 200 and "/admin/dashboard" in r.url:
            print("  ✅ PASS: Admin successfully authenticated and redirected to admin dashboard.")
        else:
            print("  ❌ FAIL: Admin login failed or redirected to wrong page.")
            return False
    except Exception as e:
        print(f"  ❌ FAIL: Admin login request failed: {e}")
        return False
        
    # Test 3: Admin Dashboard Loading
    print("\nTest 3: Checking Admin Dashboard access and data queries...")
    try:
        r = session.get(f"{BASE_URL}/admin/dashboard")
        print(f"  [+] Status Code: {r.status_code}")
        if r.status_code == 200 and "ผู้ดูแลระบบ" in r.text:
            print("  ✅ PASS: Admin dashboard loaded correctly with admin dashboard content.")
        else:
            print("  ❌ FAIL: Unable to fetch admin dashboard or missing admin context.")
            return False
    except Exception as e:
        print(f"  ❌ FAIL: Admin dashboard request failed: {e}")
        return False

    # Test 4: Admin Notification Settings Loading
    print("\nTest 4: Checking Notification Settings page...")
    try:
        r = session.get(f"{BASE_URL}/admin/notification-settings")
        print(f"  [+] Status Code: {r.status_code}")
        if r.status_code == 200 and "การแจ้งเตือนสำหรับการทำงานจริง" in r.text:
            print("  ✅ PASS: Notification settings page loaded with updated production warning text.")
        else:
            print("  ❌ FAIL: Notification settings page failed or has outdated texts.")
            return False
    except Exception as e:
        print(f"  ❌ FAIL: Notification settings request failed: {e}")
        return False

    # Test 5: Logout
    print("\nTest 5: Logging out Admin...")
    try:
        r = session.get(f"{BASE_URL}/logout", allow_redirects=True)
        print(f"  [+] Logout status: {r.status_code}")
        print(f"  [+] Final URL after logout: {r.url}")
        if r.status_code == 200 and "/login" in r.url:
            print("  ✅ PASS: Successfully logged out.")
        else:
            print("  ❌ FAIL: Logout redirect invalid.")
            return False
    except Exception as e:
        print(f"  ❌ FAIL: Logout request failed: {e}")
        return False

    # Test 6: Teacher Login
    print("\nTest 6: Authenticating as Teacher (teacher@atcc.ac.th)...")
    try:
        login_data = {
            "username": "teacher@atcc.ac.th",
            "password": "password123"
        }
        r = session.post(f"{BASE_URL}/login", data=login_data, allow_redirects=True)
        print(f"  [+] Login Response Status: {r.status_code}")
        print(f"  [+] Redirected URL: {r.url}")
        
        if r.status_code == 200 and "/user/dashboard" in r.url:
            print("  ✅ PASS: Teacher successfully authenticated and redirected to user dashboard.")
        else:
            print("  ❌ FAIL: Teacher login failed.")
            return False
    except Exception as e:
        print(f"  ❌ FAIL: Teacher login request failed: {e}")
        return False

    # Test 7: User Equipment Page Loading and Theme Test
    print("\nTest 7: Accessing Equipment Page & verifying filters...")
    try:
        r = session.get(f"{BASE_URL}/user/equipment")
        print(f"  [+] Status Code: {r.status_code}")
        if r.status_code == 200:
            print("  ✅ PASS: Equipment page loaded correctly.")
            if "borrowableFilter" in r.text:
                print("  ✅ PASS: Dropdown filter elements verified in HTML.")
            else:
                print("  ⚠️ WARNING: Could not find borrowableFilter element.")
        else:
            print("  ❌ FAIL: Equipment page failed to load.")
            return False
    except Exception as e:
        print(f"  ❌ FAIL: Equipment page request failed: {e}")
        return False

    # Test 8: User Contact Page Loading
    print("\nTest 8: Accessing Quick Contact Page...")
    try:
        r = session.get(f"{BASE_URL}/user/contact")
        print(f"  [+] Status Code: {r.status_code}")
        if r.status_code == 200 and "ช่องทางติดต่อด่วน" in r.text:
            print("  ✅ PASS: Contact page loads and displays contact methods successfully.")
        else:
            print("  ❌ FAIL: Contact page failed to load or has invalid content.")
            return False
    except Exception as e:
        print(f"  ❌ FAIL: Contact page request failed: {e}")
        return False

    print("\n🏆 Verification Suite Completed Successfully! All key endpoints are operational.")
    return True

if __name__ == "__main__":
    success = run_tests()
    if not success:
        sys.exit(1)
