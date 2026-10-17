import React from 'react';
import { ShieldCheck, Lock, AlertCircle, X } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { useApp } from '../context/AppContext';

export const ConsentModal: React.FC = () => {
  const { t } = useLanguage();
  const { showConsentModal, setShowConsentModal, giveConsent } = useApp();

  if (!showConsentModal) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl max-w-lg w-full p-6 shadow-2xl border border-slate-200 animate-in fade-in zoom-in-95 duration-150">
        <div className="flex items-start justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-2.5 bg-blue-100 rounded-xl text-blue-700">
              <ShieldCheck className="w-6 h-6" />
            </div>
            <div>
              <h3 className="text-lg font-bold text-slate-900">
                {t('Data Privacy & Processing Consent', 'डेटा गोपनीयता एवं प्रसंस्करण सहमति')}
              </h3>
              <p className="text-xs text-slate-500">
                {t('FormSathiAI Document Security Protocol', 'FormSathiAI दस्तावेज सुरक्षा प्रोटोकॉल')}
              </p>
            </div>
          </div>
          <button
            onClick={() => setShowConsentModal(false)}
            className="text-slate-400 hover:text-slate-600 p-1 rounded-lg"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="mt-4 space-y-3 text-sm text-slate-600">
          <div className="p-3 bg-blue-50 border border-blue-200 rounded-xl text-xs text-blue-900 flex items-start space-x-2">
            <Lock className="w-4 h-4 text-blue-700 flex-shrink-0 mt-0.5" />
            <span>
              {t(
                'Before processing documents containing personal, academic, or financial records, FormSathiAI requires your explicit consent.',
                'व्यक्तिगत, शैक्षणिक या वित्तीय रिकॉर्ड वाले दस्तावेजों को संसाधित करने से पहले, FormSathiAI को आपकी स्पष्ट सहमति की आवश्यकता होती है।'
              )}
            </span>
          </div>

          <p className="text-xs text-slate-600">
            {t(
              'Withdrawing consent clears uploaded documents and user-entered session data.',
              'सहमति वापस लेने पर अपलोड किए गए दस्तावेज़ और सत्र में दर्ज उपयोगकर्ता डेटा साफ़ हो जाएगा।'
            )}
          </p>

          <div className="space-y-2 text-xs">
            <p className="font-semibold text-slate-800">
              {t('What will be extracted and why:', 'क्या निकाला जाएगा और क्यों:')}
            </p>
            <ul className="list-disc pl-5 space-y-1 text-slate-600">
              <li>
                <strong>{t('Applicant Name & Date of Birth:', 'आवेदक का नाम व जन्म तिथि:')}</strong>{' '}
                {t('Cross-checked against the scholarship application for identity consistency.', 'पहचान की सत्यता के लिए छात्रवृत्ति आवेदन से मिलान किया जाता है।')}
              </li>
              <li>
                <strong>{t('Exam Marks & Percentages:', 'परीक्षा के अंक व प्रतिशत:')}</strong>{' '}
                {t('Verified against the qualifying criteria (minimum 60%).', 'न्यूनतम पात्रता मानदंड (60%) के विरुद्ध मिलान किया जाता है।')}
              </li>
              <li>
                <strong>{t('Annual Family Income:', 'वार्षिक पारिवारिक आय:')}</strong>{' '}
                {t('Checked against the scholarship income ceiling (₹2,50,000).', 'छात्रवृत्ति की आय सीमा (₹2,50,000) के विरुद्ध जाँचा जाता है।')}
              </li>
            </ul>
          </div>

          <div className="p-3 bg-amber-50 border border-amber-200 rounded-xl text-xs text-amber-900 flex items-start space-x-2">
            <AlertCircle className="w-4 h-4 text-amber-700 flex-shrink-0 mt-0.5" />
            <span>
              {t(
                'Safeguards: Documents are stored only temporarily in an isolated session directory. No sensitive document text is logged or shared with external parties. You can delete documents or reset your session at any time.',
                'सुरक्षा: दस्तावेज केवल एक अलग अस्थायी सत्र में संग्रहीत होते हैं। किसी भी संवेदनशील सामग्री को बाहरी पक्षों के साथ साझा नहीं किया जाता है। आप किसी भी समय दस्तावेज हटा सकते हैं या सत्र रीसेट कर सकते हैं।'
              )}
            </span>
          </div>
        </div>

        <div className="mt-6 flex items-center justify-end space-x-3">
          <button
            type="button"
            onClick={() => giveConsent(false)}
            className="px-4 py-2 text-xs font-semibold text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-xl transition-colors"
          >
            {t('Decline', 'अस्वीकार करें')}
          </button>
          <button
            type="button"
            onClick={() => giveConsent(true)}
            className="px-5 py-2 text-xs font-semibold text-white bg-blue-600 hover:bg-blue-700 rounded-xl shadow-md transition-colors"
          >
            {t('I Consent & Allow Processing', 'मैं सहमत हूँ और प्रसंस्करण की अनुमति देता हूँ')}
          </button>
        </div>
      </div>
    </div>
  );
};
