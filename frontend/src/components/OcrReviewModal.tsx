import React, { useState, useEffect } from 'react';
import { Eye, Check, X, FileSearch, Sparkles } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { useApp } from '../context/AppContext';

export const OcrReviewModal: React.FC = () => {
  const { t } = useLanguage();
  const { ocrReviewDoc, setOcrReviewDoc, updateOcrText } = useApp();
  const [editedText, setEditedText] = useState('');

  useEffect(() => {
    if (ocrReviewDoc) {
      setEditedText(ocrReviewDoc.extracted_text || '');
    }
  }, [ocrReviewDoc]);

  if (!ocrReviewDoc) return null;

  const handleSave = () => {
    updateOcrText(ocrReviewDoc.document_id, editedText);
  };

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl max-w-2xl w-full p-6 shadow-2xl border border-slate-200">
        <div className="flex items-start justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-2.5 bg-indigo-100 rounded-xl text-indigo-700">
              <FileSearch className="w-6 h-6" />
            </div>
            <div>
              <h3 className="text-lg font-bold text-slate-900">
                {t('Review & Correct OCR Text', 'OCR टेक्स्ट की समीक्षा एवं सुधार')}
              </h3>
              <p className="text-xs text-slate-500">
                {ocrReviewDoc.filename} • {t('Confidence:', 'विश्वसनीयता:')} {ocrReviewDoc.ocr_confidence ?? 95}%
              </p>
            </div>
          </div>
          <button
            onClick={() => setOcrReviewDoc(null)}
            className="text-slate-400 hover:text-slate-600 p-1 rounded-lg"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="mt-4 space-y-3">
          <p className="text-xs text-slate-600">
            {t(
              'Scanned documents may contain subtle optical recognition artifacts. You can review and edit the text below before FormSathiAI evaluates it against application rules.',
              'स्कैन किए गए दस्तावेजों में मामूली OCR त्रुटियाँ हो सकती हैं। FormSathiAI द्वारा नियमों की जाँच से पहले आप नीचे दिए गए टेक्स्ट की समीक्षा व संपादन कर सकते हैं।'
            )}
          </p>

          <div className="relative">
            <textarea
              rows={12}
              value={editedText}
              onChange={(e) => setEditedText(e.target.value)}
              className="w-full text-xs font-mono p-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:outline-hidden text-slate-800"
              placeholder={t('Extracted text will appear here...', 'निकाला गया टेक्स्ट यहाँ दिखाई देगा...')}
            />
          </div>

          <div className="flex items-center justify-between text-xs text-slate-500 pt-1">
            <span>
              {t('Extraction Method:', 'निकासी विधि:')}{' '}
              <strong className="text-slate-700">{ocrReviewDoc.extraction_method}</strong>
            </span>
            <span className="text-amber-600 font-medium">
              {t('User verified edits are saved to the active session.', 'सत्यापित संपादन सक्रिय सत्र में सहेजे जाते हैं।')}
            </span>
          </div>
        </div>

        <div className="mt-6 flex items-center justify-end space-x-3">
          <button
            type="button"
            onClick={() => setOcrReviewDoc(null)}
            className="px-4 py-2 text-xs font-semibold text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-xl transition-colors"
          >
            {t('Cancel', 'रद्द करें')}
          </button>
          <button
            type="button"
            onClick={handleSave}
            className="flex items-center space-x-1.5 px-5 py-2 text-xs font-semibold text-white bg-indigo-600 hover:bg-indigo-700 rounded-xl shadow-md transition-colors"
          >
            <Check className="w-4 h-4" />
            <span>{t('Confirm & Save OCR Text', 'पुष्टि करें और OCR टेक्स्ट सहेजें')}</span>
          </button>
        </div>
      </div>
    </div>
  );
};
