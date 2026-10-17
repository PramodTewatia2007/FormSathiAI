import React from 'react';
import {
  ShieldCheck,
  Lock,
  Trash2,
  AlertCircle,
  HelpCircle,
  FileCheck2,
  FileWarning,
  RotateCcw
} from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { useApp } from '../context/AppContext';

export const PrivacyHelp: React.FC = () => {
  const { t } = useLanguage();
  const { consentGiven, setShowConsentModal, resetSession } = useApp();

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      {/* Privacy Guarantee Header */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-xs">
        <div className="flex items-center space-x-3 pb-4 border-b border-slate-100">
          <div className="p-2.5 bg-blue-100 text-blue-700 rounded-xl">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-slate-900">
              {t('Privacy, Security & System Limits', 'गोपनीयता, सुरक्षा एवं प्रणाली सीमाएं')}
            </h3>
            <p className="text-xs text-slate-500">
              {t('Guiding principles for ethical and secure form assistance', 'नैतिक और सुरक्षित फॉर्म सहायता के मार्गदर्शक सिद्धांत')}
            </p>
          </div>
        </div>

        {/* 5 Core Principles */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-5">
          <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-1.5">
            <div className="flex items-center space-x-2 text-blue-700 font-bold text-xs">
              <Lock className="w-4 h-4" />
              <span>{t('1. Explicit Consent & Data Minimization', '1. स्पष्ट सहमति एवं न्यूनतम डेटा संग्रहण')}</span>
            </div>
            <p className="text-xs text-slate-600 leading-relaxed">
              {t(
                'FormSathiAI never processes uploaded documents without prior consent. Only information strictly necessary for evaluating requirements (names, marks, income) is parsed.',
                'FormSathiAI पूर्व सहमति के बिना कभी दस्तावेजों को संसाधित नहीं करता। केवल आवश्यक जानकारी (नाम, अंक, आय) ही जाँची जाती है।'
              )}
            </p>
          </div>

          <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-1.5">
            <div className="flex items-center space-x-2 text-indigo-700 font-bold text-xs">
              <Trash2 className="w-4 h-4" />
              <span>{t('2. Isolated Temporary Storage & Cleanup', '2. पृथक अस्थायी भंडारण व पूर्ण विलोपन')}</span>
            </div>
            <p className="text-xs text-slate-600 leading-relaxed">
              {t(
                'Uploaded files reside strictly within session-scoped temporary storage. Resetting the session or clicking delete removes files permanently from disk.',
                'अपलोड की गई फाइलें केवल सत्र-आधारित अस्थायी स्थान में रहती हैं। रीसेट करने पर सभी फाइलें डिस्क से स्थायी रूप से हटा दी जाती हैं।'
              )}
            </p>
          </div>

          <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-1.5">
            <div className="flex items-center space-x-2 text-amber-700 font-bold text-xs">
              <FileWarning className="w-4 h-4" />
              <span>{t('3. Never Auto-Submits or Signs', '3. कभी स्वचालित सबमिट या हस्ताक्षर नहीं')}</span>
            </div>
            <p className="text-xs text-slate-600 leading-relaxed">
              {t(
                'FormSathiAI does not automatically submit forms, mark declarations accepted, or sign documents. Explicit applicant action and review is always mandatory.',
                'FormSathiAI कभी फॉर्म स्वतः सबमिट नहीं करता और न ही घोषणा स्वीकार करता है। आवेदक की प्रत्यक्ष समीक्षा सदैव अनिवार्य है।'
              )}
            </p>
          </div>

          <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-1.5">
            <div className="flex items-center space-x-2 text-emerald-700 font-bold text-xs">
              <FileCheck2 className="w-4 h-4" />
              <span>{t('4. Unverified Placeholders vs Official Evidence', '4. अपुष्ट नमूने बनाम आधिकारिक प्रमाण')}</span>
            </div>
            <p className="text-xs text-slate-600 leading-relaxed">
              {t(
                'Uploaded sample placeholders are explicitly tagged as Unverified. The system never claims that an official government or college authority has verified them.',
                'अपलोड किए गए नमूनों को स्पष्ट रूप से अपुष्ट चिह्नित किया जाता है। सिस्टम कभी आधिकारिक सत्यापन का दावा नहीं करता।'
              )}
            </p>
          </div>
        </div>

        {/* Action Controls */}
        <div className="mt-6 pt-4 border-t border-slate-100 flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center space-x-2">
            <span className="text-xs text-slate-600">
              {t('Processing Consent Status:', 'प्रसंस्करण सहमति स्थिति:')}
            </span>
            <span
              className={`text-xs font-bold px-2.5 py-0.5 rounded-full ${
                consentGiven
                  ? 'bg-emerald-100 text-emerald-800'
                  : 'bg-slate-100 text-slate-700'
              }`}
            >
              {consentGiven ? t('Consent Granted', 'सहमति स्वीकृत') : t('Consent Not Set', 'सहमति अनिर्धारित')}
            </span>
          </div>

          <div className="flex items-center space-x-2">
            <button
              onClick={() => setShowConsentModal(true)}
              className="text-xs font-semibold px-3 py-1.5 bg-blue-50 text-blue-700 hover:bg-blue-100 rounded-lg border border-blue-200 transition-colors"
            >
              {t('Manage Consent', 'सहमति प्रबंधित करें')}
            </button>
            <button
              onClick={resetSession}
              className="text-xs font-semibold px-3 py-1.5 bg-rose-50 text-rose-700 hover:bg-rose-100 rounded-lg border border-rose-200 transition-colors flex items-center space-x-1"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>{t('Clear All Session Data', 'सभी सत्र डेटा साफ़ करें')}</span>
            </button>
          </div>
        </div>
      </div>

      {/* Limits of This Demonstration */}
      <div className="bg-amber-50 rounded-2xl p-6 border border-amber-200 text-amber-950 space-y-3">
        <div className="flex items-center space-x-2">
          <AlertCircle className="w-5 h-5 text-amber-700 flex-shrink-0" />
          <h4 className="text-sm font-bold uppercase tracking-wider">
            {t('Limits of This Demonstration', 'इस प्रदर्शन की सीमाएं')}
          </h4>
        </div>
        <p className="text-xs leading-relaxed text-amber-900">
          {t(
            'The Udaan Student Support Scholarship 2026–27 is a completely fictional scenario created exclusively to demonstrate FormSathiAI capabilities. It is not an official scholarship notification and must not be used to make decisions about a real scholarship. For real applications, consult the relevant official educational authority.',
            'उड़ान छात्रवृत्ति 2026–27 पूरी तरह से एक काल्पनिक उदाहरण है जिसे विशेष रूप से FormSathiAI की क्षमताओं को प्रदर्शित करने के लिए बनाया गया है। यह कोई आधिकारिक अधिसूचना नहीं है और इसका उपयोग वास्तविक निर्णय लेने के लिए न करें। वास्तविक आवेदनों के लिए संबंधित आधिकारिक संस्था से परामर्श करें।'
          )}
        </p>
      </div>
    </div>
  );
};
