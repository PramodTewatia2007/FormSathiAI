from typing import List
from .models import ApplicationFormData, ValidationAlert, ValidationResponse
from .config import FICTIONAL_DEMO_WARNING
from .demo_data import SCHOLARSHIP_RULES


def format_indian_currency(amount: int) -> str:
    """Format an integer using the grouping convention used in Indian rupees."""
    digits = str(amount)
    if len(digits) <= 3:
        return digits
    last_three = digits[-3:]
    remaining = digits[:-3]
    groups = []
    while remaining:
        groups.insert(0, remaining[-2:])
        remaining = remaining[:-2]
    return ",".join([*groups, last_three])


def validate_application(form: ApplicationFormData) -> ValidationResponse:
    """
    Validate application fields against scholarship rules and uploaded supporting documents.
    Categorizes alerts into confirmed, missing, inconsistency, unverified, and unavailable.
    """
    alerts: List[ValidationAlert] = []
    income_limit = SCHOLARSHIP_RULES["annual_family_income_limit"]
    marks_minimum = SCHOLARSHIP_RULES["minimum_qualifying_marks"]

    # 1. Blank Required Field Checks
    if not form.student_name.strip():
        alerts.append(ValidationAlert(
            category="missing",
            field_name="student_name",
            message_en="Student name is missing. The field is blank.",
            message_hi="विद्यार्थी का नाम अनुपलब्ध है। यह फ़ील्ड खाली है।",
            resolution_hint_en="Enter the applicant's full legal name as shown on official certificates.",
            resolution_hint_hi="आवेदक का पूरा नाम जैसा कि प्रमाणपत्रों में है, दर्ज करें।",
            severity="error"
        ))

    if not form.course.strip():
        alerts.append(ValidationAlert(
            category="missing",
            field_name="course",
            message_en="Course name is missing.",
            message_hi="पाठ्यक्रम का नाम अनुपलब्ध है।",
            resolution_hint_en="Select or enter the enrolled undergraduate course (e.g. B.Tech, B.Sc., B.A., B.Com.).",
            resolution_hint_hi="नामांकित स्नातक पाठ्यक्रम का चयन या प्रविष्टि करें।",
            severity="error"
        ))

    # 2. Academic Marks & Inconsistency Check
    demo_marksheet_values = {
        "Academic_Marksheet_Demo.pdf": 78.0,
        "Academic_Marksheet_Inconsistent_Demo.pdf": 58.0,
    }
    marksheet_pct = demo_marksheet_values.get(form.active_marksheet_filename)

    if marksheet_pct is not None and abs(form.qualifying_marks_pct - marksheet_pct) > 0.01:
        alerts.append(ValidationAlert(
            category="inconsistency",
            field_name="qualifying_marks_pct",
            message_en=f"Potential inconsistency detected: the application records {int(form.qualifying_marks_pct)}%, while the selected marksheet records {int(marksheet_pct)}%. Please check the original document.",
            message_hi=f"संभावित विसंगति पाई गई: आवेदन में {int(form.qualifying_marks_pct)}% दर्ज है, जबकि चुने गए अंकपत्र में {int(marksheet_pct)}% दर्ज है। कृपया मूल दस्तावेज की जाँच करें।",
            resolution_hint_en="Review both the application form and the physical marksheet. Verify the correct marks before updating the form.",
            resolution_hint_hi="आवेदन पत्र और मूल अंकपत्र दोनों की समीक्षा करें और सही अंक देखकर अद्यतन करें।",
            severity="warning"
        ))
    else:
        if form.qualifying_marks_pct >= marks_minimum:
            alerts.append(ValidationAlert(
                category="confirmed",
                field_name="qualifying_marks_pct",
                message_en=f"Entered qualifying marks ({form.qualifying_marks_pct}%) meet the minimum requirement of {int(marks_minimum)}%.",
                message_hi=f"दर्ज पात्रता अंक ({form.qualifying_marks_pct}%) न्यूनतम {int(marks_minimum)}% की आवश्यकता को पूरा करते हैं।",
                resolution_hint_en="The entered value meets this numerical criterion. Meeting it does not guarantee scholarship selection.",
                resolution_hint_hi="पुष्ट मानदंड। यह मानदंड पूरा करने से छात्रवृत्ति की गारंटी नहीं मिलती।",
                severity="info"
            ))
        else:
            alerts.append(ValidationAlert(
                category="inconsistency",
                field_name="qualifying_marks_pct",
                message_en=f"Marks ({form.qualifying_marks_pct}%) fall below the minimum fictional cutoff of {int(marks_minimum)}%.",
                message_hi=f"अंक ({form.qualifying_marks_pct}%) न्यूनतम {int(marks_minimum)}% की काल्पनिक सीमा से कम हैं।",
                resolution_hint_en="Applicant does not meet the fictional minimum academic criteria.",
                resolution_hint_hi="आवेदक काल्पनिक न्यूनतम शैक्षणिक मानदंड को पूरा नहीं करता है।",
                severity="error"
            ))

        if marksheet_pct is None:
            alerts.append(ValidationAlert(
                category="unavailable",
                field_name="qualifying_marks_pct",
                message_en="The uploaded marksheet value was not automatically verified. Compare the entered marks with the original document.",
                message_hi="अपलोड किए गए अंकपत्र के अंक स्वतः सत्यापित नहीं हुए। दर्ज अंकों की मूल दस्तावेज़ से तुलना करें।",
                resolution_hint_en="Review the original marksheet and confirm the value before relying on this result.",
                resolution_hint_hi="इस परिणाम पर भरोसा करने से पहले मूल अंकपत्र देखकर दर्ज मान की पुष्टि करें।",
                severity="warning"
            ))

    # 3. Family Income Criteria Check
    if form.annual_family_income > income_limit:
        alerts.append(ValidationAlert(
            category="inconsistency",
            field_name="annual_family_income",
            message_en=f"The declared income of ₹{format_indian_currency(form.annual_family_income)} exceeds the fictional scholarship limit of ₹{format_indian_currency(income_limit)}. The sample application does not meet this specific income criterion.",
            message_hi=f"घोषित आय ₹{format_indian_currency(form.annual_family_income)} काल्पनिक छात्रवृत्ति सीमा ₹{format_indian_currency(income_limit)} से अधिक है। यह नमूना आवेदन इस विशिष्ट आय मानदंड को पूरा नहीं करता है।",
            resolution_hint_en="Review the family income or check if another category or scholarship applies.",
            resolution_hint_hi="पारिवारिक आय की समीक्षा करें या अन्य उपयुक्त श्रेणी की जाँच करें।",
            severity="error"
        ))
    else:
        alerts.append(ValidationAlert(
            category="confirmed",
            field_name="annual_family_income",
            message_en=f"Declared annual family income (₹{format_indian_currency(form.annual_family_income)}) is within the fictional limit of ₹{format_indian_currency(income_limit)}.",
            message_hi=f"घोषित वार्षिक पारिवारिक आय (₹{format_indian_currency(form.annual_family_income)}) काल्पनिक सीमा ₹{format_indian_currency(income_limit)} के भीतर है।",
            resolution_hint_en="Income meets numerical ceiling. Supporting income certificate must be uploaded.",
            resolution_hint_hi="आय सीमा पूरी है। पुष्टि के लिए आय प्रमाणपत्र अपलोड किया जाना आवश्यक है।",
            severity="info"
        ))

    # 4. Missing Document Alerts
    if not form.income_cert_attached:
        alerts.append(ValidationAlert(
            category="missing",
            field_name="income_cert_attached",
            message_en="Income certificate is missing from the application.",
            message_hi="आवेदन में आय प्रमाणपत्र संलग्न नहीं है।",
            resolution_hint_en="Upload or attach the official income certificate to verify declared income.",
            resolution_hint_hi="घोषित आय की पुष्टि के लिए आधिकारिक आय प्रमाणपत्र अपलोड करें।",
            severity="warning"
        ))

    if not form.passbook_attached:
        alerts.append(ValidationAlert(
            category="missing",
            field_name="passbook_attached",
            message_en="Bank passbook copy is missing.",
            message_hi="बैंक पासबुक की प्रति संलग्न नहीं है।",
            resolution_hint_en="Upload a clear copy of the applicant's bank passbook showing account and IFSC details.",
            resolution_hint_hi="आवेदक के बैंक खाते और IFSC विवरण दर्शाने वाली पासबुक की प्रति अपलोड करें।",
            severity="warning"
        ))

    if not form.institution_cert_attached:
        alerts.append(ValidationAlert(
            category="missing",
            field_name="institution_cert_attached",
            message_en="Institution enrollment certificate is missing.",
            message_hi="संस्थान नामांकन प्रमाणपत्र अनुपलब्ध है।",
            resolution_hint_en="Upload enrollment certificate issued by Sunrise Institute of Technology.",
            resolution_hint_hi="संस्थान द्वारा जारी नामांकन प्रमाणपत्र अपलोड करें।",
            severity="warning"
        ))

    # 5. Unverified Documents (Classification: Placeholder, not official verification)
    if form.identity_proof_attached:
        alerts.append(ValidationAlert(
            category="unverified",
            field_name="identity_proof",
            message_en="Identity document is attached but has not been independently verified.",
            message_hi="पहचान दस्तावेज़ संलग्न है, लेकिन इसकी स्वतंत्र रूप से पुष्टि नहीं हुई है।",
            resolution_hint_en="Check the document against the original and confirm that it is an accepted identity document.",
            resolution_hint_hi="केवल प्रदर्शन के लिए। वास्तविक आवेदनों में मान्य सरकारी पहचान पत्र आवश्यक होता है।",
            severity="info"
        ))

    if form.marksheet_attached:
        alerts.append(ValidationAlert(
            category="unverified",
            field_name="marksheet_attached",
            message_en="Marksheet is marked as attached, but its authenticity and marks have not been independently verified.",
            message_hi="अंकपत्र संलग्न दिखाया गया है, लेकिन इसकी प्रामाणिकता और अंकों की स्वतंत्र पुष्टि नहीं हुई है।",
            resolution_hint_en="Compare the entered marks with the original marksheet and confirm the document with its issuing institution.",
            resolution_hint_hi="दर्ज अंकों की मूल अंकपत्र से तुलना करें और जारी करने वाले संस्थान से दस्तावेज़ की पुष्टि करें।",
            severity="info"
        ))

    if form.income_cert_attached:
        alerts.append(ValidationAlert(
            category="unverified",
            field_name="income_cert_attached",
            message_en="Income certificate is marked as attached, but the issuing authority and declared income have not been independently verified.",
            message_hi="आय प्रमाणपत्र संलग्न दिखाया गया है, लेकिन जारीकर्ता प्राधिकरण और घोषित आय की स्वतंत्र पुष्टि नहीं हुई है।",
            resolution_hint_en="Check the original certificate and confirm its details with the issuing authority.",
            resolution_hint_hi="मूल प्रमाणपत्र देखें और जारीकर्ता प्राधिकरण से इसके विवरण की पुष्टि करें।",
            severity="info"
        ))

    if form.passbook_attached:
        alerts.append(ValidationAlert(
            category="unverified",
            field_name="passbook_attached",
            message_en="Bank passbook is marked as attached, but its account details have not been independently verified.",
            message_hi="बैंक पासबुक संलग्न दिखाया गया है, लेकिन खाते के विवरण की स्वतंत्र पुष्टि नहीं हुई है।",
            resolution_hint_en="Review the original passbook and verify the account details with the bank.",
            resolution_hint_hi="मूल पासबुक देखें और बैंक से खाते के विवरण की पुष्टि करें।",
            severity="info"
        ))

    if form.institution_cert_attached:
        alerts.append(ValidationAlert(
            category="unverified",
            field_name="institution_certificate",
            message_en="Institution certificate is attached but has not been independently verified.",
            message_hi="संस्थान प्रमाणपत्र संलग्न है, लेकिन इसकी स्वतंत्र रूप से पुष्टि नहीं हुई है।",
            resolution_hint_en="File is readable, but has not been verified by an official institution authority.",
            resolution_hint_hi="दस्तावेज पठनीय है, किंतु किसी आधिकारिक संस्थान द्वारा सत्यापित नहीं है।",
            severity="info"
        ))

    # 6. Applicant Declaration
    if not form.declaration_accepted:
        alerts.append(ValidationAlert(
            category="missing",
            field_name="declaration_accepted",
            message_en="Applicant declaration has not been reviewed and accepted.",
            message_hi="आवेदक घोषणा की समीक्षा और स्वीकृति नहीं की गई है।",
            resolution_hint_en="The applicant must manually review and confirm the declaration. FormSathiAI will never auto-sign.",
            resolution_hint_hi="आवेदक को घोषणा की स्वयं समीक्षा कर स्वीकार करना होगा। FormSathiAI कभी स्वचालित हस्ताक्षर नहीं करता।",
            severity="warning"
        ))
    else:
        alerts.append(ValidationAlert(
            category="confirmed",
            field_name="declaration_accepted",
            message_en="Applicant declaration accepted by user.",
            message_hi="उपयोगकर्ता द्वारा आवेदक घोषणा स्वीकार कर ली गई है।",
            resolution_hint_en="Confirmed by explicit user review.",
            resolution_hint_hi="उपयोगकर्ता की स्पष्ट समीक्षा द्वारा पुष्ट।",
            severity="info"
        ))

    # Eligibility overview summary
    has_errors = any(a.severity == "error" for a in alerts)
    has_missing = any(a.category == "missing" for a in alerts)
    has_inconsistency = any(a.category == "inconsistency" for a in alerts)
    has_unverified = any(a.category == "unverified" for a in alerts)

    if has_errors or has_inconsistency:
        summary_en = "Application has discrepancies or disqualifying criteria that need attention."
        summary_hi = "आवेदन में विसंगतियाँ या अपात्रता कारक हैं जिन पर ध्यान देने की आवश्यकता है।"
        eligible = False
    elif has_missing:
        summary_en = "Application criteria are partially met, but required documents and declaration remain incomplete."
        summary_hi = "आवेदन के मानदंड आंशिक रूप से पूरे हैं, लेकिन आवश्यक दस्तावेज और घोषणा अभी बाकी हैं।"
        eligible = None
    elif has_unverified:
        summary_en = "The entered criteria and attachment checklist appear complete, but supporting documents remain unverified, so eligibility cannot be confirmed."
        summary_hi = "दर्ज मानदंड और संलग्नक सूची पूरी दिखती है, लेकिन सहायक दस्तावेज़ अपुष्ट हैं, इसलिए पात्रता की पुष्टि नहीं की जा सकती।"
        eligible = None
    else:
        summary_en = "All fictional demo requirements and documents are attached and satisfied."
        summary_hi = "सभी काल्पनिक नमूना आवश्यकताएँ और दस्तावेज संलग्न व पूरे हैं।"
        eligible = True

    return ValidationResponse(
        application_id=form.application_id,
        is_eligible=eligible,
        eligibility_summary_en=summary_en,
        eligibility_summary_hi=summary_hi,
        alerts=alerts,
        fictional_warning=FICTIONAL_DEMO_WARNING
    )
