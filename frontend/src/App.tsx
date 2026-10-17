import React from 'react';
import { LanguageProvider, useLanguage } from './context/LanguageContext';
import { AppProvider, useApp } from './context/AppContext';
import { FictionalBanner } from './components/FictionalBanner';
import { Navbar } from './components/Navbar';
import { Dashboard } from './components/Dashboard';
import { ApplicationWorkspace } from './components/ApplicationWorkspace';
import { DocumentManager } from './components/DocumentManager';
import { ChecklistView } from './components/ChecklistView';
import { AskFormSathi } from './components/AskFormSathi';
import { PrivacyHelp } from './components/PrivacyHelp';
import { ConsentModal } from './components/ConsentModal';
import { OcrReviewModal } from './components/OcrReviewModal';

const MainContent: React.FC = () => {
  const { activeTab } = useApp();
  const { t } = useLanguage();

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 text-slate-900">
      {/* Universal Fictional Warning Banner */}
      <FictionalBanner />

      {/* Main Navigation */}
      <Navbar />

      {/* Primary View Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {activeTab === 'dashboard' && <Dashboard />}
        {activeTab === 'workspace' && <ApplicationWorkspace />}
        {activeTab === 'upload' && <DocumentManager />}
        {activeTab === 'checklist' && <ChecklistView />}
        {activeTab === 'ask' && <AskFormSathi />}
        {activeTab === 'privacy' && <PrivacyHelp />}
      </main>

      {/* Modals */}
      <ConsentModal />
      <OcrReviewModal />

      {/* Footer */}
      <footer className="bg-white border-t border-slate-200 py-6 text-center text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4 space-y-2">
          <p className="font-semibold text-slate-700">
            FormSathiAI — {t('Make complicated forms easier to understand.', 'जटिल फॉर्मों को समझना आसान बनाएं।')}
          </p>
          <p>
            {t(
              'Udaan Student Support Scholarship 2026–27 is fictional demonstration data. Not an official government or college portal.',
              'उड़ान छात्रवृत्ति 2026–27 केवल प्रदर्शन का काल्पनिक उदाहरण है। यह कोई आधिकारिक पोर्टल नहीं है।'
            )}
          </p>
        </div>
      </footer>
    </div>
  );
};

export function App() {
  return (
    <LanguageProvider>
      <AppProvider>
        <MainContent />
      </AppProvider>
    </LanguageProvider>
  );
}

export default App;
