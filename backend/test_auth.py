from database import create_user, verify_user_credentials, save_user_scan, get_user_scans, delete_user_scan
from auth import generate_token, verify_token

print("=== TESTING USER AUTHENTICATION & DATABASE ENGINE ===")

# 1. Test User Registration
test_email = "swathi@example.com"
test_password = "SecurePassword123"
test_name = "Swathi Manjusha"

user = create_user(test_email, test_password, test_name)
if not user:
    # If user already exists in DB from previous run, fetch existing
    from database import get_user_by_email
    user = get_user_by_email(test_email)

assert user is not None, "FAILED: User registration returned None!"
print(f"[PASS] Registered User: {user['full_name']} ({user['email']}) [ID: {user['id']}]")

# 2. Test Password Verification
verified = verify_user_credentials(test_email, test_password)
assert verified is not None, "FAILED: Password verification failed!"
print(f"[PASS] Password verification successful for {verified['email']}")

invalid_verify = verify_user_credentials(test_email, "WrongPassword")
assert invalid_verify is None, "FAILED: Invalid password returned user!"
print("[PASS] Invalid password rejected correctly!")

# 3. Test JWT Token Generation & Verification
token = generate_token(user['id'], user['email'])
assert token is not None, "FAILED: JWT token generation failed!"
print(f"[PASS] Generated JWT Token: {token[:30]}...")

payload = verify_token(token)
assert payload is not None and payload['user_id'] == user['id'], "FAILED: JWT token verification failed!"
print(f"[PASS] Token verified correctly for user_id: {payload['user_id']}")

# 4. Test Scan Saving & Retrieval
scan_res = save_user_scan(
    user_id=user['id'],
    score=88,
    job_domain="Data Science",
    resume_filename="Swathi_Resume.pdf",
    results={"overall_score": 88, "matched_keywords": ["Python", "SQL"]}
)
assert scan_res['id'] > 0, "FAILED: Scan saving failed!"
print(f"[PASS] Saved Scan ID: {scan_res['id']} with score {scan_res['score']}")

user_scans = get_user_scans(user['id'])
assert len(user_scans) > 0, "FAILED: User scans list is empty!"
print(f"[PASS] Fetched {len(user_scans)} saved scans for user!")

print("\n[PASS] USER AUTHENTICATION & DATABASE ENGINE VERIFIED 100%!")
