import React from 'react';
import {
  ShieldAlert,
  CheckCircle2,
  AlertTriangle,
  FileQuestion,
  HelpCircle,
  Info
} from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { useApp } from '../context/AppContext';
import { ValidationAlert } from '../types';

export const ValidationAlerts: React.FC = () => {
  const { t, language } = useLanguage();
  const { validation } = useApp();

  if (!validation) return null;

  const getAlertBadge = (category: ValidationAlert['category']) => {
    switch (category) {
      case 'confirmed':
        return {
          bg: 'bg-emerald-50 border-emerald-200 text-emerald-900',
          icon: <CheckCircle2 className="w-4 h-4 text-emerald-600 flex-shrink-0 mt-0.5" />,
          label_en: 'Confirmed Requirement',
          label_hi: 'पुष्ट आवश्यकता'
        };
      case 'inconsistency':
        return {
          bg: 'bg-rose-50 border-rose-200 text-rose-900',
          icon: <AlertTriangle className="w-4 h-4 text-rose-600 flex-shrink-0 mt-0.5" />,
          label_en: 'Potential Inconsistency',
          label_hi: 'संभावित विसंगति'
        };
      case 'missing':
        return {
          bg: 'bg-amber-50/70 border-amber-200 text-amber-900',
          icon: <Info className="w-4 h-4 text-amber-600 flex-shrink-0 mt-0.5" />,
          label_en: 'Missing Information',
          label_hi: 'अधूरी जानकारी'
        };
      case 'unverified':
        return {
          bg: 'bg-blue-50/70 border-blue-200 text-blue-900',
          icon: <FileQuestion className="w-4 h-4 text-blue-600 flex-shrink-0 mt-0.5" />,
          label_en: 'Unverified Document',
          label_hi: 'अपुष्ट दस्तावेज'
        };
      case 'unavailable':
      default:
        return {
          bg: 'bg-slate-50 border-slate-200 text-slate-800',
          icon: <HelpCircle className="w-4 h-4 text-slate-500 flex-shrink-0 mt-0.5" />,
          label_en: 'Information Unavailable',
          label_hi: 'जानकारी अनुपलब्ध'
        };
    }
  };

  return (
    <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-xs">
      {/* Header */}
      <div className="flex items-center space-x-2.5 pb-4 border-b border-slate-100">
        <div className="p-2 bg-purple-100 text-purple-700 rounded-lg">
          <ShieldAlert className="w-5 h-5" />
        </div>
        <div>
          <h3 className="text-base font-bold text-slate-900">
            {t('Validation & Discrepancy Findings', 'सत्यापन एवं विसंगति परिणाम')}
          </h3>
          <p className="text-xs text-slate-500">
            {t(
              'Continuous cross-verification against rules and attached documents.',
              'नियमों और संलग्न दस्तावेजों के साथ निरंतर मिलान व सत्यापन।'
            )}
          </p>
        </div>
      </div>

      {/* Summary Banner */}
      <div className="mt-4 p-3 bg-slate-50 rounded-xl border border-slate-200 text-xs text-slate-700">
        <strong>{t('Summary: ', 'सारांश: ')}</strong>
        <span>
          {language === 'hi'
            ? validation.eligibility_summary_hi
            : validation.eligibility_summary_en}
        </span>
      </div>

      {/* Categorized Alerts */}
      <div className="space-y-3 mt-4">
        {validation.alerts.map((alert, idx) => {
          const config = getAlertBadge(alert.category);
          return (
            <div
              key={idx}
              className={`p-3.5 rounded-xl border flex items-start space-x-3 text-xs ${config.bg}`}
            >
              {config.icon}
              <div className="flex-1 space-y-1">
                <div className="flex items-center justify-between">
                  <span className="font-bold tracking-tight">
                    {t(config.label_en, config.label_hi)}
                  </span>
                  <span className="font-mono text-[10px] opacity-75 uppercase">
                    {alert.field_name}
                  </span>
                </div>
                <p className="leading-relaxed">
                  {language === 'hi' ? alert.message_hi : alert.message_en}
                </p>
                <div className="pt-1 text-[11px] opacity-85">
                  <strong>{t('Suggested Resolution: ', 'सुझाया गया समाधान: ')}</strong>
                  <span>
                    {language === 'hi' ? alert.resolution_hint_hi : alert.resolution_hint_en}
                  </span>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
