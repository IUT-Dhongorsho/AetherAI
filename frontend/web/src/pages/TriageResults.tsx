import { useState } from 'react';
import { useNavigate, useLocation, Navigate } from 'react-router-dom';

const TriageResults = () => {
  const [isExpanded, setIsExpanded] = useState(true);
  const navigate = useNavigate();
  const { state } = useLocation();

  // If we navigated here directly without data, redirect to intake
  const triageData = state?.triageData;
  if (!triageData) {
    return <Navigate to="/intake" replace />;
  }

  // Map API response to UI configurations
  const getTriageTheme = () => {
    switch (triageData.triage_level) {
      case "RED":
        return {
          wrapper: "bg-error-container border-error",
          text: "text-on-error-container",
          icon: "warning",
          iconBg: "bg-error/10 text-error",
          gradient: "from-error/10 to-transparent",
          innerBox: "bg-surface-container-lowest/60 border-error/20 text-on-error-container"
        };
      case "YELLOW":
        return {
          wrapper: "bg-tertiary-container border-tertiary",
          text: "text-on-tertiary-container",
          icon: "notification_important",
          iconBg: "bg-tertiary/10 text-tertiary",
          gradient: "from-tertiary/10 to-transparent",
          innerBox: "bg-surface-container-lowest/60 border-tertiary/20 text-on-tertiary-container"
        };
      default: // GREEN
        return {
          wrapper: "bg-primary-container border-primary",
          text: "text-on-primary-container",
          icon: "check_circle",
          iconBg: "bg-primary/10 text-primary",
          gradient: "from-primary/10 to-transparent",
          innerBox: "bg-surface-container-lowest/60 border-primary/20 text-on-primary-container"
        };
    }
  };

  const theme = getTriageTheme();
  
  // Format the citations list properly
  const renderCitations = () => {
    if (!triageData.citations || triageData.citations.length === 0) return null;
    return (
      <div className={`mt-md pt-md border-t border-black/10`}>
        <h4 className={`font-label-sm text-label-sm font-bold opacity-70 mb-1 ${theme.text}`}>EVIDENCE BASIS</h4>
        <ul className={`font-body-sm text-body-sm list-disc pl-4 opacity-90 ${theme.text}`}>
          {triageData.citations.map((cite: string, idx: number) => (
            <li key={idx}>{cite}</li>
          ))}
        </ul>
      </div>
    );
  };

  const handleDownloadPDF = () => {
    if (triageData.pdf_report_url) {
      window.open(triageData.pdf_report_url, '_blank');
    } else {
      alert("PDF not available");
    }
  };

  return (
    <div className="max-w-container-max mx-auto p-md md:p-lg lg:p-xl">
      {/* Context Header */}
      <div className="flex flex-col md:flex-row md:items-end justify-between mb-lg border-b border-outline-variant pb-md">
        <div>
          <div className="flex items-center gap-sm mb-xs">
            <span className="font-mono-sm text-mono-sm text-secondary bg-surface-container-highest px-xs py-[2px] rounded">
              ID: {triageData.patient_id}
            </span>
            <span className="font-mono-sm text-mono-sm text-secondary flex items-center gap-[2px]">
              <span className="material-symbols-outlined text-[14px]">schedule</span> Just Now
            </span>
          </div>
          <h1 className="font-display text-display text-on-surface">Analysis Complete</h1>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-12 gap-lg">
        {/* Primary Focus Area (Cols 1-8) */}
        <div className="col-span-1 md:col-span-8 flex flex-col gap-lg">
          
          {/* Dynamic Triage Alert Card */}
          <div className={`${theme.wrapper} border-l-[6px] rounded-r-xl p-md md:p-lg shadow-sm relative overflow-hidden flex flex-col sm:flex-row gap-md sm:gap-lg items-start transition-colors duration-500`}>
            <div className={`absolute inset-0 bg-gradient-to-r ${theme.gradient} pointer-events-none`}></div>
            <div className={`${theme.iconBg} p-sm rounded-full flex-shrink-0 z-10`}>
              <span className="material-symbols-outlined font-display text-display icon-fill" style={{ fontSize: '48px', lineHeight: '48px' }}>{theme.icon}</span>
            </div>
            <div className="z-10 flex-1">
              <span className={`font-label-md text-label-md ${theme.text} uppercase tracking-widest font-bold mb-xs block opacity-80`}>
                {triageData.triage_level} PRIORITY MATCH
              </span>
              <h2 className={`font-headline-lg text-headline-lg ${theme.text} mb-sm`}>
                {triageData.diagnosis?.primary || "Condition Analyzed"}
              </h2>
              
              <div className={`${theme.innerBox} border rounded-lg p-md mb-md backdrop-blur-sm`}>
                <h3 className="font-label-md text-label-md font-semibold flex items-center gap-xs mb-xs">
                  <span className="material-symbols-outlined text-[16px]">integration_instructions</span>
                  Clinical Instructions
                </h3>
                <p className="font-body-lg text-body-lg">
                  {triageData.action_text}
                </p>
                {renderCitations()}
              </div>
              
              <div className="flex flex-wrap gap-md mt-sm">
                <button 
                  onClick={handleDownloadPDF}
                  className="bg-primary text-on-primary font-label-md text-label-md px-md py-sm rounded-lg flex items-center gap-xs hover:bg-primary-container hover:text-on-primary-container transition-colors shadow-sm"
                >
                  <span className="material-symbols-outlined text-[18px]">picture_as_pdf</span>
                  Download Referral PDF
                </button>
                <button 
                  onClick={() => navigate('/intake')}
                  className="bg-surface-container-lowest text-on-surface border border-outline-variant font-label-md text-label-md px-md py-sm rounded-lg hover:bg-surface-container-lowest/80 transition-colors"
                >
                  Start New Patient
                </button>
              </div>
            </div>
          </div>

          {/* AI Insights Bento Grid */}
          <div className="bg-surface-container-lowest border border-outline-variant rounded-xl p-md shadow-sm">
            <div 
              className="flex items-center justify-between mb-md cursor-pointer group"
              onClick={() => setIsExpanded(!isExpanded)}
            >
              <h3 className="font-headline-md text-headline-md text-on-surface flex items-center gap-sm">
                <span className="material-symbols-outlined text-primary">memory</span>
                AI Diagnostic Insights
              </h3>
              <span 
                className={`material-symbols-outlined text-secondary group-hover:text-primary transition-colors transform duration-200 ${isExpanded ? '' : '-rotate-90'}`}
              >
                expand_more
              </span>
            </div>
            
            <div 
              className={`grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-md transition-all duration-300 origin-top overflow-hidden ${isExpanded ? 'max-h-[1000px] opacity-100 mt-4' : 'max-h-0 opacity-0 mt-0'}`}
            >
              {/* Visualization Card */}
              <div className="col-span-1 sm:col-span-2 lg:col-span-2 bg-surface-bright border border-outline-variant rounded-lg p-sm relative overflow-hidden group">
                <div className="flex justify-between items-center mb-xs px-xs">
                  <span className="font-label-md text-label-md text-secondary">Audio Spectrogram Analysis</span>
                  <span className="font-mono-sm text-mono-sm text-primary flex items-center gap-xs">
                    <span className="material-symbols-outlined text-[14px]">graphic_eq</span> Live
                  </span>
                </div>
                <div className="h-32 w-full rounded bg-on-surface-variant relative overflow-hidden">
                  <div className="absolute inset-0 bg-grid-pattern opacity-20"></div>
                  <div className="absolute bottom-0 left-0 w-full h-1/2 bg-gradient-to-t from-on-surface-variant to-transparent pointer-events-none"></div>
                </div>
              </div>

              {/* Metrics & Findings */}
              <div className="col-span-1 flex flex-col gap-md">
                <div className="bg-surface-bright border border-outline-variant rounded-lg p-md flex-1 flex flex-col justify-center">
                  <span className="font-label-md text-label-md text-secondary mb-xs">Model Used</span>
                  <span className="font-body-lg text-body-lg text-on-surface font-medium leading-tight">
                    ResNet50 + Gemini 3.5 Flash Fusion
                  </span>
                </div>
                <div className="bg-surface-bright border border-outline-variant rounded-lg p-md flex-1 flex flex-col justify-center relative overflow-hidden">
                  <div className="absolute right-0 top-0 w-16 h-16 bg-primary/5 rounded-bl-full pointer-events-none"></div>
                  <span className="font-label-md text-label-md text-secondary mb-xs">Diagnostic Confidence</span>
                  <div className="flex items-baseline gap-xs">
                    <span className="font-display text-display text-primary tracking-tighter">
                      {Math.round((triageData.diagnosis?.confidence || 0) * 100)}
                    </span>
                    <span className="font-headline-md text-headline-md text-primary">%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Secondary Area / Triage Queue Context */}
        <div className="col-span-1 md:col-span-4 flex flex-col gap-md">
          <h3 className="font-headline-md text-headline-md text-on-surface mb-xs border-b border-outline-variant pb-xs">Recent Queue Activity</h3>
          
          <div className="bg-surface-container-lowest border-l-[4px] border-tertiary rounded-r-lg p-md shadow-sm hover:shadow-md transition-shadow cursor-default group">
            <div className="flex items-start gap-sm">
              <span className="material-symbols-outlined text-tertiary mt-[2px]">warning</span>
              <div>
                <div className="flex justify-between items-center mb-xs">
                  <span className="font-mono-sm text-mono-sm text-secondary">PT-89920-Y</span>
                  <span className="font-label-md text-label-md text-secondary">10 min ago</span>
                </div>
                <h4 className="font-body-md text-body-md font-semibold text-on-surface mb-xs">Medical Review Recommended</h4>
                <p className="font-body-md text-body-md text-on-surface-variant">Refer to clinic within 48 hours for follow-up evaluation.</p>
              </div>
            </div>
          </div>

          <div className="bg-surface-container-lowest border-l-[4px] border-primary rounded-r-lg p-md shadow-sm hover:shadow-md transition-shadow cursor-default group opacity-80">
            <div className="flex items-start gap-sm">
              <span className="material-symbols-outlined text-primary mt-[2px]">check_circle</span>
              <div>
                <div className="flex justify-between items-center mb-xs">
                  <span className="font-mono-sm text-mono-sm text-secondary">PT-89919-Z</span>
                  <span className="font-label-md text-label-md text-secondary">45 min ago</span>
                </div>
                <h4 className="font-body-md text-body-md font-semibold text-on-surface mb-xs">Viral/Common Cold</h4>
                <p className="font-body-md text-body-md text-on-surface-variant font-medium">DO NOT dispense antibiotics.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TriageResults;
