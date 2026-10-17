"""
Demo data definitions, bilingual explanations, scenarios, and exact predefined Q&A.
"""

from typing import Dict, List, Any
from .models import ApplicationFormData, DemoScenario, FieldExplanation, SourceCitation
from .config import FICTIONAL_DEMO_WARNING

SCHOLARSHIP_RULES = {
    "scholarship_name": "Udaan Student Support Scholarship 2026–27",
    "issuing_organization": "Udaan Education Foundation (fictional)",
    "reference_id": "DEMO-USS-RULES-2026",
    "academic_session": "2026–27",
    "eligible_study_level": "First-year undergraduate",
    "minimum_qualifying_marks": 60.0,
    "annual_family_income_limit": 250000,
    "application_deadline": "30 November 2026",
    "submission_method": "Fictional demonstration portal",
    "accepted_courses": [
        "Bachelor of Technology (B.Tech)",
        "Bachelor of Science (B.Sc.)",
        "Bachelor of Arts (B.A.)",
        "Bachelor of Commerce (B.Com.)"
    ],
    "warning": FICTIONAL_DEMO_WARNING
}

FIELD_EXPLANATIONS: Dict[str, FieldExplanation] = {
    "annual_family_income": FieldExplanation(
        field_key="annual_family_income",
        label_en="Annual family income",
        label_hi="वार्षिक पारिवारिक आय",
        explanation_en="Total income earned by the student's family in one year.",
        explanation_hi="विद्यार्थी के परिवार द्वारा एक वर्ष में अर्जित की गई कुल आय।",
        source_reference="Udaan_Scholarship_Instructions_Demo.pdf, Section 3 — Family Income Criteria",
        required_in_instructions=True
    ),
    "qualifying_marks_pct": FieldExplanation(
        field_key="qualifying_marks_pct",
        label_en="Qualifying examination marks",
        label_hi="पात्रता परीक्षा के अंक",
        explanation_en="Marks obtained in the examination used to assess scholarship eligibility.",
        explanation_hi="छात्रवृत्ति की पात्रता जाँचने के लिए उपयोग की जाने वाली परीक्षा में प्राप्त अंक।",
        source_reference="Udaan_Scholarship_Instructions_Demo.pdf, Section 1 — Academic Eligibility",
        required_in_instructions=True
    ),
    "income_cert_attached": FieldExplanation(
        field_key="income_cert_attached",
        label_en="Income certificate",
        label_hi="आय प्रमाणपत्र",
        explanation_en="A document issued by an authorized body to verify family income.",
        explanation_hi="परिवार की आय की पुष्टि करने के लिए अधिकृत संस्था द्वारा जारी किया गया प्रमाणपत्र।",
        source_reference="Udaan_Scholarship_Instructions_Demo.pdf, Section 4 — Required Documents",
        required_in_instructions=True
    ),
    "institution_cert_attached": FieldExplanation(
        field_key="institution_cert_attached",
        label_en="Institution certificate",
        label_hi="संस्थान प्रमाणपत्र",
        explanation_en="A document confirming the student's enrollment at an educational institution.",
        explanation_hi="विद्यार्थी के किसी शैक्षणिक संस्थान में नामांकन की पुष्टि करने वाला प्रमाणपत्र।",
        source_reference="Udaan_Scholarship_Instructions_Demo.pdf, Section 4 — Required Documents",
        required_in_instructions=True
    ),
    "passbook_attached": FieldExplanation(
        field_key="passbook_attached",
        label_en="Bank passbook copy",
        label_hi="बैंक पासबुक की प्रति",
        explanation_en="A copy used to show the beneficiary's bank account details.",
        explanation_hi="लाभार्थी के बैंक खाते का विवरण दिखाने के लिए उपयोग की जाने वाली पासबुक की प्रति।",
        source_reference="Udaan_Scholarship_Instructions_Demo.pdf, Section 4 — Required Documents",
        required_in_instructions=True
    ),
    "declaration_accepted": FieldExplanation(
        field_key="declaration_accepted",
        label_en="Declaration",
        label_hi="घोषणा पत्र",
        explanation_en="A statement confirming that the applicant has reviewed the information supplied.",
        explanation_hi="एक घोषणा जिसमें आवेदक पुष्टि करता है कि उसने दी गई जानकारी की जाँच कर ली है।",
        source_reference="Udaan_Scholarship_Instructions_Demo.pdf, Section 5 & Section 9",
        required_in_instructions=True
    ),
    "student_name": FieldExplanation(
        field_key="student_name",
        label_en="Student name",
        label_hi="विद्यार्थी का नाम",
        explanation_en="Full legal name of the applicant as displayed on official school/college documents.",
        explanation_hi="आवेदक का पूरा नाम जैसा कि उसके आधिकारिक शैक्षणिक प्रमाणपत्रों पर दर्ज है।",
        source_reference="Udaan_Scholarship_Instructions_Demo.pdf, Section 5 — Completing the Form",
        required_in_instructions=True
    ),
    "course": FieldExplanation(
        field_key="course",
        label_en="Course",
        label_hi="पाठ्यक्रम",
        explanation_en="The undergraduate degree program in which the student is currently enrolled.",
        explanation_hi="स्नातक पाठ्यक्रम जिसमें विद्यार्थी वर्तमान में नामांकित है।",
        source_reference="Udaan_Scholarship_Instructions_Demo.pdf, Section 2 — Eligible Courses",
        required_in_instructions=True
    )
}

EXACT_DEMO_QA = [
    {
        "question_en": "What is the minimum marks requirement?",
        "question_hi": "न्यूनतम कितने प्रतिशत अंक आवश्यक हैं?",
        "answer_en": "The fictional Udaan scholarship requires at least 60% in the qualifying examination.",
        "answer_hi": "इस काल्पनिक उड़ान छात्रवृत्ति के लिए पिछली पात्रता परीक्षा में कम से कम 60% अंक आवश्यक हैं।",
        "citation": SourceCitation(
            document_name="Udaan_Scholarship_Instructions_Demo.pdf",
            page_number=1,
            section_heading="Section 1: Academic Eligibility",
            supporting_quote="2. Applicants must have obtained at least 60% marks in their qualifying examination."
        )
    },
    {
        "question_en": "What is the annual family income limit?",
        "question_hi": "वार्षिक पारिवारिक आय की अधिकतम सीमा क्या है?",
        "answer_en": "The fictional annual family income limit is ₹2,50,000.",
        "answer_hi": "इस काल्पनिक छात्रवृत्ति के लिए परिवार की वार्षिक आय की सीमा ₹2,50,000 है।",
        "citation": SourceCitation(
            document_name="Udaan_Scholarship_Instructions_Demo.pdf",
            page_number=2,
            section_heading="Section 3: Family Income Criteria",
            supporting_quote="1. The fictional annual family income limit is ₹2,50,000."
        )
    },
    {
        "question_en": "Which documents are required?",
        "question_hi": "कौन-कौन से दस्तावेज आवश्यक हैं?",
        "answer_en": "The sample instructions list an academic marksheet, identity proof, income certificate, bank passbook copy, institution certificate, and completed applicant declaration.",
        "answer_hi": "नमूना निर्देशों के अनुसार अंकपत्र, पहचान प्रमाण, आय प्रमाणपत्र, बैंक पासबुक की प्रति, संस्थान प्रमाणपत्र और पूर्ण आवेदक घोषणा आवश्यक हैं।",
        "citation": SourceCitation(
            document_name="Udaan_Scholarship_Instructions_Demo.pdf",
            page_number=2,
            section_heading="Section 4: Required Documents",
            supporting_quote="The fictional instructions list: 1. Academic marksheet. 2. Identity proof. 3. Income certificate. 4. Bank passbook copy. 5. Institution certificate. 6. Completed applicant declaration."
        )
    },
    {
        "question_en": "What is the deadline?",
        "question_hi": "आवेदन करने की अंतिम तिथि क्या है?",
        "answer_en": "The fictional application deadline is 30 November 2026.",
        "answer_hi": "इस काल्पनिक आवेदन की अंतिम तिथि 30 नवंबर 2026 है।",
        "citation": SourceCitation(
            document_name="Udaan_Scholarship_Instructions_Demo.pdf",
            page_number=4,
            section_heading="Section 8: Application Deadline",
            supporting_quote="Fictional deadline: 30 November 2026."
        )
    },
    {
        "question_en": "Is my application complete?",
        "question_hi": "क्या मेरा आवेदन पूरा हो गया है?",
        "answer_en": "Not yet. The default sample is missing the income certificate, bank passbook copy, and completed declaration.",
        "answer_hi": "अभी नहीं। नमूने में आय प्रमाणपत्र, बैंक पासबुक की प्रति और पूर्ण घोषणा उपलब्ध नहीं हैं।",
        "citation": SourceCitation(
            document_name="Udaan_Application_Form_Demo.pdf",
            page_number=1,
            section_heading="Sections C, D, E & Dynamic Checklist",
            supporting_quote="Income cert: No, Passbook: No, Declaration: Not accepted"
        )
    },
    {
        "question_en": "Is this a real scholarship?",
        "question_hi": "क्या यह कोई वास्तविक छात्रवृत्ति है?",
        "answer_en": "No. Udaan Student Support Scholarship is fictional demo data created to demonstrate FormSathiAI. It is not an official scholarship.",
        "answer_hi": "नहीं। उड़ान छात्रवृत्ति केवल FormSathiAI के प्रदर्शन के लिए बनाया गया काल्पनिक उदाहरण है। यह कोई आधिकारिक छात्रवृत्ति नहीं है।",
        "citation": SourceCitation(
            document_name="Udaan_Scholarship_Instructions_Demo.pdf",
            page_number=4,
            section_heading="Section 10: Limits of This Document",
            supporting_quote="This document is fictional and is not an official scholarship notification."
        )
    }
]

def get_default_application() -> ApplicationFormData:
    return ApplicationFormData(
        application_id="DEMO-USS-2026-001",
        student_name="Aarav Sharma",
        dob="15/08/2007",
        course="B.Tech Computer Science",
        study_year="First year",
        institution="Sunrise Institute of Technology",
        qualifying_marks_pct=78.0,
        annual_family_income=180000,
        marksheet_attached=True,
        identity_proof_attached=True,
        income_cert_attached=False,
        passbook_attached=False,
        institution_cert_attached=True,
        declaration_accepted=False,
        applicant_signature=None,
        declaration_date=None,
        bank_account_holder="Aarav Sharma",
        bank_account_reference="DEMO-ACCOUNT-0001",
        application_status="Incomplete",
        active_marksheet_filename="Academic_Marksheet_Demo.pdf"
    )

def get_demo_scenarios() -> List[DemoScenario]:
    # Scenario 1
    s1_form = get_default_application()
    
    # Scenario 2: Missing Information
    s2_form = get_default_application()
    s2_form.student_name = ""
    s2_form.institution_cert_attached = False
    s2_form.declaration_accepted = False

    # Scenario 3: Inconsistent Marks
    s3_form = get_default_application()
    s3_form.qualifying_marks_pct = 78.0
    s3_form.active_marksheet_filename = "Academic_Marksheet_Inconsistent_Demo.pdf"

    # Scenario 4: Income Limit Exceeded
    s4_form = get_default_application()
    s4_form.annual_family_income = 280000

    return [
        DemoScenario(
            scenario_id="scenario_1",
            title_en="Scenario 1 — Eligible Sample",
            title_hi="परिदृश्य 1 — पात्र नमूना",
            description_en="Default application (Marks: 78%, Income: ₹1,80,000). Meets criteria, but lacks income certificate, passbook, and declaration.",
            description_hi="डिफ़ॉल्ट आवेदन (अंक: 78%, आय: ₹1,80,000)। मानदंड पूरे हैं, लेकिन आय प्रमाणपत्र, पासबुक और घोषणा बाकी हैं।",
            form_values=s1_form
        ),
        DemoScenario(
            scenario_id="scenario_2",
            title_en="Scenario 2 — Missing Information",
            title_hi="परिदृश्य 2 — अधूरी जानकारी",
            description_en="Student name is blank, institution certificate removed, and declaration incomplete.",
            description_hi="विद्यार्थी का नाम खाली है, संस्थान प्रमाणपत्र नहीं है, और घोषणा अधूरी है।",
            form_values=s2_form
        ),
        DemoScenario(
            scenario_id="scenario_3",
            title_en="Scenario 3 — Inconsistent Marks",
            title_hi="परिदृश्य 3 — अंकों में विसंगति",
            description_en="Application claims 78%, but attached alternate marksheet shows 58%. System flags discrepancy.",
            description_hi="आवेदन में 78% दर्ज है, जबकि संलग्न अंकपत्र 58% दर्शाता है। प्रणाली विसंगति का संकेत देती है।",
            form_values=s3_form
        ),
        DemoScenario(
            scenario_id="scenario_4",
            title_en="Scenario 4 — Income Limit Exceeded",
            title_hi="परिदृश्य 4 — आय सीमा से अधिक",
            description_en="Declared family income is ₹2,80,000, exceeding the fictional ₹2,50,000 ceiling.",
            description_hi="घोषित पारिवारिक आय ₹2,80,000 है, जो काल्पनिक ₹2,50,000 की सीमा से अधिक है।",
            form_values=s4_form
        )
    ]
