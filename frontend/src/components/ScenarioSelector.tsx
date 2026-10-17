import React from 'react';
import { Layers, RotateCcw, AlertCircle, CheckCircle2 } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { useApp } from '../context/AppContext';

export const ScenarioSelector: React.FC = () => {
  const { t } = useLanguage();
  const { scenarios, activeScenarioId, selectScenario, resetSession, isLoading } = useApp();

  return (
    <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-xs mb-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-3 border-b border-slate-100 gap-3">
        <div className="flex items-center space-x-2.5">
          <div className="p-2 bg-blue-100 text-blue-700 rounded-lg">
            <Layers className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-base font-bold text-slate-900">
              {t('Fictional Test Scenarios', 'काल्पनिक परीक्षण परिदृश्य')}
            </h2>
            <p className="text-xs text-slate-500">
              {t(
                'Switch scenarios to test discrepancy detection, missing fields, and eligibility limits.',
                'विसंगतियों, छूटे हुए फ़ील्ड और पात्रता सीमाओं का परीक्षण करने के लिए परिदृश्य बदलें।'
              )}
            </p>
          </div>
        </div>
        <button
          onClick={resetSession}
          disabled={isLoading}
          className="flex items-center space-x-1.5 px-3 py-1.5 text-xs font-semibold text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-xl transition-colors cursor-pointer self-start sm:self-auto"
        >
          <RotateCcw className={`w-3.5 h-3.5 ${isLoading ? 'animate-spin' : ''}`} />
          <span>{t('Reset to Initial Sample', 'मूल नमूने पर रीसेट करें')}</span>
        </button>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 mt-4">
        {scenarios.map((scen) => {
          const isSelected = activeScenarioId === scen.scenario_id;
          return (
            <button
              key={scen.scenario_id}
              onClick={() => selectScenario(scen.scenario_id)}
              disabled={isLoading}
              className={`p-3.5 rounded-xl text-left border transition-all cursor-pointer flex flex-col justify-between ${
                isSelected
                  ? 'bg-blue-50/80 border-blue-500 ring-2 ring-blue-500/20 shadow-xs'
                  : 'bg-slate-50 border-slate-200 hover:bg-white hover:border-slate-300'
              }`}
            >
              <div>
                <div className="flex items-center justify-between mb-1.5">
                  <span
                    className={`text-xs font-bold ${
                      isSelected ? 'text-blue-800' : 'text-slate-800'
                    }`}
                  >
                    {t(scen.title_en, scen.title_hi)}
                  </span>
                  {isSelected ? (
                    <CheckCircle2 className="w-4 h-4 text-blue-600 flex-shrink-0" />
                  ) : (
                    <span className="w-2 h-2 rounded-full bg-slate-300" />
                  )}
                </div>
                <p className="text-[11px] leading-relaxed text-slate-600 line-clamp-3">
                  {t(scen.description_en, scen.description_hi)}
                </p>
              </div>
              <div className="mt-2.5 pt-2 border-t border-slate-200/60 flex items-center justify-between text-[10px]">
                <span className={`font-semibold ${isSelected ? 'text-blue-700' : 'text-slate-500'}`}>
                  {isSelected ? t('Active Scenario', 'सक्रिय परिदृश्य') : t('Select Scenario', 'परिदृश्य चुनें')}
                </span>
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
};
