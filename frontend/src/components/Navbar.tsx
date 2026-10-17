import React from 'react';
import {
  FileText,
  RotateCcw,
  Languages,
  CheckSquare,
  HelpCircle,
  Upload,
  MessageSquare,
  Home,
  Layers
} from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { useApp } from '../context/AppContext';

export const Navbar: React.FC = () => {
  const { language, setLanguage, t } = useLanguage();
  const { activeTab, setActiveTab, resetSession, isLoading } = useApp();

  const navItems = [
    { id: 'dashboard', label_en: 'Home', label_hi: 'मुख्य पृष्ठ', icon: Home },
    { id: 'workspace', label_en: 'Try Demo', label_hi: 'डेमो आज़माएँ', icon: Layers },
    { id: 'upload', label_en: 'Upload Documents', label_hi: 'दस्तावेज अपलोड', icon: Upload },
    { id: 'checklist', label_en: 'My Checklist', label_hi: 'मेरी चेकलिस्ट', icon: CheckSquare },
    { id: 'ask', label_en: 'Ask FormSathiAI', label_hi: 'सवाल पूछें', icon: MessageSquare },
    { id: 'privacy', label_en: 'Privacy & Help', label_hi: 'गोपनीयता व सहायता', icon: HelpCircle },
  ];

  return (
    <header className="bg-white border-b border-slate-200 sticky top-0 z-40 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo & Tagline */}
          <div
            className="flex items-center space-x-3 cursor-pointer"
            onClick={() => setActiveTab('dashboard')}
          >
            <div className="w-10 h-10 rounded-lg bg-blue-600 flex items-center justify-center text-white shadow-md">
              <FileText className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="text-xl font-bold text-slate-900 tracking-tight">FormSathiAI</span>
                <span className="text-xs bg-blue-100 text-blue-800 font-semibold px-2 py-0.5 rounded-full">
                  Demo
                </span>
              </div>
              <p className="text-xs text-slate-500 hidden sm:block">
                {t('Make complicated forms easier to understand.', 'जटिल फॉर्मों को समझना आसान बनाएं।')}
              </p>
            </div>
          </div>

          {/* Navigation Links */}
          <nav className="hidden md:flex items-center space-x-1 lg:space-x-2">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  className={`flex items-center space-x-1.5 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                    isActive
                      ? 'bg-blue-50 text-blue-700 shadow-xs'
                      : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                  }`}
                >
                  <Icon className={`w-4 h-4 ${isActive ? 'text-blue-600' : 'text-slate-500'}`} />
                  <span>{t(item.label_en, item.label_hi)}</span>
                </button>
              );
            })}
          </nav>

          {/* Actions: Language Toggle & Reset */}
          <div className="flex items-center space-x-2 sm:space-x-3">
            {/* Language Selector */}
            <div className="flex items-center bg-slate-100 p-1 rounded-lg border border-slate-200">
              <Languages className="w-4 h-4 text-slate-500 ml-1.5 mr-1 hidden sm:block" />
              <button
                type="button"
                onClick={() => setLanguage('en')}
                className={`px-2 py-1 text-xs font-semibold rounded-md transition-all ${
                  language === 'en'
                    ? 'bg-white text-blue-700 shadow-xs'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                EN
              </button>
              <button
                type="button"
                onClick={() => setLanguage('hi')}
                className={`px-2 py-1 text-xs font-semibold rounded-md transition-all ${
                  language === 'hi'
                    ? 'bg-white text-blue-700 shadow-xs'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                हिन्दी
              </button>
            </div>

            {/* Reset Button */}
            <button
              type="button"
              onClick={resetSession}
              disabled={isLoading}
              title={t('Reset Demo to Initial State', 'डेमो को प्रारंभिक स्थिति में रीसेट करें')}
              className="flex items-center space-x-1.5 px-3 py-1.5 text-xs font-medium text-slate-700 bg-slate-100 hover:bg-slate-200 border border-slate-200 rounded-lg transition-colors cursor-pointer"
            >
              <RotateCcw className={`w-3.5 h-3.5 ${isLoading ? 'animate-spin' : ''}`} />
              <span className="hidden sm:inline">{t('Reset', 'रीसेट')}</span>
            </button>
          </div>
        </div>

        {/* Mobile Navigation bar */}
        <div className="flex md:hidden overflow-x-auto py-2 space-x-2 border-t border-slate-100">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`flex items-center space-x-1 px-2.5 py-1.5 rounded-md text-xs whitespace-nowrap font-medium ${
                  isActive
                    ? 'bg-blue-600 text-white'
                    : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                }`}
              >
                <Icon className="w-3.5 h-3.5" />
                <span>{t(item.label_en, item.label_hi)}</span>
              </button>
            );
          })}
        </div>
      </div>
    </header>
  );
};
