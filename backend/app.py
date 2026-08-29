import io
import traceback
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

from resume_parser import extract_text_from_pdf
from keyword_extractor import extract_keywords
from ats_engine import calculate_ats_score
from pdf_generator import build_single_column_ats_pdf
from database import create_user, verify_user_credentials, get_user_by_id, save_user_scan, get_user_scans, delete_user_scan
from auth import generate_token, verify_token

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

def get_current_user():
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        payload = verify_token(token)
        if payload and "user_id" in payload:
            return get_user_by_id(payload["user_id"])
    return None

@app.route("/")
def home():
    return jsonify({"message": "ATS Checker v2 Backend Running with SQLite Database Auth Engine"})

# --- AUTHENTICATION ROUTES ---

@app.route("/api/auth/register", methods=["POST"])
def register():
    try:
        data = request.json or {}
        email = data.get("email", "").strip()
        password = data.get("password", "").strip()
        full_name = data.get("full_name", "").strip()
        
        if not email or not password or not full_name:
            return jsonify({"error": "Full Name, Email, and Password are required."}), 400
            
        if len(password) < 6:
            return jsonify({"error": "Password must be at least 6 characters long."}), 400

        user = create_user(email, password, full_name)
        if not user:
            return jsonify({"error": "An account with this email address already exists."}), 400

        token = generate_token(user["id"], user["email"])
        return jsonify({
            "message": "Account created successfully!",
            "token": token,
            "user": user
        }), 201
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

@app.route("/api/auth/login", methods=["POST"])
def login():
    try:
        data = request.json or {}
        email = data.get("email", "").strip()
        password = data.get("password", "").strip()
        
        if not email or not password:
            return jsonify({"error": "Email and Password are required."}), 400

        user = verify_user_credentials(email, password)
        if not user:
            return jsonify({"error": "Invalid email or password. Please try again."}), 401

        token = generate_token(user["id"], user["email"])
        return jsonify({
            "message": "Logged in successfully!",
            "token": token,
            "user": user
        })
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

@app.route("/api/auth/me", methods=["GET"])
def get_me():
    user = get_current_user()
    if not user:
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify({"user": user})

@app.route("/api/user/scans", methods=["GET"])
def list_scans():
    user = get_current_user()
    if not user:
        return jsonify({"error": "Unauthorized"}), 401
    scans = get_user_scans(user["id"])
    return jsonify({"scans": scans})

@app.route("/api/user/scans/<int:scan_id>", methods=["DELETE"])
def remove_scan(scan_id):
    user = get_current_user()
    if not user:
        return jsonify({"error": "Unauthorized"}), 401
    delete_user_scan(user["id"], scan_id)
    return jsonify({"message": "Scan deleted successfully."})

# --- ATS ENGINE ROUTES ---

@app.route("/analyze", methods=["POST"])
def analyze_resume():
    try:
        if "resume" not in request.files:
            return jsonify({"error": "No resume file provided"}), 400
            
        resume_file = request.files["resume"]
        job_description = request.form.get("job_description", "")
        
        if resume_file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        file_bytes = io.BytesIO(resume_file.read())

        # 1. Parse Resume with pdfplumber
        parsed_data = extract_text_from_pdf(file_bytes)
        resume_text = parsed_data.get("raw_text", "")
        
        if not resume_text.strip():
            return jsonify({"error": "Could not extract text from the provided PDF file."}), 400

        # 2. Extract Keywords from Job Description
        keywords = extract_keywords(job_description)

        # 3. Intelligent Matcher & Weighted Scoring
        result = calculate_ats_score(resume_text, keywords, job_description, layout_data=parsed_data)
        result["raw_extracted_text"] = resume_text

        # If user is logged in, auto-save scan to SQLite database!
        current_user = get_current_user()
        if current_user:
            job_domain = result.get("job_domain", "Technical")
            saved_meta = save_user_scan(
                user_id=current_user["id"],
                score=result.get("overall_score", 0),
                job_domain=job_domain,
                resume_filename=resume_file.filename,
                results=result
            )
            result["saved_scan_id"] = saved_meta["id"]

        return jsonify(result)

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

@app.route("/generate_pdf", methods=["POST"])
def generate_pdf():
    try:
        data = request.json or {}
        resume_text = data.get("resume_text", "")
        missing_keywords = data.get("missing_keywords", [])
        
        if not resume_text.strip():
            return jsonify({"error": "No resume text provided for PDF generation"}), 400

        pdf_buffer = build_single_column_ats_pdf(resume_text, missing_keywords)
        
        return send_file(
            pdf_buffer,
            mimetype="application/pdf",
            as_attachment=True,
            download_name="Optimized_ATS_Resume.pdf"
        )
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)