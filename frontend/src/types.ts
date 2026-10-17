export type Language = 'en' | 'hi';

export interface ApplicationFormData {
  application_id: string;
  student_name: string;
  dob: string;
  course: string;
  study_year: string;
  institution: string;
  qualifying_marks_pct: number;
  annual_family_income: number;
  marksheet_attached: boolean;
  identity_proof_attached: boolean;
  income_cert_attached: boolean;
  passbook_attached: boolean;
  institution_cert_attached: boolean;
  declaration_accepted: boolean;
  applicant_signature?: string | null;
  declaration_date?: string | null;
  bank_account_holder: string;
  bank_account_reference: string;
  application_status: string;
  active_marksheet_filename: string;
}

export interface DocumentMetadata {
  document_id: string;
  filename: string;
  file_type: string;
  file_size_bytes: number;
  page_count: number;
  upload_timestamp: string;
  extraction_method: 'digital_pdf' | 'ocr_image' | 'fallback_extracted';
  ocr_confidence?: number | null;
  extracted_text: string;
  needs_ocr_review: boolean;
  is_fictional_placeholder: boolean;
  verification_status: 'verified' | 'unverified' | 'missing';
}

export interface SourceCitation {
  document_name: string;
  page_number?: number | null;
  section_heading?: string | null;
  supporting_quote?: string | null;
}

export interface AskQuestionResponse {
  question: string;
  language: Language;
  answer: string;
  source_citation: SourceCitation;
  is_live_ai: boolean;
  is_predefined_grounded: boolean;
  warning: string;
}

export interface ChecklistItem {
  key: string;
  title_en: string;
  title_hi: string;
  status: 'completed' | 'missing' | 'unverified';
  is_placeholder: boolean;
  source_document?: string | null;
  details_en: string;
  details_hi: string;
}

export interface ChecklistResponse {
  total_items: number;
  completed_items: number;
  remaining_items: number;
  overall_status: 'Complete' | 'Incomplete';
  items: ChecklistItem[];
  disclaimer: string;
}

export interface ValidationAlert {
  category: 'confirmed' | 'missing' | 'inconsistency' | 'unverified' | 'unavailable';
  field_name: string;
  message_en: string;
  message_hi: string;
  resolution_hint_en: string;
  resolution_hint_hi: string;
  severity: 'info' | 'warning' | 'error';
}

export interface ValidationResponse {
  application_id: string;
  is_eligible?: boolean | null;
  eligibility_summary_en: string;
  eligibility_summary_hi: string;
  alerts: ValidationAlert[];
  fictional_warning: string;
}

export interface FieldExplanation {
  field_key: string;
  label_en: string;
  label_hi: string;
  explanation_en: string;
  explanation_hi: string;
  source_reference?: string | null;
  required_in_instructions: boolean;
}

export interface DemoScenario {
  scenario_id: string;
  title_en: string;
  title_hi: string;
  description_en: string;
  description_hi: string;
}

export interface PredefinedQuestion {
  question_en: string;
  question_hi: string;
  answer_en: string;
  answer_hi: string;
  citation: SourceCitation;
}
