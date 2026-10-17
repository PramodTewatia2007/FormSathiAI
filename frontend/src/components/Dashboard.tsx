import React from 'react';
import {
  FileText,
  Layers,
  CheckSquare,
  AlertTriangle,
  Upload,
  MessageSquare,
  ArrowRight,
  ShieldCheck,
  Sparkles,
  HelpCircle,
  FileCheck2,
  Clock,
  BookOpen
} from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { useApp } from '../context/AppContext';

export const Dashboard: React.FC = () => {
  const { t, language } = useLanguage();
  const { setActiveTab, checklist, validation, documents, selectScenario } = useApp();

  const missingAlerts = validation?.alerts.filter((a) => a.category === 'missing') || [];
  const inconsistencyAlerts = validation?.alerts.filter((a) => a.category === 'inconsistency') || [];

  return (
    <div className="space-y-6">
      {/* Hero Welcome Banner */}
      <div className="bg-gradient-to-r from-blue-700 via-blue-800 to-indigo-900 rounded-3xl p-6 sm:p-8 text-white shadow-xl relative overflow-hidden">
        <div className="absolute right-0 top-0 bottom-0 w-1/3 opacity-10 pointer-events-none flex items-center justify-center">
          <FileText className="w-96 h-96 transform translate-x-16 -translate-y-12" />
        </div>

        <div className="max-w-2xl relative z-10 space-y-4">
          <div className="inline-flex items-center space-x-2 bg-blue-600/40 backdrop-blur-md px-3 py-1 rounded-full text-xs font-semibold text-blue-100 border border-blue-400/30">
            <Sparkles className="w-3.5 h-3.5 text-blue-200" />
            <span>{t('AI-Powered Form Assistant', 'AI-संचालित फॉर्म सहायक')}</span>
          </div>

          <h1 className="text-2xl sm:text-4xl font-extrabold tracking-tight leading-tight">
            FormSathiAI
          </h1>

          <p className="text-lg sm:text-xl font-medium text-blue-100">
            “{t('Make complicated forms easier to understand.', 'जटिल फॉर्मों को समझना आसान बनाएं।')}”
          </p>

          <p className="text-xs sm:text-sm text-blue-200/90 leading-relaxed">
            {t(
              'Assisting students, families, and community service centres to understand scholarship applications, college admissions, and paperwork through simple English and Hindi explanations.',
              'छात्रवृत्ति, कॉलेज प्रवेश और सरकारी फॉर्मों को समझने में विद्यार्थियों, परिवारों और जनसेवा केंद्रों की सरल हिन्दी और अंग्रेजी में सहायता।'
            )}
          </p>

          <div className="pt-2 flex flex-wrap gap-3">
            <button
              onClick={() => {
                selectScenario('scenario_1');
                setActiveTab('workspace');
              }}
              className="flex items-center space-x-2 bg-white text-blue-800 hover:bg-blue-50 px-5 py-3 rounded-2xl font-bold text-sm shadow-lg hover:shadow-xl transition-all cursor-pointer"
            >
              <Layers className="w-4 h-4" />
              <span>{t('Try Demo Workspace', 'डेमो वर्कस्पेस आज़माएँ')}</span>
              <ArrowRight className="w-4 h-4" />
            </button>

            <button
              onClick={() => setActiveTab('upload')}
              className="flex items-center space-x-2 bg-blue-600/60 hover:bg-blue-600 text-white border border-blue-400/40 px-5 py-3 rounded-2xl font-bold text-sm transition-all cursor-pointer"
            >
              <Upload className="w-4 h-4" />
              <span>{t('Upload Documents', 'दस्तावेज अपलोड करें')}</span>
            </button>
          </div>
        </div>
      </div>

      {/* Overview Status Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Checklist Progress */}
        <div
          onClick={() => setActiveTab('checklist')}
          className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs hover:border-blue-300 hover:shadow-md transition-all cursor-pointer"
        >
          <div className="flex items-center justify-between">
            <div className="p-2.5 bg-blue-100 text-blue-700 rounded-xl">
              <CheckSquare className="w-5 h-5" />
            </div>
            <span className="text-xs font-bold text-blue-600">
              {checklist?.overall_status === 'Complete' ? t('Complete', 'पूर्ण') : t('Incomplete', 'अपूर्ण')}
            </span>
          </div>
          <div className="mt-3">
            <h4 className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
              {t('Checklist Progress', 'चेकलिस्ट प्रगति')}
            </h4>
            <div className="text-2xl font-extrabold text-slate-900 mt-1">
              {checklist ? `${checklist.completed_items}/${checklist.total_items}` : '0/6'}
            </div>
            <p className="text-[11px] text-slate-500 mt-0.5">
              {checklist?.remaining_items || 0} {t('remaining items required', 'आवश्यक मदें शेष')}
            </p>
          </div>
        </div>

        {/* Missing-Document Alerts */}
        <div
          onClick={() => setActiveTab('workspace')}
          className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs hover:border-amber-300 hover:shadow-md transition-all cursor-pointer"
        >
          <div className="flex items-center justify-between">
            <div className="p-2.5 bg-amber-100 text-amber-700 rounded-xl">
              <FileText className="w-5 h-5" />
            </div>
            <span className="text-xs font-bold text-amber-600">
              {missingAlerts.length} {t('Alerts', 'चेतावनी')}
            </span>
          </div>
          <div className="mt-3">
            <h4 className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
              {t('Missing Information', 'अधूरी जानकारी')}
            </h4>
            <div className="text-2xl font-extrabold text-slate-900 mt-1">
              {missingAlerts.length}
            </div>
            <p className="text-[11px] text-slate-500 mt-0.5">
              {t('Passbook, income cert & declaration', 'पासबुक, आय प्रमाण व घोषणा')}
            </p>
          </div>
        </div>

        {/* Inconsistency Warnings */}
        <div
          onClick={() => setActiveTab('workspace')}
          className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs hover:border-rose-300 hover:shadow-md transition-all cursor-pointer"
        >
          <div className="flex items-center justify-between">
            <div className="p-2.5 bg-rose-100 text-rose-700 rounded-xl">
              <AlertTriangle className="w-5 h-5" />
            </div>
            <span className="text-xs font-bold text-rose-600">
              {inconsistencyAlerts.length} {t('Active', 'सक्रिय')}
            </span>
          </div>
          <div className="mt-3">
            <h4 className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
              {t('Inconsistencies', 'विसंगति चेतावनियां')}
            </h4>
            <div className="text-2xl font-extrabold text-slate-900 mt-1">
              {inconsistencyAlerts.length}
            </div>
            <p className="text-[11px] text-slate-500 mt-0.5">
              {inconsistencyAlerts.length > 0
                ? t('Discrepancies flagged for review', 'समीक्षा के लिए चिन्हित विसंगतियां')
                : t('No value conflicts detected', 'कोई विसंगति नहीं मिली')}
            </p>
          </div>
        </div>

        {/* Processed Documents */}
        <div
          onClick={() => setActiveTab('upload')}
          className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs hover:border-purple-300 hover:shadow-md transition-all cursor-pointer"
        >
          <div className="flex items-center justify-between">
            <div className="p-2.5 bg-purple-100 text-purple-700 rounded-xl">
              <FileCheck2 className="w-5 h-5" />
            </div>
            <span className="text-xs font-bold text-purple-600">
              {documents.length} {t('Files', 'फ़ाइलें')}
            </span>
          </div>
          <div className="mt-3">
            <h4 className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
              {t('Documents Stored', 'संसाधित दस्तावेज')}
            </h4>
            <div className="text-2xl font-extrabold text-slate-900 mt-1">
              {documents.length}
            </div>
            <p className="text-[11px] text-slate-500 mt-0.5">
              {t('Isolated session temporary storage', 'पृथक अस्थायी सत्र भंडारण')}
            </p>
          </div>
        </div>
      </div>

      {/* Interactive Scenario Cards */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-xs">
        <div className="flex items-center justify-between pb-4 border-b border-slate-100">
          <div>
            <h3 className="text-base font-bold text-slate-900">
              {t('Explore 4 Demo Test Scenarios', '4 डेमो परीक्षण परिदृश्य देखें')}
            </h3>
            <p className="text-xs text-slate-500">
              {t('Preconfigured application states to observe how FormSathiAI explains requirements.', 'फॉर्मसाथीएआई आवश्यकताओं की व्याख्या कैसे करता है, यह देखने के लिए पूर्व-कॉन्फ़िगर परिदृश्य।')}
            </p>
          </div>
          <button
            onClick={() => setActiveTab('workspace')}
            className="text-xs font-bold text-blue-600 hover:text-blue-800 flex items-center space-x-1"
          >
            <span>{t('Go to Workspace', 'वर्कस्पेस पर जाएँ')}</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mt-4">
          <div
            onClick={() => { selectScenario('scenario_1'); setActiveTab('workspace'); }}
            className="p-4 rounded-xl border border-slate-200 bg-slate-50 hover:bg-blue-50/50 hover:border-blue-300 transition-all cursor-pointer space-y-2"
          >
            <div className="text-xs font-bold text-slate-900">
              {t('Scenario 1 — Eligible Sample', 'परिदृश्य 1 — पात्र नमूना')}
            </div>
            <p className="text-[11px] text-slate-600 leading-relaxed">
              {t('Default student with 78% marks and ₹1,80,000 income. Meets academic/income rules, but lacks 3 attachments.', '78% अंक और ₹1,80,000 आय वाला डिफ़ॉल्ट विद्यार्थी। मानदंड पूरे, पर 3 दस्तावेज बाकी।')}
            </p>
            <span className="inline-block text-[10px] font-bold text-blue-600 uppercase">
              {t('Load Scenario →', 'लोड करें →')}
            </span>
          </div>

          <div
            onClick={() => { selectScenario('scenario_2'); setActiveTab('workspace'); }}
            className="p-4 rounded-xl border border-slate-200 bg-slate-50 hover:bg-amber-50/50 hover:border-amber-300 transition-all cursor-pointer space-y-2"
          >
            <div className="text-xs font-bold text-slate-900">
              {t('Scenario 2 — Missing Info', 'परिदृश्य 2 — अधूरी जानकारी')}
            </div>
            <p className="text-[11px] text-slate-600 leading-relaxed">
              {t('Student name is left blank, institution cert removed. System guides how to resolve incomplete fields.', 'विद्यार्थी का नाम खाली है, संस्थान प्रमाणपत्र नहीं है। सिस्टम अधूरे फ़ील्ड पूरा करने का मार्गदर्शन करता है।')}
            </p>
            <span className="inline-block text-[10px] font-bold text-amber-600 uppercase">
              {t('Load Scenario →', 'लोड करें →')}
            </span>
          </div>

          <div
            onClick={() => { selectScenario('scenario_3'); setActiveTab('workspace'); }}
            className="p-4 rounded-xl border border-slate-200 bg-slate-50 hover:bg-rose-50/50 hover:border-rose-300 transition-all cursor-pointer space-y-2"
          >
            <div className="text-xs font-bold text-slate-900">
              {t('Scenario 3 — Inconsistent Marks', 'परिदृश्य 3 — अंकों में विसंगति')}
            </div>
            <p className="text-[11px] text-slate-600 leading-relaxed">
              {t('Application states 78%, while attached marksheet says 58%. System warns and avoids auto-choosing.', 'आवेदन में 78% और संलग्न अंकपत्र में 58% है। सिस्टम विसंगति चेतावनी देता है और स्वतः चयन से बचता है।')}
            </p>
            <span className="inline-block text-[10px] font-bold text-rose-600 uppercase">
              {t('Load Scenario →', 'लोड करें →')}
            </span>
          </div>

          <div
            onClick={() => { selectScenario('scenario_4'); setActiveTab('workspace'); }}
            className="p-4 rounded-xl border border-slate-200 bg-slate-50 hover:bg-purple-50/50 hover:border-purple-300 transition-all cursor-pointer space-y-2"
          >
            <div className="text-xs font-bold text-slate-900">
              {t('Scenario 4 — Income Limit Exceeded', 'परिदृश्य 4 — आय सीमा से अधिक')}
            </div>
            <p className="text-[11px] text-slate-600 leading-relaxed">
              {t('Declared income ₹2,80,000 exceeds ₹2,50,000 ceiling. System explains specific income ineligibility.', 'घोषित आय ₹2,80,000 सीमा ₹2,50,000 से अधिक है। सिस्टम आय अपात्रता की स्पष्ट व्याख्या करता है।')}
            </p>
            <span className="inline-block text-[10px] font-bold text-purple-600 uppercase">
              {t('Load Scenario →', 'लोड करें →')}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};
