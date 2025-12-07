import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

from ocr import extract_text
from parser import parse_fields
from verify import verify_data

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)


# ✅ Single home route – serves frontend
@app.route("/")
def index():
    return render_template("index.html")


# ✅ OCR Extraction API
@app.route("/extract", methods=["POST"])
def extract_api():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    raw_text = extract_text(file_path)
    extracted_fields = parse_fields(raw_text)

    return jsonify({
        "raw_text": raw_text,
        "extracted_fields": extracted_fields
    })


# ✅ Verification API
@app.route("/verify", methods=["POST"])
def verify_api():
    data = request.get_json(force=True)

    extracted_fields = data.get("extracted_fields", {})
    user_input = data.get("user_input", {})

    result = verify_data(extracted_fields, user_input)

    return jsonify({
        "verification_results": result
    })


if __name__ == "__main__":
    app.run(debug=True)
