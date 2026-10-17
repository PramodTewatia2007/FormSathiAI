import React from 'react';
import { AlertTriangle } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';

export const FictionalBanner: React.FC = () => {
  const { language } = useLanguage();

  return (
    <div className="bg-amber-500 text-slate-950 font-semibold px-4 py-2 text-xs md:text-sm shadow-sm flex items-center justify-center space-x-2 border-b border-amber-600 tracking-wide text-center">
      <AlertTriangle className="w-4 h-4 text-slate-950 flex-shrink-0" />
      <span>
        {language === 'hi'
          ? 'काल्पनिक डेमो — यह कोई आधिकारिक छात्रवृत्ति नहीं है — वास्तविक आवेदनों के लिए मान्य नहीं है।'
          : 'FICTIONAL DEMO — NOT AN OFFICIAL SCHOLARSHIP — NOT VALID FOR REAL APPLICATIONS.'}
      </span>
    </div>
  );
};
