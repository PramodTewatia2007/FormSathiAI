import React from 'react';
import {
  CheckSquare,
  CheckCircle2,
  XCircle,
  AlertTriangle,
  FileText,
  FileCheck2,
  HelpCircle
} from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { useApp } from '../context/AppContext';

export const ChecklistView: React.FC = () => {
  const { t, language } = useLanguage();
  const { checklist, applicationForm, updateFormField } = useApp();

  if (!checklist) return null;

  const pct = Math.round((checklist.completed_items / checklist.total_items) * 100);

  const toggleAttachment = (key: string) => {
    if (!applicationForm) return;
    if (key === 'income_cert') {
      updateFormField('income_cert_attached', !applicationForm.income_cert_attached);
    } else if (key === 'passbook') {
      updateFormField('passbook_attached', !applicationForm.passbook_attached);
    } else if (key === 'marksheet') {
      updateFormField('marksheet_attached', !applicationForm.marksheet_attached);
    } else if (key === 'identity_proof') {
      updateFormField('identity_proof_attached', !applicationForm.identity_proof_attached);
    } else if (key === 'institution_cert') {
      updateFormField('institution_cert_attached', !applicationForm.institution_cert_attached);
    } else if (key === 'declaration') {
      updateFormField('declaration_accepted', !applicationForm.declaration_accepted);
    }
  };

  return (
    <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-xs">
      {/* Header & Progress */}
      <div className="pb-4 border-b border-slate-100">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2.5">
            <div className="p-2 bg-blue-100 text-blue-700 rounded-lg">
              <CheckSquare className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base font-bold text-slate-900">
                {t('Required Document Checklist', 'आवश्यक दस्तावेज चेकलिस्ट')}
              </h3>
              <p className="text-xs text-slate-500">
                {t('Dynamic tracking of required attachments & declarations', 'आवश्यक संलग्नकों और घोषणाओं की गतिशील ट्रैकिंग')}
              </p>
            </div>
          </div>
          <span
            className={`px-3 py-1 text-xs font-bold rounded-full ${
              checklist.overall_status === 'Complete'
                ? 'bg-emerald-100 text-emerald-800'
                : 'bg-amber-100 text-amber-800'
            }`}
          >
            {checklist.overall_status === 'Complete'
              ? t('Complete', 'पूर्ण')
              : t('Incomplete', 'अपूर्ण')}
          </span>
        </div>

        {/* Progress Bar */}
        <div className="mt-4">
          <div className="flex items-center justify-between text-xs font-medium text-slate-600 mb-1.5">
            <span>
              {t('Progress:', 'प्रगति:')}{' '}
              <strong className="text-slate-900">
                {checklist.completed_items} of {checklist.total_items} items completed
              </strong>
            </span>
            <span className="font-bold text-blue-600">{pct}%</span>
          </div>
          <div className="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden">
            <div
              className={`h-2.5 rounded-full transition-all duration-300 ${
                pct === 100 ? 'bg-emerald-500' : 'bg-blue-600'
              }`}
              style={{ width: `${pct}%` }}
            />
          </div>
          <div className="flex justify-between text-[11px] text-slate-500 mt-1">
            <span>{checklist.remaining_items} {t('remaining items to complete', 'मदें पूरी करना बाकी')}</span>
          </div>
        </div>
      </div>

      {/* Checklist items list */}
      <div className="divide-y divide-slate-100 mt-2">
        {checklist.items.map((item) => {
          const isDone = item.status === 'completed';
          return (
            <div
              key={item.key}
              className="py-3 flex items-start justify-between gap-3 hover:bg-slate-50/60 rounded-xl px-2 transition-colors"
            >
              <div className="flex items-start space-x-3">
                <button
                  type="button"
                  onClick={() => toggleAttachment(item.key)}
                  title={t('Click to toggle attachment state', 'संलग्नक स्थिति बदलने के लिए क्लिक करें')}
                  className="mt-0.5 flex-shrink-0 cursor-pointer focus:outline-hidden"
                >
                  {isDone ? (
                    <CheckCircle2 className="w-5 h-5 text-emerald-600 hover:text-emerald-700" />
                  ) : (
                    <XCircle className="w-5 h-5 text-slate-300 hover:text-slate-400" />
                  )}
                </button>
                <div>
                  <div className="flex items-center space-x-2">
                    <span
                      className={`text-xs font-bold ${
                        isDone ? 'text-slate-800' : 'text-slate-600'
                      }`}
                    >
                      {language === 'hi' ? item.title_hi : item.title_en}
                    </span>
                    {item.is_placeholder && (
                      <span className="text-[10px] font-semibold bg-blue-50 text-blue-700 border border-blue-200 px-1.5 py-0.2 rounded-sm">
                        {t('Fictional Placeholder', 'काल्पनिक प्लेसहोल्डर')}
                      </span>
                    )}
                  </div>
                  <p className="text-[11px] text-slate-500 mt-0.5">
                    {language === 'hi' ? item.details_hi : item.details_en}
                  </p>
                </div>
              </div>

              {/* Action pill */}
              <button
                type="button"
                onClick={() => toggleAttachment(item.key)}
                className={`text-[11px] font-semibold px-2.5 py-1 rounded-lg border transition-colors cursor-pointer flex-shrink-0 ${
                  isDone
                    ? 'bg-slate-100 text-slate-700 border-slate-200 hover:bg-slate-200'
                    : 'bg-blue-50 text-blue-700 border-blue-200 hover:bg-blue-100'
                }`}
              >
                {isDone ? t('Detach', 'हटाएँ') : t('Attach Sample', 'संलग्न करें')}
              </button>
            </div>
          );
        })}
      </div>
    </div>
  );
};
