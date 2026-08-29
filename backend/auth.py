import jwt
import datetime

SECRET_KEY = "ats_checker_v2_super_secret_jwt_key_harshini_2026"

def generate_token(user_id, email):
    """Generates a signed JWT token valid for 7 days."""
    payload = {
        "user_id": user_id,
        "email": email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_token(token):
    """Decodes JWT token and returns payload dict, or None if invalid/expired."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None
