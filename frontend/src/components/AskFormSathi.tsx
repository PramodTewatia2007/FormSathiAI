import React, { useState } from 'react';
import { MessageSquare, Send, Sparkles, BookOpen } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { useApp } from '../context/AppContext';
import { AskQuestionResponse } from '../types';

export const AskFormSathi: React.FC = () => {
  const { t, language } = useLanguage();
  const { sessionId } = useApp();
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<AskQuestionResponse | null>(null);

  const sampleQuestions = [
    { en: 'What is the minimum marks requirement?', hi: 'न्यूनतम कितने प्रतिशत अंक आवश्यक हैं?' },
    { en: 'What is the annual family income limit?', hi: 'वार्षिक पारिवारिक आय की अधिकतम सीमा क्या है?' },
    { en: 'Which documents are required?', hi: 'कौन-कौन से दस्तावेज आवश्यक हैं?' },
    { en: 'What is the deadline?', hi: 'आवेदन करने की अंतिम तिथि क्या है?' },
    { en: 'Is my application complete?', hi: 'क्या मेरा आवेदन पूरा हो गया है?' },
    { en: 'Is this a real scholarship?', hi: 'क्या यह कोई वास्तविक छात्रवृत्ति है?' },
    { en: 'What is the sports quota reservation?', hi: 'खेल कोटा आरक्षण क्या है?' } // Tests strict grounding absence response
  ];

  const handleAsk = async (questionText: string) => {
    if (!questionText.trim()) return;
    setLoading(true);
    setResponse(null);
    try {
      const res = await fetch('/api/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId,
          question: questionText,
          language: language
        })
      });
      if (res.ok) {
        const data: AskQuestionResponse = await res.json();
        setResponse(data);
      }
    } catch (err) {
      console.error('Error asking FormSathiAI', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-xs">
      <div className="flex items-center space-x-2.5 pb-4 border-b border-slate-100">
        <div className="p-2 bg-indigo-100 text-indigo-700 rounded-lg">
          <MessageSquare className="w-5 h-5" />
        </div>
        <div>
          <h3 className="text-base font-bold text-slate-900">
            {t('Ask FormSathiAI', 'FormSathiAI से सवाल पूछें')}
          </h3>
          <p className="text-xs text-slate-500">
            {t(
              'Grounded answers with page numbers and section citations. Never invents unsupported rules.',
              'पेज नंबर और सेक्शन संदर्भों के साथ प्रमाणित उत्तर। बिना आधार वाले नियमों का कभी आविष्कार नहीं करता।'
            )}
          </p>
        </div>
      </div>

      {/* Clickable Quick Questions */}
      <div className="mt-4">
        <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block mb-2">
          {t('Click a sample question to try:', 'आजमाने के लिए किसी नमूना प्रश्न पर क्लिक करें:')}
        </span>
        <div className="flex flex-wrap gap-2">
          {sampleQuestions.map((q, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => {
                const text = language === 'hi' ? q.hi : q.en;
                setQuery(text);
                handleAsk(text);
              }}
              className="text-xs bg-slate-50 hover:bg-blue-50 text-slate-700 hover:text-blue-700 border border-slate-200 hover:border-blue-200 px-3 py-1.5 rounded-xl transition-all cursor-pointer text-left"
            >
              {language === 'hi' ? q.hi : q.en}
            </button>
          ))}
        </div>
      </div>

      {/* Query Input Box */}
      <div className="mt-4 flex gap-2">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleAsk(query)}
          placeholder={t(
            'Ask anything about eligibility, deadlines, documents, or rules...',
            'पात्रता, अंतिम तिथि, आवश्यक दस्तावेज या नियमों के बारे में कुछ भी पूछें...'
          )}
          className="flex-1 text-xs px-3.5 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:outline-hidden text-slate-900"
        />
        <button
          onClick={() => handleAsk(query)}
          disabled={loading || !query.trim()}
          className="flex items-center space-x-1.5 px-4 py-2.5 text-xs font-semibold text-white bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 rounded-xl shadow-xs transition-colors cursor-pointer"
        >
          <Send className={`w-3.5 h-3.5 ${loading ? 'animate-pulse' : ''}`} />
          <span>{loading ? t('Searching...', 'खोज रहे हैं...') : t('Ask', 'पूछें')}</span>
        </button>
      </div>

      {/* Answer & Grounded Citation Box */}
      {response && (
        <div className="mt-5 p-4 rounded-xl border border-indigo-100 bg-indigo-50/40 animate-in fade-in duration-150">
          <div className="flex items-center justify-between pb-2 border-b border-indigo-100 mb-2.5">
            <div className="flex items-center space-x-1.5">
              <Sparkles className="w-4 h-4 text-indigo-600" />
              <span className="text-xs font-bold text-indigo-900">
                {t('FormSathiAI Answer', 'FormSathiAI का उत्तर')}
              </span>
            </div>
            <span className="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800">
              {response.is_predefined_grounded
                ? t('Grounded in Official Instructions', 'आधिकारिक निर्देशों पर आधारित')
                : t('AI Generated', 'AI जनित')}
            </span>
          </div>

          <p className="text-sm text-slate-800 leading-relaxed font-medium">
            {response.answer}
          </p>

          {/* Citation Card */}
          <div className="mt-3 pt-3 border-t border-indigo-100/80 bg-white/80 p-3 rounded-lg border border-slate-200 text-xs space-y-1.5">
            <div className="flex items-center space-x-1 text-slate-500 font-semibold text-[11px]">
              <BookOpen className="w-3.5 h-3.5 text-indigo-500" />
              <span>{t('Grounded Source Citation:', 'प्रमाणित स्रोत संदर्भ:')}</span>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-[11px] text-slate-700">
              <div>
                <strong>{t('Document:', 'दस्तावेज:')}</strong>{' '}
                <span className="font-mono text-blue-700">{response.source_citation.document_name}</span>
              </div>
              {response.source_citation.section_heading && (
                <div>
                  <strong>{t('Section:', 'सेक्शन:')}</strong> {response.source_citation.section_heading}
                </div>
              )}
              {response.source_citation.page_number && (
                <div>
                  <strong>{t('Page Number:', 'पेज संख्या:')}</strong> {response.source_citation.page_number}
                </div>
              )}
            </div>
            {response.source_citation.supporting_quote && (
              <p className="text-[11px] italic text-slate-500 bg-slate-50 p-2 rounded border border-slate-100">
                “{response.source_citation.supporting_quote}”
              </p>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
