from typing import List
from .models import ApplicationFormData, ChecklistItem, ChecklistResponse
from .config import FICTIONAL_DEMO_WARNING


def generate_checklist(form: ApplicationFormData) -> ChecklistResponse:
    """Generate dynamic checklist based on application form state."""
    items: List[ChecklistItem] = []

    # 1. Academic marksheet
    if form.marksheet_attached:
        items.append(ChecklistItem(
            key="marksheet",
            title_en="Academic marksheet uploaded",
            title_hi="शैक्षणिक अंकपत्र अपलोड किया गया",
            status="completed",
            is_placeholder=False,
            source_document=form.active_marksheet_filename,
            details_en=f"Marksheet ({form.active_marksheet_filename}) attached with qualifying records.",
            details_hi=f"अंकपत्र ({form.active_marksheet_filename}) संलग्न है।"
        ))
    else:
        items.append(ChecklistItem(
            key="marksheet",
            title_en="Academic marksheet uploaded",
            title_hi="शैक्षणिक अंकपत्र अपलोड किया गया",
            status="missing",
            is_placeholder=False,
            source_document=None,
            details_en="Academic marksheet is required to evaluate eligibility.",
            details_hi="पात्रता की समीक्षा के लिए शैक्षणिक अंकपत्र आवश्यक है।"
        ))

    # 2. Identity proof
    if form.identity_proof_attached:
        items.append(ChecklistItem(
            key="identity_proof",
            title_en="Identity proof placeholder uploaded",
            title_hi="पहचान प्रमाण प्लेसहोल्डर अपलोड किया गया",
            status="completed",
            is_placeholder=True,
            source_document="Identity_Proof_Placeholder_Demo.pdf",
            details_en="Fictional identity placeholder attached (Unverified sample).",
            details_hi="काल्पनिक पहचान प्लेसहोल्डर संलग्न (अपुष्ट नमूना)।"
        ))
    else:
        items.append(ChecklistItem(
            key="identity_proof",
            title_en="Identity proof placeholder uploaded",
            title_hi="पहचान प्रमाण प्लेसहोल्डर अपलोड किया गया",
            status="missing",
            is_placeholder=True,
            source_document=None,
            details_en="Identity proof document is missing.",
            details_hi="पहचान प्रमाण दस्तावेज अनुपलब्ध है।"
        ))

    # 3. Income certificate
    if form.income_cert_attached:
        items.append(ChecklistItem(
            key="income_cert",
            title_en="Income certificate uploaded",
            title_hi="आय प्रमाणपत्र अपलोड किया गया",
            status="completed",
            is_placeholder=True,
            source_document="Income_Certificate_Placeholder_Demo.pdf",
            details_en="Fictional income certificate attached.",
            details_hi="काल्पनिक आय प्रमाणपत्र संलग्न है।"
        ))
    else:
        items.append(ChecklistItem(
            key="income_cert",
            title_en="Income certificate uploaded",
            title_hi="आय प्रमाणपत्र अपलोड किया गया",
            status="missing",
            is_placeholder=False,
            source_document=None,
            details_en="Income certificate required to verify annual family income limit (₹2,50,000).",
            details_hi="वार्षिक पारिवारिक आय सीमा (₹2,50,000) की पुष्टि के लिए आय प्रमाणपत्र आवश्यक है।"
        ))

    # 4. Bank passbook copy
    if form.passbook_attached:
        items.append(ChecklistItem(
            key="passbook",
            title_en="Bank passbook copy uploaded",
            title_hi="बैंक पासबुक की प्रति अपलोड की गई",
            status="completed",
            is_placeholder=True,
            source_document="Bank_Passbook_Placeholder_Demo.pdf",
            details_en="Fictional bank passbook copy attached.",
            details_hi="काल्पनिक बैंक पासबुक प्रति संलग्न है।"
        ))
    else:
        items.append(ChecklistItem(
            key="passbook",
            title_en="Bank passbook copy uploaded",
            title_hi="बैंक पासबुक की प्रति अपलोड की गई",
            status="missing",
            is_placeholder=False,
            source_document=None,
            details_en="Bank passbook copy required for scholarship disbursement details.",
            details_hi="छात्रवृत्ति वितरण विवरण के लिए बैंक पासबुक की प्रति आवश्यक है।"
        ))

    # 5. Institution certificate
    if form.institution_cert_attached:
        items.append(ChecklistItem(
            key="institution_cert",
            title_en="Institution certificate attached",
            title_hi="संस्थान प्रमाणपत्र संलग्न किया गया",
            status="completed",
            is_placeholder=True,
            source_document="Institution_Certificate_Demo.pdf",
            details_en="Student enrollment certificate attached (Unverified sample).",
            details_hi="विद्यार्थी नामांकन प्रमाणपत्र संलग्न (अपुष्ट नमूना)।"
        ))
    else:
        items.append(ChecklistItem(
            key="institution_cert",
            title_en="Institution certificate attached",
            title_hi="संस्थान प्रमाणपत्र संलग्न किया गया",
            status="missing",
            is_placeholder=False,
            source_document=None,
            details_en="Institution enrollment certificate is missing.",
            details_hi="संस्थान नामांकन प्रमाणपत्र अनुपलब्ध है।"
        ))

    # 6. Applicant declaration
    if form.declaration_accepted:
        items.append(ChecklistItem(
            key="declaration",
            title_en="Applicant declaration completed",
            title_hi="आवेदक घोषणा पूर्ण की गई",
            status="completed",
            is_placeholder=False,
            source_document="Applicant_Declaration_Demo.pdf",
            details_en="Applicant declaration accepted by user.",
            details_hi="आवेदक घोषणा उपयोगकर्ता द्वारा स्वीकार कर ली गई है।"
        ))
    else:
        items.append(ChecklistItem(
            key="declaration",
            title_en="Applicant declaration completed",
            title_hi="आवेदक घोषणा पूर्ण की गई",
            status="missing",
            is_placeholder=False,
            source_document=None,
            details_en="Declaration must be explicitly reviewed and accepted by the applicant.",
            details_hi="घोषणा पत्र की आवेदक द्वारा स्पष्ट रूप से समीक्षा और स्वीकृति आवश्यक है।"
        ))

    completed = sum(1 for i in items if i.status == "completed")
    total = len(items)
    remaining = total - completed
    overall = "Complete" if remaining == 0 else "Incomplete"

    return ChecklistResponse(
        total_items=total,
        completed_items=completed,
        remaining_items=remaining,
        overall_status=overall,
        items=items,
        disclaimer=FICTIONAL_DEMO_WARNING
    )
