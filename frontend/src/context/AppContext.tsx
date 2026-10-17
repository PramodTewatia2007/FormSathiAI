import React, { createContext, useContext, useState, useEffect, useRef } from 'react';
import {
  ApplicationFormData,
  DocumentMetadata,
  ChecklistResponse,
  ValidationResponse,
  FieldExplanation,
  DemoScenario,
  PredefinedQuestion
} from '../types';

interface AppContextType {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  sessionId: string;
  applicationForm: ApplicationFormData | null;
  documents: DocumentMetadata[];
  checklist: ChecklistResponse | null;
  validation: ValidationResponse | null;
  scenarios: DemoScenario[];
  activeScenarioId: string;
  fieldExplanations: Record<string, FieldExplanation>;
  predefinedQuestions: PredefinedQuestion[];
  consentGiven: boolean;
  showConsentModal: boolean;
  setShowConsentModal: (show: boolean) => void;
  ocrReviewDoc: DocumentMetadata | null;
  setOcrReviewDoc: (doc: DocumentMetadata | null) => void;
  isLoading: boolean;
  error: string | null;
  loadDemoData: () => Promise<void>;
  selectScenario: (scenarioId: string) => Promise<void>;
  updateFormField: <K extends keyof ApplicationFormData>(field: K, value: ApplicationFormData[K]) => Promise<void>;
  giveConsent: (consent: boolean) => Promise<void>;
  resetSession: () => Promise<void>;
  refreshAnalysis: (formOverride?: ApplicationFormData) => Promise<void>;
  deleteDocument: (documentId: string) => Promise<void>;
  updateOcrText: (documentId: string, correctedText: string) => Promise<void>;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

const getSessionId = (): string => {
  const key = 'formsathi_session_id';
  try {
    const saved = window.sessionStorage.getItem(key);
    if (saved) return saved;
    const id = window.crypto.randomUUID();
    window.sessionStorage.setItem(key, id);
    return id;
  } catch {
    // Keep the app usable when browser storage is unavailable. This fallback
    // lasts only for this page load and is still unique per app instance.
    return window.crypto.randomUUID();
  }
};

const getErrorMessage = (error: unknown, fallback: string): string =>
  error instanceof Error ? error.message : fallback;

export const AppProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [activeTab, setActiveTab] = useState<string>('dashboard');
  const [sessionId] = useState<string>(getSessionId);
  const [applicationForm, setApplicationForm] = useState<ApplicationFormData | null>(null);
  const [documents, setDocuments] = useState<DocumentMetadata[]>([]);
  const [checklist, setChecklist] = useState<ChecklistResponse | null>(null);
  const [validation, setValidation] = useState<ValidationResponse | null>(null);
  const [scenarios, setScenarios] = useState<DemoScenario[]>([]);
  const [activeScenarioId, setActiveScenarioId] = useState<string>('scenario_1');
  const [fieldExplanations, setFieldExplanations] = useState<Record<string, FieldExplanation>>({});
  const [predefinedQuestions, setPredefinedQuestions] = useState<PredefinedQuestion[]>([]);
  const [consentGiven, setConsentGiven] = useState<boolean>(false);
  const [showConsentModal, setShowConsentModal] = useState<boolean>(false);
  const [ocrReviewDoc, setOcrReviewDoc] = useState<DocumentMetadata | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const formUpdateQueue = useRef<Promise<void>>(Promise.resolve());
  const latestFormRef = useRef<ApplicationFormData | null>(applicationForm);
  latestFormRef.current = applicationForm;

  const fetchSessionDocs = async () => {
    try {
      const res = await fetch(`/api/documents?session_id=${sessionId}`);
      if (res.ok) {
        const data = await res.json();
        setDocuments(data.documents || []);
      }
    } catch (err) {
      console.error('Failed to fetch documents', err);
    }
  };

  const refreshAnalysis = async (formOverride?: ApplicationFormData) => {
    const formToUse = formOverride || applicationForm;
    if (!formToUse) return;

    try {
      const [chkRes, valRes] = await Promise.all([
        fetch(`/api/checklist?session_id=${sessionId}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(formToUse)
        }),
        fetch(`/api/validate?session_id=${sessionId}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(formToUse)
        })
      ]);

      if (chkRes.ok) {
        const chkData = await chkRes.json();
        setChecklist(chkData);
      }
      if (valRes.ok) {
        const valData = await valRes.json();
        setValidation(valData);
      }
    } catch (err) {
      console.error('Error refreshing analysis', err);
    }
  };

  const loadDemoData = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const [demoRes, scenRes, statusRes] = await Promise.all([
        fetch(`/api/demo?session_id=${sessionId}`),
        fetch('/api/demo/scenarios'),
        fetch(`/api/session/status?session_id=${sessionId}`)
      ]);

      if (!demoRes.ok) throw new Error('Failed to load demo data');

      const demoData = await demoRes.json();
      const scenData = await scenRes.json();
      const statusData = await statusRes.json();

      setApplicationForm(demoData.application_form);
      latestFormRef.current = demoData.application_form;
      setFieldExplanations(demoData.field_explanations || {});
      setPredefinedQuestions(demoData.predefined_questions || []);
      setScenarios(scenData.scenarios || []);
      setConsentGiven(statusData.consent_given || false);

      await fetchSessionDocs();
      await refreshAnalysis(demoData.application_form);
    } catch (err: unknown) {
      setError(getErrorMessage(err, 'Error connecting to FormSathiAI backend'));
    } finally {
      setIsLoading(false);
    }
  };

  const selectScenario = async (scenarioId: string) => {
    setIsLoading(true);
    try {
      await formUpdateQueue.current.catch(() => undefined);
      const res = await fetch('/api/demo/scenario', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionId, scenario_id: scenarioId })
      });
      if (!res.ok) throw new Error('Failed to load scenario');
      const data = await res.json();
      setApplicationForm(data.application_form);
      latestFormRef.current = data.application_form;
      setActiveScenarioId(scenarioId);
      await refreshAnalysis(data.application_form);
    } catch (err: unknown) {
      setError(getErrorMessage(err, 'Failed to load scenario'));
    } finally {
      setIsLoading(false);
    }
  };

  const updateFormField = async <K extends keyof ApplicationFormData>(field: K, value: ApplicationFormData[K]) => {
    if (!applicationForm) return;
    const updated = { ...applicationForm, [field]: value };
    latestFormRef.current = updated;
    setApplicationForm(updated);

    const queuedUpdate = formUpdateQueue.current.catch(() => undefined).then(async () => {
      const res = await fetch(`/api/form/update?session_id=${sessionId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updated)
      });
      if (!res.ok) throw new Error('Failed to save application changes');
      // Serialize edits to prevent older keystrokes from overwriting newer
      // values, and refresh the analysis once the latest edit has persisted.
      if (latestFormRef.current === updated) await refreshAnalysis(updated);
    });
    formUpdateQueue.current = queuedUpdate;
    try {
      await queuedUpdate;
    } catch (err) {
      console.error('Error updating form field', err);
    }
  };

  const giveConsent = async (consent: boolean) => {
    try {
      const res = await fetch('/api/session/consent', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionId, consent_given: consent })
      });
      if (res.ok) {
        const data = await res.json();
        setConsentGiven(consent);
        if (!consent && data.application_form) {
          setApplicationForm(data.application_form);
          latestFormRef.current = data.application_form;
          setDocuments([]);
          setActiveScenarioId('scenario_1');
          await refreshAnalysis(data.application_form);
        }
        setShowConsentModal(false);
      }
    } catch (err) {
      console.error('Error updating consent', err);
    }
  };

  const resetSession = async () => {
    setIsLoading(true);
    try {
      await formUpdateQueue.current.catch(() => undefined);
      const res = await fetch(`/api/session/reset?session_id=${sessionId}`, { method: 'POST' });
      if (res.ok) {
        const data = await res.json();
        setApplicationForm(data.application_form);
        latestFormRef.current = data.application_form;
        setDocuments([]);
        setConsentGiven(data.consent_given || false);
        setOcrReviewDoc(null);
        setShowConsentModal(false);
        setActiveScenarioId('scenario_1');
        await refreshAnalysis(data.application_form);
      }
    } catch (err) {
      console.error('Failed to reset session', err);
    } finally {
      setIsLoading(false);
    }
  };

  const deleteDocument = async (documentId: string) => {
    try {
      const res = await fetch(`/api/documents/${documentId}?session_id=${sessionId}`, {
        method: 'DELETE'
      });
      if (res.ok) {
        const data = await res.json();
        setApplicationForm(data.application_form);
        latestFormRef.current = data.application_form;
        await fetchSessionDocs();
        await refreshAnalysis(data.application_form);
      }
    } catch (err) {
      console.error('Failed to delete document', err);
    }
  };

  const updateOcrText = async (documentId: string, correctedText: string) => {
    try {
      const res = await fetch('/api/documents/ocr-correct', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          document_id: documentId,
          session_id: sessionId,
          corrected_text: correctedText
        })
      });
      if (res.ok) {
        await fetchSessionDocs();
        setOcrReviewDoc(null);
      }
    } catch (err) {
      console.error('Failed to correct OCR text', err);
    }
  };

  useEffect(() => {
    loadDemoData();
  }, []);

  return (
    <AppContext.Provider
      value={{
        activeTab,
        setActiveTab,
        sessionId,
        applicationForm,
        documents,
        checklist,
        validation,
        scenarios,
        activeScenarioId,
        fieldExplanations,
        predefinedQuestions,
        consentGiven,
        showConsentModal,
        setShowConsentModal,
        ocrReviewDoc,
        setOcrReviewDoc,
        isLoading,
        error,
        loadDemoData,
        selectScenario,
        updateFormField,
        giveConsent,
        resetSession,
        refreshAnalysis,
        deleteDocument,
        updateOcrText,
      }}
    >
      {children}
    </AppContext.Provider>
  );
};

export const useApp = (): AppContextType => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
};
