# OCR Identity Extraction & Verification System

This project is an AI-powered OCR-based identity extraction and verification system.
It extracts key personal details from uploaded document images and verifies them
against user-edited values using fuzzy matching.

---

## 🚀 Features
- Upload identity document images
- OCR text extraction using Tesseract
- Intelligent parsing for handwritten & printed formats
- Field-level verification with confidence score
- Supports Name, Age, Gender, Email, Phone, Address
- Web-based UI using HTML/CSS/JS
- REST API using Flask (Python)

---

## 🏗️ Architecture Design

Frontend (HTML + JS)
↓
Flask Backend (REST API)
↓
OCR Engine (Tesseract)
↓
Parser (Regex + Rule-based)
↓
Verification Engine (Fuzzy Matching)
↓
Verification Result (Confidence %)

---

## 🔄 Data Flow

1. User uploads image
2. Image sent to `/extract` API
3. OCR extracts raw text
4. Parser converts text to structured fields
5. Fields displayed in UI (editable)
6. User clicks Verify
7. `/verify` API compares fields
8. Confidence score returned

---

## 🛠️ Installation

### 1. Install Python Dependencies
```bash
pip install -r backend/requirements.txt


2. Install Tesseract OCR

Windows: https://github.com/UB-Mannheim/tesseract/wiki

Add Tesseract to PATH

3. Run the Application
python backend/app.py


Open browser:

http://localhost:5000
