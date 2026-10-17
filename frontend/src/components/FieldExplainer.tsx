import React, { useState } from 'react';
import { HelpCircle, BookOpen, ExternalLink, Sparkles, ChevronRight } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { useApp } from '../context/AppContext';
import { FieldExplanation } from '../types';

export const FieldExplainer: React.FC = () => {
  const { t, language } = useLanguage();
  const { fieldExplanations } = useApp();
  const [selectedKey, setSelectedKey] = useState<string>('annual_family_income');

  const keys = Object.keys(fieldExplanations);
  const activeExpl = fieldExplanations[selectedKey];

  return (
    <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-xs">
      <div className="flex items-center space-x-2.5 pb-4 border-b border-slate-100">
        <div className="p-2 bg-emerald-100 text-emerald-700 rounded-lg">
          <BookOpen className="w-5 h-5" />
        </div>
        <div>
          <h3 className="text-base font-bold text-slate-900">
            {t('Plain-Language Field Explanations', 'सरल भाषा में फ़ील्ड स्पष्टीकरण')}
          </h3>
          <p className="text-xs text-slate-500">
            {t(
              'Simple English and Hindi explanations grounded in official instructions.',
              'आधिकारिक निर्देशों पर आधारित सरल अंग्रेजी और हिन्दी स्पष्टीकरण।'
            )}
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
        {/* Field List */}
        <div className="space-y-1 md:border-r md:border-slate-100 md:pr-3 max-h-80 overflow-y-auto">
          {keys.map((k) => {
            const item = fieldExplanations[k];
            const isSelected = selectedKey === k;
            return (
              <button
                key={k}
                onClick={() => setSelectedKey(k)}
                className={`w-full flex items-center justify-between p-2.5 rounded-xl text-left text-xs font-medium transition-colors cursor-pointer ${
                  isSelected
                    ? 'bg-blue-50 text-blue-800 font-semibold border border-blue-200 shadow-2xs'
                    : 'text-slate-700 hover:bg-slate-50 border border-transparent'
                }`}
              >
                <span>{language === 'hi' ? item.label_hi : item.label_en}</span>
                <ChevronRight className={`w-3.5 h-3.5 ${isSelected ? 'text-blue-600' : 'text-slate-400'}`} />
              </button>
            );
          })}
        </div>

        {/* Selected Field Explanation Detail */}
        {activeExpl && (
          <div className="md:col-span-2 bg-slate-50 rounded-xl p-4 border border-slate-200 flex flex-col justify-between">
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold uppercase tracking-wider text-blue-600">
                  {t('Form Field', 'फॉर्म फ़ील्ड')}
                </span>
                <span className="text-[11px] bg-blue-100 text-blue-800 font-semibold px-2 py-0.5 rounded-full">
                  {activeExpl.required_in_instructions ? t('Mandatory', 'अनिवार्य') : t('Optional', 'वैकल्पिक')}
                </span>
              </div>

              <h4 className="text-base font-bold text-slate-900">
                {language === 'hi' ? activeExpl.label_hi : activeExpl.label_en}
              </h4>

              {/* Bilingual Cards */}
              <div className="space-y-2">
                <div className="p-3 bg-white rounded-lg border border-slate-200 text-xs">
                  <span className="text-[10px] font-bold text-slate-400 block mb-1">ENGLISH EXPLANATION</span>
                  <p className="text-slate-700 leading-relaxed">{activeExpl.explanation_en}</p>
                </div>
                <div className="p-3 bg-white rounded-lg border border-slate-200 text-xs">
                  <span className="text-[10px] font-bold text-slate-400 block mb-1">हिन्दी स्पष्टीकरण</span>
                  <p className="text-slate-700 leading-relaxed font-sans">{activeExpl.explanation_hi}</p>
                </div>
              </div>
            </div>

            {/* Source Reference Citation */}
            {activeExpl.source_reference && (
              <div className="mt-4 pt-3 border-t border-slate-200 text-[11px] text-slate-500 flex items-center space-x-1.5">
                <ExternalLink className="w-3.5 h-3.5 text-blue-500 flex-shrink-0" />
                <span>
                  <strong>{t('Source:', 'स्रोत:')}</strong> {activeExpl.source_reference}
                </span>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
