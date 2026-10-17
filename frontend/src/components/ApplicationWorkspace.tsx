import React, { useState } from 'react';
import {
  FileText,
  AlertTriangle,
  CheckCircle,
  HelpCircle,
  Info,
  Calendar,
  User,
  GraduationCap,
  IndianRupee,
  Building,
  CheckSquare,
  ShieldCheck,
  ChevronDown,
  Layers
} from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { useApp } from '../context/AppContext';
import { ScenarioSelector } from './ScenarioSelector';
import { FieldExplainer } from './FieldExplainer';
import { AskFormSathi } from './AskFormSathi';
import { ChecklistView } from './ChecklistView';
import { ValidationAlerts } from './ValidationAlerts';

export const ApplicationWorkspace: React.FC = () => {
  const { t, language } = useLanguage();
  const { applicationForm, updateFormField, fieldExplanations, documents, checklist, validation } = useApp();
  const [activeRightTab, setActiveRightTab] = useState<'explanations' | 'ask' | 'checklist' | 'validation'>('validation');

  if (!applicationForm) return null;

  return (
    <div className="space-y-6">
      {/* Scenario Selector Banner */}
      <ScenarioSelector />

      {/* Main Two-Column Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* LEFT PANEL: Form Fields & Application Status (Col 5) */}
        <div className="lg:col-span-5 space-y-5">
          <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-xs">
            <div className="flex items-center justify-between pb-4 border-b border-slate-100">
              <div className="flex items-center space-x-2.5">
                <div className="p-2 bg-blue-100 text-blue-700 rounded-lg">
                  <FileText className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-base font-bold text-slate-900">
                    {t('Application Form Data', 'आवेदन फॉर्म विवरण')}
                  </h3>
                  <p className="text-xs text-slate-500 font-mono">
                    ID: {applicationForm.application_id}
                  </p>
                </div>
              </div>
              <span
                className={`text-xs px-2.5 py-1 rounded-full font-bold ${
                  applicationForm.application_status === 'Complete'
                    ? 'bg-emerald-100 text-emerald-800'
                    : 'bg-amber-100 text-amber-800'
                }`}
              >
                {applicationForm.application_status === 'Complete'
                  ? t('Complete', 'पूर्ण')
                  : t('Incomplete', 'अपूर्ण')}
              </span>
            </div>

            {/* Form Fields Inputs */}
            <div className="space-y-4 mt-4 text-xs">
              {/* Student Name */}
              <div>
                <div className="flex items-center justify-between mb-1">
                  <label className="font-semibold text-slate-700 flex items-center space-x-1">
                    <User className="w-3.5 h-3.5 text-slate-400" />
                    <span>{t('Student Name', 'विद्यार्थी का नाम')}</span>
                  </label>
                  {!applicationForm.student_name.trim() && (
                    <span className="text-[10px] text-amber-600 font-bold bg-amber-50 px-1.5 py-0.5 rounded">
                      {t('Required Missing', 'आवश्यक छूटा हुआ')}
                    </span>
                  )}
                </div>
                <input
                  type="text"
                  value={applicationForm.student_name}
                  onChange={(e) => updateFormField('student_name', e.target.value)}
                  placeholder={t('Enter student name', 'विद्यार्थी का नाम दर्ज करें')}
                  className={`w-full p-2.5 rounded-xl border text-xs focus:ring-2 focus:ring-blue-500 focus:outline-hidden ${
                    !applicationForm.student_name.trim()
                      ? 'border-amber-300 bg-amber-50/30'
                      : 'border-slate-200 bg-slate-50'
                  }`}
                />
              </div>

              {/* Date of Birth & Study Year */}
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="font-semibold text-slate-700 flex items-center space-x-1 mb-1">
                    <Calendar className="w-3.5 h-3.5 text-slate-400" />
                    <span>{t('Date of Birth', 'जन्म तिथि')}</span>
                  </label>
                  <input
                    type="text"
                    value={applicationForm.dob}
                    onChange={(e) => updateFormField('dob', e.target.value)}
                    className="w-full p-2.5 rounded-xl border border-slate-200 bg-slate-50 text-xs"
                  />
                </div>
                <div>
                  <label className="font-semibold text-slate-700 block mb-1">
                    {t('Study Year', 'अध्ययन वर्ष')}
                  </label>
                  <input
                    type="text"
                    value={applicationForm.study_year}
                    onChange={(e) => updateFormField('study_year', e.target.value)}
                    className="w-full p-2.5 rounded-xl border border-slate-200 bg-slate-50 text-xs"
                  />
                </div>
              </div>

              {/* Course & Institution */}
              <div>
                <label className="font-semibold text-slate-700 flex items-center space-x-1 mb-1">
                  <GraduationCap className="w-3.5 h-3.5 text-slate-400" />
                  <span>{t('Course Enrolled', 'नामांकित पाठ्यक्रम')}</span>
                </label>
                <input
                  type="text"
                  value={applicationForm.course}
                  onChange={(e) => updateFormField('course', e.target.value)}
                  className="w-full p-2.5 rounded-xl border border-slate-200 bg-slate-50 text-xs"
                />
              </div>

              <div>
                <label className="font-semibold text-slate-700 flex items-center space-x-1 mb-1">
                  <Building className="w-3.5 h-3.5 text-slate-400" />
                  <span>{t('Institution', 'शैक्षणिक संस्थान')}</span>
                </label>
                <input
                  type="text"
                  value={applicationForm.institution}
                  onChange={(e) => updateFormField('institution', e.target.value)}
                  className="w-full p-2.5 rounded-xl border border-slate-200 bg-slate-50 text-xs"
                />
              </div>

              {/* Qualifying Marks & Annual Family Income */}
              <div className="grid grid-cols-2 gap-3 pt-1">
                <div>
                  <div className="flex items-center justify-between mb-1">
                    <label className="font-semibold text-slate-700">
                      {t('Qualifying Marks', 'पात्रता अंक (%)')}
                    </label>
                    <span className="text-[10px] text-blue-600 font-semibold">{t('Min 60%', 'न्यूनतम 60%')}</span>
                  </div>
                  <input
                    type="number"
                    min={0}
                    max={100}
                    step="0.1"
                    value={applicationForm.qualifying_marks_pct}
                    onChange={(e) => updateFormField('qualifying_marks_pct', parseFloat(e.target.value) || 0)}
                    className="w-full p-2.5 rounded-xl border border-slate-200 bg-slate-50 text-xs font-semibold"
                  />
                  <span className="text-[10px] text-slate-500 mt-0.5 block">
                    {t('Active Marksheet:', 'सक्रिय अंकपत्र:')} {applicationForm.active_marksheet_filename}
                  </span>
                </div>

                <div>
                  <div className="flex items-center justify-between mb-1">
                    <label className="font-semibold text-slate-700 flex items-center space-x-1">
                      <IndianRupee className="w-3 h-3 text-slate-400" />
                      <span>{t('Family Income', 'पारिवारिक आय')}</span>
                    </label>
                    <span className="text-[10px] text-blue-600 font-semibold">{t('Limit ₹2.5L', 'सीमा ₹2.5L')}</span>
                  </div>
                  <input
                    type="number"
                    min={0}
                    value={applicationForm.annual_family_income}
                    onChange={(e) => updateFormField('annual_family_income', parseInt(e.target.value) || 0)}
                    className={`w-full p-2.5 rounded-xl border text-xs font-semibold ${
                      applicationForm.annual_family_income > 250000
                        ? 'border-rose-300 bg-rose-50/50 text-rose-700'
                        : 'border-slate-200 bg-slate-50 text-slate-900'
                    }`}
                  />
                  <span className="text-[10px] text-slate-500 mt-0.5 block">
                    ₹{applicationForm.annual_family_income.toLocaleString('en-IN')} / year
                  </span>
                </div>
              </div>

              {/* Bank Account Reference */}
              <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 space-y-1">
                <span className="text-[10px] uppercase font-bold text-slate-400 block">
                  {t('Disbursement Banking (Fictional Placeholder)', 'वितरण बैंकिंग विवरण (काल्पनिक नमूना)')}
                </span>
                <div className="flex justify-between text-xs">
                  <span className="text-slate-600">{t('Holder:', 'खाताधारक:')} {applicationForm.bank_account_holder}</span>
                  <span className="font-mono text-slate-700">{applicationForm.bank_account_reference}</span>
                </div>
              </div>

              {/* Applicant Declaration Section */}
              <div className="p-3.5 bg-amber-50/60 rounded-xl border border-amber-200 space-y-2">
                <div className="flex items-center space-x-2">
                  <ShieldCheck className="w-4 h-4 text-amber-600" />
                  <span className="text-xs font-bold text-amber-900">
                    {t('Section E — Applicant Declaration', 'सेक्शन E — आवेदक घोषणा')}
                  </span>
                </div>
                <p className="text-[11px] text-amber-800 italic leading-snug">
                  “I confirm that I have reviewed the information in this fictional demonstration form. I understand that any discrepancies must be checked against the original documents.”
                </p>
                <div className="pt-2 flex items-center justify-between">
                  <label className="flex items-center space-x-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={applicationForm.declaration_accepted}
                      onChange={(e) => updateFormField('declaration_accepted', e.target.checked)}
                      className="w-4 h-4 rounded text-blue-600 focus:ring-blue-500"
                    />
                    <span className="text-xs font-semibold text-slate-800">
                      {t('I explicitly review and accept declaration', 'मैं घोषणा की समीक्षा कर इसे स्वीकार करता हूँ')}
                    </span>
                  </label>
                </div>
                <span className="text-[10px] text-slate-500 block">
                  {t(
                    'FormSathiAI never auto-signs declarations. Explicit applicant consent is required.',
                    'FormSathiAI घोषणा पर कभी स्वचालित हस्ताक्षर नहीं करता। आवेदक की स्पष्ट सहमति अनिवार्य है।'
                  )}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* RIGHT PANEL: Explanations, Q&A, Checklist, Validation (Col 7) */}
        <div className="lg:col-span-7 space-y-5">
          {/* Sub-tabs header */}
          <div className="flex bg-white p-1.5 rounded-2xl border border-slate-200 shadow-xs space-x-1 overflow-x-auto">
            <button
              onClick={() => setActiveRightTab('validation')}
              className={`flex-1 py-2 px-3 rounded-xl text-xs font-bold transition-all whitespace-nowrap cursor-pointer ${
                activeRightTab === 'validation'
                  ? 'bg-blue-600 text-white shadow-xs'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
              }`}
            >
              {t('Validation Results', 'सत्यापन परिणाम')}
            </button>
            <button
              onClick={() => setActiveRightTab('checklist')}
              className={`flex-1 py-2 px-3 rounded-xl text-xs font-bold transition-all whitespace-nowrap cursor-pointer ${
                activeRightTab === 'checklist'
                  ? 'bg-blue-600 text-white shadow-xs'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
              }`}
            >
              {t('Checklist', 'चेकलिस्ट')} ({checklist?.completed_items}/{checklist?.total_items})
            </button>
            <button
              onClick={() => setActiveRightTab('ask')}
              className={`flex-1 py-2 px-3 rounded-xl text-xs font-bold transition-all whitespace-nowrap cursor-pointer ${
                activeRightTab === 'ask'
                  ? 'bg-blue-600 text-white shadow-xs'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
              }`}
            >
              {t('Ask FormSathiAI', 'सवाल पूछें')}
            </button>
            <button
              onClick={() => setActiveRightTab('explanations')}
              className={`flex-1 py-2 px-3 rounded-xl text-xs font-bold transition-all whitespace-nowrap cursor-pointer ${
                activeRightTab === 'explanations'
                  ? 'bg-blue-600 text-white shadow-xs'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
              }`}
            >
              {t('Field Explanations', 'फ़ील्ड स्पष्टीकरण')}
            </button>
          </div>

          {/* Active Tab View */}
          {activeRightTab === 'validation' && <ValidationAlerts />}
          {activeRightTab === 'checklist' && <ChecklistView />}
          {activeRightTab === 'ask' && <AskFormSathi />}
          {activeRightTab === 'explanations' && <FieldExplainer />}
        </div>
      </div>
    </div>
  );
};
