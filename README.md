# FormSathiAI

> **“Make complicated forms easier to understand.”**

FormSathiAI is an AI-powered web application designed to help students, families, and community service centres (CSCs) understand scholarship applications, college admissions paperwork, and public-service forms through simple, grounded explanations in **English** and **Hindi**.

---

## 1. Universal Fictional Warning

> **FICTIONAL DEMO — NOT AN OFFICIAL SCHOLARSHIP — NOT VALID FOR REAL APPLICATIONS.**
> *काल्पनिक डेमो — यह कोई आधिकारिक छात्रवृत्ति नहीं है — वास्तविक आवेदनों के लिए मान्य नहीं है।*

All scholarship details, institutions, applicant records, identity cards, and banking references provided in this demonstration are **entirely fictional samples** created exclusively to test and demonstrate FormSathiAI. The application never submits data to real authorities and never auto-signs declarations.

---

## 2. Key Features

1. **Dual-Language Interface (English & हिन्दी)**: Complete bilingual support across navigation, field explanations, checklists, validation alerts, and Q&A.
2. **Two-Column Application Workspace**:
   - **Left Panel**: Application form data (editable for interactive scenario testing), uploaded document badges, and missing field indicators.
   - **Right Panel**: Plain-language field explanations, grounded Q&A interface with citations, dynamic checklist, and validation findings.
   - **Mobile Friendly**: Automatically stacks vertically on smaller screens.
3. **Four Functional Demo Scenarios**:
   - **Scenario 1 — Eligible Sample**: Standard applicant (Aarav Sharma, 78% marks, ₹1,80,000 income). Criteria are met, but lacks income certificate, passbook, and declaration.
   - **Scenario 2 — Missing Information**: Student name is blank, institution certificate removed, and declaration incomplete.
   - **Scenario 3 — Inconsistent Marks**: Application records 78%, but attached alternate marksheet shows 58%. System flags discrepancy without automatically choosing either value.
   - **Scenario 4 — Income Limit Exceeded**: Declared income ₹2,80,000 exceeds fictional ₹2,50,000 ceiling.
4. **Document Processing & OCR Engine**:
   - Digital PDF parsing via PyMuPDF (`pymupdf`) with page-by-page extraction and heading detection.
   - Scanned image OCR using Tesseract OCR and Pillow, with preprocessing (contrast/grayscale) and confidence scoring.
   - OCR Review & Correction modal allowing applicants to inspect and correct optical recognition text.
   - Graceful fallback if Tesseract is not installed.
5. **Grounded Retrieval-Augmented Q&A (RAG)**:
   - Chunked local document index with page and section metadata.
   - Predefined questions 1–6 with exact bilingual answers and citations.
   - Free-form search grounded strictly in uploaded instructions.
   - **Strict Grounding Rule**: When information is absent from source documents, responds:
     - English: *"This information is not available in the provided instructions."*
     - Hindi: *"यह जानकारी दिए गए निर्देशों में उपलब्ध नहीं है।"*
6. **Dynamic Required-Document Checklist**:
   - Tracks 6 required items (Marksheet, Identity Proof, Income Cert, Bank Passbook, Institution Cert, Declaration).
   - Real-time progress bar (X of Y completed).
   - Clear distinction for unverified placeholders vs official documents.
7. **Cross-Validation & Inconsistency Detection**:
   - Categorizes alerts into: **Confirmed Requirement**, **Missing Information**, **Potential Inconsistency**, **Unverified Document**, and **Information Unavailable**.
   - Non-alarming warnings for ordinary incomplete fields.
8. **Privacy & Security Safeguards**:
   - Explicit user consent modal before processing sensitive personal information.
   - Explains what will be extracted and why.
   - Session-isolated temporary storage with instant reset and file deletion.
   - Zero sensitive document logging.
   - 100% offline deterministic execution without requiring external LLM API keys.

---

## 3. Technology Stack

- **Frontend**:
  - React 19 with TypeScript and Vite
  - Tailwind CSS for modern responsive styling
  - Lucide React for accessible icons
- **Backend**:
  - Python 3.12 with FastAPI and Uvicorn
  - PyMuPDF (`pymupdf`) for digital PDF parsing
  - Pillow (`PIL`) and `pytesseract` for image OCR
  - ReportLab for generating valid sample PDF assets
  - Pytest with TestClient for automated testing

---

## 4. Exact Demo Data & Assets

### Scholarship Rules:
- **Scholarship Name**: Udaan Student Support Scholarship 2026–27
- **Issuing Organization**: Udaan Education Foundation (fictional)
- **Reference ID**: DEMO-USS-RULES-2026
- **Academic Session**: 2026–27
- **Eligible Study Level**: First-year undergraduate (B.Tech, B.Sc., B.A., B.Com.)
- **Minimum Qualifying Marks**: 60%
- **Annual Family Income Limit**: ₹2,50,000
- **Application Deadline**: 30 November 2026

### Default Applicant Record:
- **Application ID**: DEMO-USS-2026-001
- **Student Name**: Aarav Sharma
- **Date of Birth**: 15/08/2007
- **Course**: B.Tech Computer Science (First year)
- **Institution**: Sunrise Institute of Technology (fictional)
- **Qualifying Marks**: 78%
- **Annual Family Income**: ₹1,80,000
- **Bank Account Reference**: DEMO-ACCOUNT-0001 (Placeholder)

### Generated Demo Documents (`demo_data/`):
| File | Format | Description |
|---|---|---|
| `Udaan_Scholarship_Instructions_Demo.pdf` | PDF (4 Pages) | Complete official instructions with 10 sections |
| `Udaan_Scholarship_Instructions_Demo.txt` | TXT | Exact plain-text equivalent |
| `Udaan_Application_Form_Demo.pdf` | PDF | Sample application form with Sections A–E |
| `Udaan_Application_Form_Demo.txt` | TXT | Exact plain-text equivalent |
| `Academic_Marksheet_Demo.pdf` | PDF | Marksheet showing 78% obtained |
| `Academic_Marksheet_Inconsistent_Demo.pdf` | PDF | Marksheet altered to 58% for discrepancy testing |
| `Identity_Proof_Placeholder_Demo.pdf` | PDF | Sample identity placeholder (DEMO-ID-0001) |
| `Income_Certificate_Placeholder_Demo.pdf` | PDF | Sample income certificate (₹1,80,000) |
| `Bank_Passbook_Placeholder_Demo.pdf` | PDF | Sample bank passbook placeholder |
| `Institution_Certificate_Demo.pdf` | PDF | Student enrollment certificate |
| `Applicant_Declaration_Demo.pdf` | PDF | Unsigned declaration document |
| `Udaan_Application_Form_Scanned_Demo.png` | PNG | Scanned-style image for OCR testing |
| `Udaan_Scholarship_Instructions_Scanned_Demo.png` | PNG | Scanned-style image for OCR testing |
| `demo_documents_manifest.json` | JSON | Complete metadata manifest of all demo assets |

---

## 5. Quick Start & Execution

### Prerequisites:
- Python 3.11+ (or `uv` package manager)
- Node.js 18+ and npm
- (Optional) Tesseract OCR installed at `C:\Program Files\Tesseract-OCR\tesseract.exe`

### One-Click Launch (Windows):
Double-click:
```bat
run_app.bat
```
This launches the FastAPI server and opens `http://127.0.0.1:8000` in your default browser.

### Manual Startup:

#### 1. Backend Setup:
```powershell
cd backend
# Create virtual environment with uv or python
uv venv .venv --python 3.12
# Activate virtual environment
.\.venv\Scripts\activate
# Install requirements
uv pip install -r requirements.txt
# (Optional) Regenerate demo assets if needed
python generate_demo_assets.py
# Start backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

#### 2. Frontend Setup:
```powershell
cd frontend
# Install dependencies
npm install
# Build production bundle
npm run build
# Or run Vite dev server
npm run dev
```

---

## 6. Running Automated Tests

A comprehensive automated test suite (`backend/tests/test_formsathiai.py`) tests all 17 requirements:
- Launches without API key in offline demo mode
- Validates all 8 fictional document types and manifest
- Verifies PDF text and 4-page structure
- Validates OCR extraction on scanned test assets
- Confirms source retrieval and section citations
- Validates default checklist missing items
- Verifies inconsistent marks detection (78% vs 58%)
- Verifies family income limit checking (₹2,80,000 vs ₹2,50,000)
- Confirms Hindi and English bilingual consistency
- Verifies placeholders are marked unverified
- Verifies declaration requires explicit user confirmation
- Verifies session reset and session isolation
- Verifies unknown queries return strict absence statement without hallucination
- Confirms unsupported file rejection and local offline execution

To run the tests:
```powershell
cd backend
.\.venv\Scripts\python.exe -m pytest tests -v
```

## 7. GitHub Actions and Render Deployment

The `CI` workflow runs the backend tests and builds the frontend on pushes and pull requests targeting `main`. A successful push to `main` triggers a Render deploy when the `RENDER_DEPLOY_HOOK_URL` GitHub Actions repository secret is configured. Pull requests never deploy.

To connect Render:

1. In Render, create a Blueprint and connect `IRNCyber/FormSathiAI` on the `main` branch. Render reads the root `render.yaml` and builds the Docker service.
2. After the service is created, open its Settings page and create a Deploy Hook.
3. In GitHub, open **Settings → Secrets and variables → Actions**, create a repository secret named `RENDER_DEPLOY_HOOK_URL`, and paste the Render hook URL as its value.

Render auto-deploys are disabled in the Blueprint so production deploys start only after both CI jobs pass. The GitHub workflow skips the deploy step until the secret is set.

---

## 8. Project Directory Structure

```
formsathiai/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI app & static file server
│   │   ├── config.py                  # Environment & storage settings
│   │   ├── models.py                  # Pydantic data schemas
│   │   ├── demo_data.py               # Fictional rules, explanations & Q&A
│   │   ├── document_parser.py         # PyMuPDF & OCR extraction
│   │   ├── ocr_engine.py              # Tesseract engine & preprocessing
│   │   ├── retrieval.py               # Grounded RAG & local chunk search
│   │   ├── validator.py               # Rule checks & discrepancy detector
│   │   ├── checklist.py               # Dynamic checklist calculator
│   │   ├── session_manager.py         # Isolated session management
│   │   └── api/
│   │       ├── __init__.py
│   │       ├── demo.py                # Scenarios & demo asset serving
│   │       ├── documents.py           # Upload, delete, OCR review
│   │       ├── qa.py                  # Grounded Q&A endpoint
│   │       ├── validation.py          # Checklist & validation endpoints
│   │       └── session.py             # Consent & session reset endpoints
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_formsathiai.py        # 17 automated tests
│   ├── generate_demo_assets.py        # ReportLab asset generator
│   ├── requirements.txt               # Backend dependencies
│   └── .env.example                   # Environment configuration template
├── demo_data/                         # Generated PDFs, TXT, PNG & JSON manifest
│   ├── Udaan_Scholarship_Instructions_Demo.pdf
│   ├── Udaan_Scholarship_Instructions_Demo.txt
│   ├── Udaan_Application_Form_Demo.pdf
│   ├── Udaan_Application_Form_Demo.txt
│   ├── Academic_Marksheet_Demo.pdf
│   ├── Academic_Marksheet_Inconsistent_Demo.pdf
│   ├── Identity_Proof_Placeholder_Demo.pdf
│   ├── Income_Certificate_Placeholder_Demo.pdf
│   ├── Bank_Passbook_Placeholder_Demo.pdf
│   ├── Institution_Certificate_Demo.pdf
│   ├── Applicant_Declaration_Demo.pdf
│   ├── Udaan_Application_Form_Scanned_Demo.png
│   ├── Udaan_Scholarship_Instructions_Scanned_Demo.png
│   └── demo_documents_manifest.json
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.tsx
│   │   │   ├── FictionalBanner.tsx
│   │   │   ├── Dashboard.tsx
│   │   │   ├── ApplicationWorkspace.tsx
│   │   │   ├── ScenarioSelector.tsx
│   │   │   ├── FieldExplainer.tsx
│   │   │   ├── DocumentManager.tsx
│   │   │   ├── AskFormSathi.tsx
│   │   │   ├── ChecklistView.tsx
│   │   │   ├── ValidationAlerts.tsx
│   │   │   ├── ConsentModal.tsx
│   │   │   ├── OcrReviewModal.tsx
│   │   │   └── PrivacyHelp.tsx
│   │   ├── context/
│   │   │   ├── LanguageContext.tsx    # English & Hindi toggle
│   │   │   └── AppContext.tsx         # Central application state
│   │   ├── types.ts                   # TypeScript interfaces
│   │   ├── App.tsx                    # Primary layout & routing
│   │   ├── main.tsx
│   │   └── index.css                  # Tailwind styles
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   └── tsconfig.app.json
├── run_app.bat                        # Integrated launcher
├── run_backend.bat                    # Backend-only launcher
├── run_frontend.bat                   # Frontend-only launcher
└── README.md
```
