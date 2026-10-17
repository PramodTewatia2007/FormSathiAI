"""
Generate all fictional demo PDF, TXT, PNG, and JSON manifest files for FormSathiAI.
All data is fictional and explicitly marked as such.
"""

import json
import math
import os
import random
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.pdfgen import canvas
from PIL import Image, ImageDraw, ImageFilter
import fitz  # PyMuPDF

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEMO_DATA_DIR = os.path.join(BASE_DIR, "demo_data")
os.makedirs(DEMO_DATA_DIR, exist_ok=True)

DISCLAIMER_TEXT = "FICTIONAL DEMO — NOT AN OFFICIAL SCHOLARSHIP — NOT VALID FOR REAL APPLICATIONS."


class NumberedCanvas(canvas.Canvas):
    """Adds a disclaimer header and page footer with watermark on every page."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        
        # Diagonal watermark
        self.setFont("Helvetica-Bold", 40)
        self.setFillColor(colors.Color(0.85, 0.85, 0.85, alpha=0.35))
        self.rotate(35)
        self.drawString(180, 50, "FICTIONAL DEMO ONLY")
        self.drawString(140, 10, "NOT VALID FOR REAL APPLICATIONS")
        self.restoreState()

        self.saveState()
        # Top banner
        self.setFillColor(colors.HexColor("#FEF2F2"))
        self.rect(0, 762, 612, 30, fill=1, stroke=0)
        self.setFillColor(colors.HexColor("#DC2626"))
        self.setFont("Helvetica-Bold", 8)
        self.drawCentredString(306, 773, DISCLAIMER_TEXT)

        # Bottom footer
        self.setStrokeColor(colors.HexColor("#E5E7EB"))
        self.setLineWidth(0.5)
        self.line(36, 45, 576, 45)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#6B7280"))
        self.drawString(36, 32, "FormSathiAI Demonstration System — Fictional Sample Data")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(576, 32, page_str)
        self.restoreState()


def get_styles():
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#1E3A8A"),
        spaceAfter=6
    )
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#2563EB"),
        spaceAfter=12
    )
    h2_style = ParagraphStyle(
        'DocH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#1F2937"),
        spaceBefore=10,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#374151"),
        spaceAfter=6
    )
    body_bold = ParagraphStyle(
        'DocBodyBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )
    box_style = ParagraphStyle(
        'DocBox',
        parent=body_style,
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#4B5563")
    )
    return {
        "title": title_style,
        "subtitle": subtitle_style,
        "h2": h2_style,
        "body": body_style,
        "bold": body_bold,
        "box": box_style
    }


def generate_instructions_pdf():
    pdf_path = os.path.join(DEMO_DATA_DIR, "Udaan_Scholarship_Instructions_Demo.pdf")
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=55,
        bottomMargin=55
    )
    s = get_styles()
    story = []

    # PAGE 1
    story.append(Paragraph("Udaan Education Foundation", s["title"]))
    story.append(Paragraph("Udaan Student Support Scholarship 2026–27", s["subtitle"]))
    story.append(Paragraph("<b>Document type:</b> Fictional scholarship instructions.", s["body"]))
    story.append(Paragraph("<b>Reference ID:</b> DEMO-USS-RULES-2026", s["body"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>Purpose:</b>", s["bold"]))
    story.append(Paragraph(
        "This fictional scholarship program demonstrates how FormSathiAI explains "
        "application requirements to students and families.", s["body"]
    ))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Section 1: Academic Eligibility", s["h2"]))
    story.append(Paragraph("1. Applicants must be enrolled in the first year of an undergraduate course.", s["body"]))
    story.append(Paragraph("2. Applicants must have obtained at least 60% marks in their qualifying examination.", s["body"]))
    story.append(Paragraph("3. Applicants must provide an academic marksheet as supporting evidence.", s["body"]))
    story.append(Paragraph("4. Meeting these criteria does not guarantee selection or a scholarship award.", s["body"]))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Section 2: Eligible Courses", s["h2"]))
    story.append(Paragraph("For this demonstration, the following courses are accepted:", s["body"]))
    story.append(Paragraph("• Bachelor of Technology (B.Tech)", s["body"]))
    story.append(Paragraph("• Bachelor of Science (B.Sc.)", s["body"]))
    story.append(Paragraph("• Bachelor of Arts (B.A.)", s["body"]))
    story.append(Paragraph("• Bachelor of Commerce (B.Com.)", s["body"]))
    story.append(Paragraph("All eligibility rules in this document are fictional.", s["body"]))

    # PAGE 2
    story.append(PageBreak())
    story.append(Paragraph("Udaan Education Foundation — Scholarship Instructions (Contd.)", s["subtitle"]))
    story.append(Paragraph("Section 3: Family Income Criteria", s["h2"]))
    story.append(Paragraph("1. The fictional annual family income limit is ₹2,50,000.", s["body"]))
    story.append(Paragraph("2. Applicants must provide an income certificate as evidence.", s["body"]))
    story.append(Paragraph("3. If declared income exceeds ₹2,50,000, the application does not meet this sample income criterion.", s["body"]))
    story.append(Paragraph("4. FormSathiAI must flag missing or inconsistent income information for review.", s["body"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Section 4: Required Documents", s["h2"]))
    story.append(Paragraph("The fictional instructions list:", s["body"]))
    story.append(Paragraph("1. Academic marksheet.", s["body"]))
    story.append(Paragraph("2. Identity proof.", s["body"]))
    story.append(Paragraph("3. Income certificate.", s["body"]))
    story.append(Paragraph("4. Bank passbook copy.", s["body"]))
    story.append(Paragraph("5. Institution certificate.", s["body"]))
    story.append(Paragraph("6. Completed applicant declaration.", s["body"]))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Document verification:</b>", s["bold"]))
    story.append(Paragraph(
        "Uploaded files must be checked for presence and readability. "
        "The prototype may flag missing documents but must not claim that an official authority has verified them.",
        s["body"]
    ))

    # PAGE 3
    story.append(PageBreak())
    story.append(Paragraph("Udaan Education Foundation — Application Instructions", s["subtitle"]))
    story.append(Paragraph("Section 5: Completing the Form", s["h2"]))
    story.append(Paragraph("1. Enter the applicant's name as shown on supporting documents.", s["body"]))
    story.append(Paragraph("2. Enter the date of birth in DD/MM/YYYY format.", s["body"]))
    story.append(Paragraph("3. Provide the course and current year of study.", s["body"]))
    story.append(Paragraph("4. Enter the qualifying examination percentage.", s["body"]))
    story.append(Paragraph("5. Enter annual family income in Indian rupees.", s["body"]))
    story.append(Paragraph("6. Confirm which supporting documents are available.", s["body"]))
    story.append(Paragraph("7. Review all warnings before marking the declaration complete.", s["body"]))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Section 6: Inconsistent Information", s["h2"]))
    story.append(Paragraph(
        "If marks entered in the application differ from marks on the marksheet, the applicant must review "
        "both values and correct the application only after checking the original document.", s["body"]
    ))
    story.append(Paragraph("The system must not automatically choose one value as correct.", s["body"]))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Section 7: Privacy", s["h2"]))
    story.append(Paragraph(
        "Applicants should upload only documents necessary for the demonstration. Sensitive values must be minimized, "
        "protected, and not retained unnecessarily.", s["body"]
    ))
    story.append(Paragraph(
        "The demo must use placeholder identity and banking information rather than real personal records.", s["body"]
    ))

    # PAGE 4
    story.append(PageBreak())
    story.append(Paragraph("Udaan Education Foundation — Deadline & Submission", s["subtitle"]))
    story.append(Paragraph("Section 8: Application Deadline", s["h2"]))
    story.append(Paragraph("Fictional deadline: <b>30 November 2026</b>.", s["body"]))
    story.append(Paragraph("Date format: DD/MM/YYYY.", s["body"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Section 9: Submission Instructions", s["h2"]))
    story.append(Paragraph("1. Complete the application fields.", s["body"]))
    story.append(Paragraph("2. Review the required-document checklist.", s["body"]))
    story.append(Paragraph("3. Resolve missing-field warnings.", s["body"]))
    story.append(Paragraph("4. Review inconsistencies.", s["body"]))
    story.append(Paragraph("5. Confirm the declaration only after checking the supplied information.", s["body"]))
    story.append(Paragraph("The demonstration application must not submit anything to an external website.", s["body"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Section 10: Limits of This Document", s["h2"]))
    story.append(Paragraph(
        "This document is fictional and is not an official scholarship notification. It must not be used to make "
        "decisions about a real scholarship. For real applications, consult the relevant official authority and "
        "its current instructions.", s["body"]
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated: {pdf_path}")


def generate_instructions_txt():
    txt_path = os.path.join(DEMO_DATA_DIR, "Udaan_Scholarship_Instructions_Demo.txt")
    content = """Udaan Education Foundation
Udaan Student Support Scholarship 2026–27
Document type: Fictional scholarship instructions.
Reference ID: DEMO-USS-RULES-2026

Purpose:
This fictional scholarship program demonstrates how FormSathiAI explains application requirements to students and families.

Section 1: Academic Eligibility
1. Applicants must be enrolled in the first year of an undergraduate course.
2. Applicants must have obtained at least 60% marks in their qualifying examination.
3. Applicants must provide an academic marksheet as supporting evidence.
4. Meeting these criteria does not guarantee selection or a scholarship award.

Section 2: Eligible Courses
For this demonstration, the following courses are accepted:
- Bachelor of Technology (B.Tech)
- Bachelor of Science (B.Sc.)
- Bachelor of Arts (B.A.)
- Bachelor of Commerce (B.Com.)
All eligibility rules in this document are fictional.

Section 3: Family Income Criteria
1. The fictional annual family income limit is ₹2,50,000.
2. Applicants must provide an income certificate as evidence.
3. If declared income exceeds ₹2,50,000, the application does not meet this sample income criterion.
4. FormSathiAI must flag missing or inconsistent income information for review.

Section 4: Required Documents
The fictional instructions list:
1. Academic marksheet.
2. Identity proof.
3. Income certificate.
4. Bank passbook copy.
5. Institution certificate.
6. Completed applicant declaration.

Document verification:
Uploaded files must be checked for presence and readability. The prototype may flag missing documents but must not claim that an official authority has verified them.

Section 5: Completing the Form
1. Enter the applicant's name as shown on supporting documents.
2. Enter the date of birth in DD/MM/YYYY format.
3. Provide the course and current year of study.
4. Enter the qualifying examination percentage.
5. Enter annual family income in Indian rupees.
6. Confirm which supporting documents are available.
7. Review all warnings before marking the declaration complete.

Section 6: Inconsistent Information
If marks entered in the application differ from marks on the marksheet, the applicant must review both values and correct the application only after checking the original document.
The system must not automatically choose one value as correct.

Section 7: Privacy
Applicants should upload only documents necessary for the demonstration. Sensitive values must be minimized, protected, and not retained unnecessarily.
The demo must use placeholder identity and banking information rather than real personal records.

Section 8: Application Deadline
Fictional deadline: 30 November 2026.
Date format: DD/MM/YYYY.

Section 9: Submission Instructions
1. Complete the application fields.
2. Review the required-document checklist.
3. Resolve missing-field warnings.
4. Review inconsistencies.
5. Confirm the declaration only after checking the supplied information.
The demonstration application must not submit anything to an external website.

Section 10: Limits of This Document
This document is fictional and is not an official scholarship notification. It must not be used to make decisions about a real scholarship. For real applications, consult the relevant official authority and its current instructions.
"""
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated: {txt_path}")


def generate_application_form_pdf():
    pdf_path = os.path.join(DEMO_DATA_DIR, "Udaan_Application_Form_Demo.pdf")
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=55,
        bottomMargin=55
    )
    s = get_styles()
    story = []

    story.append(Paragraph("Udaan Student Support Scholarship Application", s["title"]))
    story.append(Paragraph("Academic Session: 2026–27 | Application ID: DEMO-USS-2026-001", s["subtitle"]))
    story.append(Spacer(1, 6))

    # Section A
    story.append(Paragraph("Section A — Applicant Information", s["h2"]))
    table_a_data = [
        ["Full name:", "Aarav Sharma", "Date of birth:", "15/08/2007"],
        ["Course:", "B.Tech Computer Science", "Current study year:", "First year"],
        ["Institution:", "Sunrise Institute of Technology (fictional)", "", ""]
    ]
    t_a = Table(table_a_data, colWidths=[120, 150, 110, 140])
    t_a.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F9FAFB")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_a)
    story.append(Spacer(1, 10))

    # Section B
    story.append(Paragraph("Section B — Academic Information", s["h2"]))
    table_b_data = [
        ["Qualifying examination percentage:", "78%"],
        ["Marksheet attached:", "Yes"],
        ["Institution certificate attached:", "Yes"]
    ]
    t_b = Table(table_b_data, colWidths=[230, 290])
    t_b.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F9FAFB")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_b)
    story.append(Spacer(1, 10))

    # Section C
    story.append(Paragraph("Section C — Family Income", s["h2"]))
    table_c_data = [
        ["Annual family income:", "₹1,80,000"],
        ["Income certificate attached:", "No"]
    ]
    t_c = Table(table_c_data, colWidths=[230, 290])
    t_c.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F9FAFB")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_c)
    story.append(Spacer(1, 10))

    # Section D
    story.append(Paragraph("Section D — Identity and Bank Documents", s["h2"]))
    table_d_data = [
        ["Identity proof attached:", "Yes, fictional placeholder"],
        ["Bank passbook copy attached:", "No"],
        ["Bank account holder:", "Aarav Sharma"],
        ["Bank account reference:", "DEMO-ACCOUNT-0001"]
    ]
    t_d = Table(table_d_data, colWidths=[230, 290])
    t_d.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F9FAFB")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_d)
    story.append(Spacer(1, 10))

    # Section E
    story.append(Paragraph("Section E — Applicant Declaration", s["h2"]))
    story.append(Paragraph(
        "“I confirm that I have reviewed the information in this fictional demonstration form. "
        "I understand that any discrepancies must be checked against the original documents.”",
        s["body"]
    ))
    table_e_data = [
        ["Declaration accepted:", "No"],
        ["Applicant signature:", "Not provided"],
        ["Date:", "Not provided"]
    ]
    t_e = Table(table_e_data, colWidths=[230, 290])
    t_e.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#FEE2E2")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#FCA5A5")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_e)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated: {pdf_path}")


def generate_application_form_txt():
    txt_path = os.path.join(DEMO_DATA_DIR, "Udaan_Application_Form_Demo.txt")
    content = """Udaan Student Support Scholarship Application
Academic session: 2026–27
Application ID: DEMO-USS-2026-001

Section A — Applicant Information
- Full name: Aarav Sharma
- Date of birth: 15/08/2007
- Course: B.Tech Computer Science
- Current study year: First year
- Institution: Sunrise Institute of Technology (fictional)

Section B — Academic Information
- Qualifying examination percentage: 78%
- Marksheet attached: Yes
- Institution certificate attached: Yes

Section C — Family Income
- Annual family income: ₹1,80,000
- Income certificate attached: No

Section D — Identity and Bank Documents
- Identity proof attached: Yes, fictional placeholder
- Bank passbook copy attached: No
- Bank account holder: Aarav Sharma
- Bank account reference: DEMO-ACCOUNT-0001

Section E — Applicant Declaration
“I confirm that I have reviewed the information in this fictional demonstration form. I understand that any discrepancies must be checked against the original documents.”
- Declaration accepted: No
- Applicant signature: Not provided
- Date: Not provided
"""
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated: {txt_path}")


def generate_marksheet_pdf(filename, recorded_pct, is_inconsistent=False):
    pdf_path = os.path.join(DEMO_DATA_DIR, filename)
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=55,
        bottomMargin=55
    )
    s = get_styles()
    story = []

    story.append(Paragraph("Sunrise Institute of Technology (fictional)", s["title"]))
    story.append(Paragraph("Qualifying Examination — Demo Record", s["subtitle"]))
    story.append(Spacer(1, 4))

    meta_data = [
        ["Student Name:", "Aarav Sharma", "Record ID:", "DEMO-MARK-001"],
        ["Academic Year:", "2025–26", "Status:", "Invited Record (Demo)"]
    ]
    t_m = Table(meta_data, colWidths=[110, 160, 100, 150])
    t_m.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F3F4F6")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_m)
    story.append(Spacer(1, 14))

    marks_data = [
        ["Subject", "Maximum marks", "Marks obtained"],
        ["Mathematics", "100", "82"],
        ["Physics", "100", "76"],
        ["Chemistry", "100", "75"],
        ["English", "100", "80"],
        ["Computer Science", "100", "77"],
        ["Total", "500", "390"]
    ]
    t_marks = Table(marks_data, colWidths=[220, 150, 150])
    t_marks.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor("#E5E7EB")),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_marks)
    story.append(Spacer(1, 12))

    story.append(Paragraph(f"<b>Recorded Percentage:</b> {recorded_pct}", s["h2"]))
    story.append(Paragraph("Calculation: 390 ÷ 500 × 100 = 78%", s["body"]))
    story.append(Spacer(1, 10))

    if is_inconsistent:
        story.append(Paragraph(
            "<b>Altered test value for inconsistency detection. This is a fictional test asset.</b>",
            s["bold"]
        ))
    else:
        story.append(Paragraph(
            "This is an invented academic record for software testing. It is not an official marksheet.",
            s["body"]
        ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated: {pdf_path}")


def generate_identity_pdf():
    pdf_path = os.path.join(DEMO_DATA_DIR, "Identity_Proof_Placeholder_Demo.pdf")
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=55,
        bottomMargin=55
    )
    s = get_styles()
    story = []

    story.append(Paragraph("Fictional Identity Proof Placeholder", s["title"]))
    story.append(Paragraph("Reference: DEMO-ID-0001", s["subtitle"]))
    story.append(Spacer(1, 8))

    data = [
        ["Holder name:", "Aarav Sharma"],
        ["Date of birth:", "15/08/2007"],
        ["Address:", "Fictional Demo Address, Demo City"],
        ["Issuing authority:", "None — fictional sample only"],
        ["Verification status:", "Not verified"]
    ]
    t = Table(data, colWidths=[160, 360])
    t.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9.5),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F9FAFB")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 14))
    story.append(Paragraph(
        "<b>Notice:</b> This document is not government-issued identification and cannot be used as proof of identity.",
        s["bold"]
    ))
    story.append(Paragraph(
        "Classification: Sample placeholder, not verified identity evidence.",
        s["body"]
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated: {pdf_path}")


def generate_income_certificate_pdf():
    pdf_path = os.path.join(DEMO_DATA_DIR, "Income_Certificate_Placeholder_Demo.pdf")
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=55,
        bottomMargin=55
    )
    s = get_styles()
    story = []

    story.append(Paragraph("Fictional Income Certificate Placeholder", s["title"]))
    story.append(Paragraph("Reference ID: DEMO-INCOME-0001", s["subtitle"]))
    story.append(Spacer(1, 8))

    data = [
        ["Applicant:", "Aarav Sharma"],
        ["Annual family income:", "₹1,80,000"],
        ["Issue date:", "01/10/2026"],
        ["Issuing authority:", "None — fictional sample only"],
        ["Verification status:", "Not verified"]
    ]
    t = Table(data, colWidths=[160, 360])
    t.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9.5),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F9FAFB")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 14))
    story.append(Paragraph(
        "<b>Important Notice:</b> This is not an official income certificate.",
        s["bold"]
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated: {pdf_path}")


def generate_bank_passbook_pdf():
    pdf_path = os.path.join(DEMO_DATA_DIR, "Bank_Passbook_Placeholder_Demo.pdf")
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=55,
        bottomMargin=55
    )
    s = get_styles()
    story = []

    story.append(Paragraph("Fictional Bank Passbook Placeholder", s["title"]))
    story.append(Paragraph("Account Reference: DEMO-ACCOUNT-0001", s["subtitle"]))
    story.append(Spacer(1, 8))

    data = [
        ["Account holder:", "Aarav Sharma"],
        ["Bank name:", "Fictional Demo Bank"],
        ["Branch:", "Demo Branch"],
        ["IFSC:", "NOT-A-REAL-IFSC"],
        ["Account verification:", "Not verified"]
    ]
    t = Table(data, colWidths=[160, 360])
    t.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9.5),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F9FAFB")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 14))
    story.append(Paragraph(
        "<b>Notice:</b> This is not a bank-issued document. All banking fields are placeholders.",
        s["bold"]
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated: {pdf_path}")


def generate_institution_certificate_pdf():
    pdf_path = os.path.join(DEMO_DATA_DIR, "Institution_Certificate_Demo.pdf")
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=55,
        bottomMargin=55
    )
    s = get_styles()
    story = []

    story.append(Paragraph("Student Enrollment Certificate — Fictional Demo", s["title"]))
    story.append(Paragraph("Enrollment Reference: DEMO-ENROLL-001", s["subtitle"]))
    story.append(Spacer(1, 8))

    data = [
        ["Institution:", "Sunrise Institute of Technology"],
        ["Student:", "Aarav Sharma"],
        ["Course:", "B.Tech Computer Science"],
        ["Study year:", "First year"],
        ["Academic session:", "2026–27"],
        ["Certificate status:", "Fictional sample; not officially verified"]
    ]
    t = Table(data, colWidths=[160, 360])
    t.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9.5),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F9FAFB")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t)
    story.append(Spacer(1, 14))
    story.append(Paragraph(
        "Statement: This sample record is provided solely to demonstrate document extraction, "
        "field explanation, and checklist generation in FormSathiAI.",
        s["body"]
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated: {pdf_path}")


def generate_declaration_pdf():
    pdf_path = os.path.join(DEMO_DATA_DIR, "Applicant_Declaration_Demo.pdf")
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=55,
        bottomMargin=55
    )
    s = get_styles()
    story = []

    story.append(Paragraph("Applicant Declaration — Fictional Demo", s["title"]))
    story.append(Paragraph("Application ID: DEMO-USS-2026-001", s["subtitle"]))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>I understand that:</b>", s["bold"]))
    story.append(Paragraph("1. All scholarship rules in this demonstration are fictional.", s["body"]))
    story.append(Paragraph("2. I must review the information entered into the sample application.", s["body"]))
    story.append(Paragraph("3. Missing documents and inconsistencies must be resolved before completing the demonstration workflow.", s["body"]))
    story.append(Paragraph("4. FormSathiAI provides explanations and checks but does not certify eligibility or guarantee an award.", s["body"]))
    story.append(Paragraph("5. This demo does not submit an application to any real institution.", s["body"]))
    story.append(Spacer(1, 10))

    data = [
        ["Applicant name:", "Aarav Sharma"],
        ["Declaration status:", "NOT ACCEPTED"],
        ["Signature:", "Not provided"],
        ["Date:", "Not provided"]
    ]
    t = Table(data, colWidths=[160, 360])
    t.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9.5),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#FEF2F2")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#FCA5A5")),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated: {pdf_path}")


def generate_scanned_pngs():
    """Render page 1 of PDFs and apply realistic scan effects."""
    pairs = [
        ("Udaan_Application_Form_Demo.pdf", "Udaan_Application_Form_Scanned_Demo.png"),
        ("Udaan_Scholarship_Instructions_Demo.pdf", "Udaan_Scholarship_Instructions_Scanned_Demo.png")
    ]
    for pdf_name, png_name in pairs:
        pdf_path = os.path.join(DEMO_DATA_DIR, pdf_name)
        png_path = os.path.join(DEMO_DATA_DIR, png_name)
        
        doc = fitz.open(pdf_path)
        page = doc.load_page(0)
        pix = page.get_pixmap(dpi=200)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        # Subtle scan effect: slight warm tint, slight rotation (0.4 deg)
        # Background paper tint
        tint = Image.new("RGB", img.size, (253, 252, 250))
        img = Image.blend(img, tint, 0.04)

        # Rotate by 0.35 degrees with white background to simulate slight physical scanner skew
        img = img.rotate(0.35, resample=Image.Resampling.BICUBIC, expand=False, fillcolor=(255, 255, 255))
        
        # Add faint scanner line or slight edge border
        draw = ImageDraw.Draw(img)
        draw.rectangle([(2, 2), (img.width - 3, img.height - 3)], outline=(220, 220, 220), width=1)
        
        img.save(png_path, "PNG", quality=95)
        print(f"Generated scanned image: {png_path}")


def generate_manifest():
    manifest_path = os.path.join(DEMO_DATA_DIR, "demo_documents_manifest.json")
    manifest = {
        "scholarship_name": "Udaan Student Support Scholarship 2026–27",
        "reference_id": "DEMO-USS-RULES-2026",
        "academic_session": "2026–27",
        "application_id": "DEMO-USS-2026-001",
        "fictional_warning": DISCLAIMER_TEXT,
        "documents": [
            {
                "filename": "Udaan_Scholarship_Instructions_Demo.pdf",
                "document_type": "official_instructions",
                "reference_id": "DEMO-USS-RULES-2026",
                "expected_attachment_status": "official_guideline",
                "description": "Four-page complete official scholarship instructions with 10 sections.",
                "relevant_scenarios": ["Scenario 1", "Scenario 2", "Scenario 3", "Scenario 4"]
            },
            {
                "filename": "Udaan_Application_Form_Demo.pdf",
                "document_type": "application_form",
                "reference_id": "DEMO-USS-2026-001",
                "expected_attachment_status": "core_application",
                "description": "Completed sample application form with Sections A to E.",
                "relevant_scenarios": ["Scenario 1", "Scenario 2", "Scenario 3", "Scenario 4"]
            },
            {
                "filename": "Academic_Marksheet_Demo.pdf",
                "document_type": "academic_marksheet",
                "reference_id": "DEMO-MARK-001",
                "expected_attachment_status": "attached",
                "description": "Standard marksheet showing 78% percentage obtained.",
                "relevant_scenarios": ["Scenario 1", "Scenario 4"]
            },
            {
                "filename": "Academic_Marksheet_Inconsistent_Demo.pdf",
                "document_type": "academic_marksheet_inconsistent",
                "reference_id": "DEMO-MARK-001",
                "expected_attachment_status": "available_in_library",
                "description": "Altered marksheet showing 58% percentage for discrepancy testing.",
                "relevant_scenarios": ["Scenario 3"]
            },
            {
                "filename": "Identity_Proof_Placeholder_Demo.pdf",
                "document_type": "identity_proof",
                "reference_id": "DEMO-ID-0001",
                "expected_attachment_status": "attached_unverified",
                "description": "Fictional identity placeholder, non-official.",
                "relevant_scenarios": ["Scenario 1", "Scenario 3", "Scenario 4"]
            },
            {
                "filename": "Income_Certificate_Placeholder_Demo.pdf",
                "document_type": "income_certificate",
                "reference_id": "DEMO-INCOME-0001",
                "expected_attachment_status": "missing_by_default",
                "description": "Fictional income certificate for Aarav Sharma showing ₹1,80,000.",
                "relevant_scenarios": ["Scenario 1", "Scenario 2", "Scenario 3", "Scenario 4"]
            },
            {
                "filename": "Bank_Passbook_Placeholder_Demo.pdf",
                "document_type": "bank_passbook",
                "reference_id": "DEMO-ACCOUNT-0001",
                "expected_attachment_status": "missing_by_default",
                "description": "Fictional bank passbook placeholder, non-official.",
                "relevant_scenarios": ["Scenario 1", "Scenario 2", "Scenario 3", "Scenario 4"]
            },
            {
                "filename": "Institution_Certificate_Demo.pdf",
                "document_type": "institution_certificate",
                "reference_id": "DEMO-ENROLL-001",
                "expected_attachment_status": "attached_unverified",
                "description": "Enrollment certificate from Sunrise Institute of Technology.",
                "relevant_scenarios": ["Scenario 1", "Scenario 3", "Scenario 4"]
            },
            {
                "filename": "Applicant_Declaration_Demo.pdf",
                "document_type": "applicant_declaration",
                "reference_id": "DEMO-USS-2026-001",
                "expected_attachment_status": "incomplete_by_default",
                "description": "Applicant declaration requiring explicit confirmation.",
                "relevant_scenarios": ["Scenario 1", "Scenario 2", "Scenario 3", "Scenario 4"]
            },
            {
                "filename": "Udaan_Application_Form_Scanned_Demo.png",
                "document_type": "scanned_image",
                "reference_id": "DEMO-USS-2026-001-SCAN",
                "expected_attachment_status": "ocr_test_asset",
                "description": "Scanned image representation of application form for OCR testing.",
                "relevant_scenarios": ["OCR Testing"]
            },
            {
                "filename": "Udaan_Scholarship_Instructions_Scanned_Demo.png",
                "document_type": "scanned_image",
                "reference_id": "DEMO-USS-RULES-2026-SCAN",
                "expected_attachment_status": "ocr_test_asset",
                "description": "Scanned image representation of scholarship instructions for OCR testing.",
                "relevant_scenarios": ["OCR Testing"]
            }
        ]
    }
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f"Generated manifest: {manifest_path}")


def main():
    print("Generating demo assets...")
    generate_instructions_pdf()
    generate_instructions_txt()
    generate_application_form_pdf()
    generate_application_form_txt()
    generate_marksheet_pdf("Academic_Marksheet_Demo.pdf", "78%", is_inconsistent=False)
    generate_marksheet_pdf("Academic_Marksheet_Inconsistent_Demo.pdf", "58%", is_inconsistent=True)
    generate_identity_pdf()
    generate_income_certificate_pdf()
    generate_bank_passbook_pdf()
    generate_institution_certificate_pdf()
    generate_declaration_pdf()
    generate_scanned_pngs()
    generate_manifest()
    print("All demo assets successfully generated!")


if __name__ == "__main__":
    main()
