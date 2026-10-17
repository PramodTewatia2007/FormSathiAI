import React, { useState, useRef } from 'react';
import {
  Upload,
  FileText,
  Trash2,
  FileSearch,
  AlertCircle,
  Shield,
  Download
} from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { useApp } from '../context/AppContext';

export const DocumentManager: React.FC = () => {
  const { t } = useLanguage();
  const {
    sessionId,
    documents,
    consentGiven,
    setShowConsentModal,
    setOcrReviewDoc,
    deleteDocument,
    refreshAnalysis,
    loadDemoData
  } = useApp();

  const [dragActive, setDragActive] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const demoLibraryDocs = [
    { name: 'Udaan_Scholarship_Instructions_Demo.pdf', label_en: 'Official Instructions (4 Pages)', type: 'PDF' },
    { name: 'Udaan_Application_Form_Demo.pdf', label_en: 'Sample Application Form', type: 'PDF' },
    { name: 'Academic_Marksheet_Demo.pdf', label_en: 'Marksheet (78% Obtained)', type: 'PDF' },
    { name: 'Academic_Marksheet_Inconsistent_Demo.pdf', label_en: 'Marksheet (58% Discrepancy)', type: 'PDF' },
    { name: 'Identity_Proof_Placeholder_Demo.pdf', label_en: 'Identity Placeholder (Unverified)', type: 'PDF' },
    { name: 'Income_Certificate_Placeholder_Demo.pdf', label_en: 'Income Cert Placeholder (₹1,80,000)', type: 'PDF' },
    { name: 'Bank_Passbook_Placeholder_Demo.pdf', label_en: 'Bank Passbook Placeholder', type: 'PDF' },
    { name: 'Institution_Certificate_Demo.pdf', label_en: 'Institution Enrollment Certificate', type: 'PDF' },
    { name: 'Applicant_Declaration_Demo.pdf', label_en: 'Applicant Declaration Record', type: 'PDF' },
    { name: 'Udaan_Application_Form_Scanned_Demo.png', label_en: 'Scanned Application Form (OCR Test)', type: 'PNG' },
    { name: 'Udaan_Scholarship_Instructions_Scanned_Demo.png', label_en: 'Scanned Instructions (OCR Test)', type: 'PNG' }
  ];

  const handleFiles = async (files: FileList | null) => {
    if (!files || files.length === 0) return;
    setUploadError(null);

    if (!consentGiven) {
      setShowConsentModal(true);
      return;
    }

    setUploading(true);
    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      const formData = new FormData();
      formData.append('file', file);
      formData.append('session_id', sessionId);

      try {
        const res = await fetch('/api/documents/upload', {
          method: 'POST',
          body: formData
        });
        if (!res.ok) {
          const errData = await res.json();
          throw new Error(errData.detail || 'Upload failed');
        }
      } catch (err: unknown) {
        setUploadError(err instanceof Error ? err.message : 'Error uploading file');
      }
    }
    setUploading(false);
    await loadDemoData();
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragActive(false);
    handleFiles(e.dataTransfer.files);
  };

  return (
    <div className="space-y-6">
      {/* Upload Box */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-xs">
        <div className="flex items-center space-x-2.5 pb-4 border-b border-slate-100">
          <div className="p-2 bg-blue-100 text-blue-700 rounded-lg">
            <Upload className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-base font-bold text-slate-900">
              {t('Document Upload & Processing', 'दस्तावेज अपलोड एवं प्रसंस्करण')}
            </h3>
            <p className="text-xs text-slate-500">
              {t(
                'Digital PDFs, scanned PNG/JPGs. Tesseract OCR with manual review and correction support.',
                'डिजिटल पीडीएफ, स्कैन किए गए पीएनजी/जेपीजी। मैन्युअल समीक्षा और सुधार सहायता के साथ टेसरैक्ट ओसीआर।'
              )}
            </p>
          </div>
        </div>

        {uploadError && (
          <div className="mt-4 p-3 bg-rose-50 border border-rose-200 rounded-xl text-xs text-rose-800 flex items-center space-x-2">
            <AlertCircle className="w-4 h-4 flex-shrink-0" />
            <span>{uploadError}</span>
          </div>
        )}

        {/* Drag & Drop Zone */}
        <div
          onDragOver={(e) => { e.preventDefault(); setDragActive(true); }}
          onDragLeave={() => setDragActive(false)}
          onDrop={handleDrop}
          role="button"
          tabIndex={0}
          onClick={() => fileInputRef.current?.click()}
          onKeyDown={(e) => {
            if (e.target === e.currentTarget && (e.key === 'Enter' || e.key === ' ')) {
              e.preventDefault();
              fileInputRef.current?.click();
            }
          }}
          className={`mt-4 border-2 border-dashed rounded-2xl p-8 text-center cursor-pointer transition-colors ${
            dragActive
              ? 'border-blue-500 bg-blue-50/50'
              : 'border-slate-300 hover:border-blue-400 bg-slate-50/50'
          }`}
        >
          <input
            type="file"
            ref={fileInputRef}
            onClick={(e) => e.stopPropagation()}
            onChange={(e) => handleFiles(e.target.files)}
            multiple
            accept=".pdf,.png,.jpg,.jpeg"
            className="hidden"
          />
          <div className="flex flex-col items-center justify-center space-y-2">
            <div className="p-3 bg-white shadow-xs rounded-full border border-slate-200 text-blue-600">
              <Upload className="w-6 h-6" />
            </div>
            <p className="text-sm font-semibold text-slate-800">
              {uploading
                ? t('Processing and parsing file...', 'फ़ाइल को संसाधित व पार्स किया जा रहा है...')
                : t('Drag & drop your forms or documents here, or browse', 'अपने फॉर्म या दस्तावेज यहाँ खींचें व छोड़ें, या चुनें')}
            </p>
            <p className="text-xs text-slate-500">
              {t('Supported formats: PDF, PNG, JPG, JPEG (Max 15MB)', 'समर्थित प्रारूप: PDF, PNG, JPG, JPEG (अधिकतम 15MB)')}
            </p>
          </div>
        </div>

        {/* Privacy Note */}
        <div className="mt-3 flex items-center justify-between text-[11px] text-slate-500">
          <div className="flex items-center space-x-1.5">
            <Shield className="w-3.5 h-3.5 text-blue-600" />
            <span>
              {consentGiven
                ? t('User processing consent is active for this session.', 'इस सत्र के लिए उपयोगकर्ता प्रसंस्करण सहमति सक्रिय है।')
                : t('Consent will be requested before extracting personal data.', 'व्यक्तिगत डेटा निकालने से पहले सहमति मांगी जाएगी।')}
            </span>
          </div>
          {!consentGiven && (
            <button
              onClick={() => setShowConsentModal(true)}
              className="text-blue-600 font-semibold underline hover:text-blue-800"
            >
              {t('Grant Consent', 'सहमति दें')}
            </button>
          )}
        </div>
      </div>

      {/* Uploaded Documents List */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-xs">
        <h4 className="text-sm font-bold text-slate-900 pb-3 border-b border-slate-100 flex items-center justify-between">
          <span>{t('Active Session Documents', 'सक्रिय सत्र दस्तावेज')} ({documents.length})</span>
          <span className="text-xs font-normal text-slate-500">
            {t('Session isolated & deletable anytime', 'सत्र पृथक और किसी भी समय हटाने योग्य')}
          </span>
        </h4>

        {documents.length === 0 ? (
          <div className="py-8 text-center text-xs text-slate-500">
            {t('No documents uploaded in this session yet. Upload a file or test with sample assets below.', 'इस सत्र में अभी तक कोई दस्तावेज अपलोड नहीं किया गया है। नीचे दिए गए नमूना संपत्तियों से परीक्षण करें।')}
          </div>
        ) : (
          <div className="divide-y divide-slate-100 mt-2">
            {documents.map((doc) => (
              <div key={doc.document_id} className="py-3.5 flex items-center justify-between gap-3">
                <div className="flex items-center space-x-3">
                  <div className="p-2 bg-slate-100 rounded-lg text-slate-600">
                    <FileText className="w-5 h-5" />
                  </div>
                  <div>
                    <div className="flex items-center space-x-2">
                      <span className="text-xs font-bold text-slate-800">{doc.filename}</span>
                      <span className="text-[10px] px-2 py-0.5 rounded-full bg-slate-100 text-slate-700 font-mono">
                        {doc.extraction_method}
                      </span>
                      {doc.ocr_confidence !== null && doc.ocr_confidence !== undefined && (
                        <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 font-medium">
                          OCR: {doc.ocr_confidence}%
                        </span>
                      )}
                    </div>
                    <p className="text-[11px] text-slate-500 mt-0.5">
                      {(doc.file_size_bytes / 1024).toFixed(1)} KB • {doc.page_count} {t('page(s)', 'पेज')}
                    </p>
                  </div>
                </div>

                <div className="flex items-center space-x-2">
                  {doc.needs_ocr_review && (
                    <button
                      type="button"
                      onClick={() => setOcrReviewDoc(doc)}
                      className="flex items-center space-x-1 px-2.5 py-1 text-xs font-semibold text-indigo-700 bg-indigo-50 hover:bg-indigo-100 rounded-lg border border-indigo-200 transition-colors cursor-pointer"
                    >
                      <FileSearch className="w-3.5 h-3.5" />
                      <span>{t('Review OCR', 'OCR समीक्षा')}</span>
                    </button>
                  )}
                  <button
                    type="button"
                    onClick={() => deleteDocument(doc.document_id)}
                    className="p-1.5 text-slate-400 hover:text-rose-600 rounded-lg hover:bg-rose-50 transition-colors cursor-pointer"
                    title={t('Delete document', 'दस्तावेज हटाएं')}
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Demo Assets Library Download/Inspect Section */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-xs">
        <h4 className="text-sm font-bold text-slate-900 pb-3 border-b border-slate-100 flex items-center justify-between">
          <span>{t('Fictional Demo Documents Library', 'काल्पनिक डेमो दस्तावेज लाइब्रेरी')}</span>
          <span className="text-xs font-normal text-slate-500">
            {t('Generated official sample assets', 'उत्पन्न आधिकारिक नमूना संपत्तियाँ')}
          </span>
        </h4>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mt-4">
          {demoLibraryDocs.map((item, idx) => (
            <div
              key={idx}
              className="p-3 bg-slate-50 rounded-xl border border-slate-200 flex items-center justify-between"
            >
              <div className="space-y-0.5">
                <div className="flex items-center space-x-1.5">
                  <span className="text-xs font-bold text-slate-800">{item.name}</span>
                  <span className="text-[10px] bg-slate-200 text-slate-700 font-bold px-1.5 py-0.2 rounded-sm">
                    {item.type}
                  </span>
                </div>
                <p className="text-[11px] text-slate-500">{item.label_en}</p>
              </div>

              <a
                href={`/api/demo/files/${item.name}`}
                target="_blank"
                rel="noreferrer"
                className="flex items-center space-x-1 text-xs font-semibold text-blue-600 hover:text-blue-800 bg-white border border-slate-200 hover:border-blue-300 px-2.5 py-1 rounded-lg transition-colors cursor-pointer"
              >
                <Download className="w-3.5 h-3.5" />
                <span>{t('View', 'देखें')}</span>
              </a>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
