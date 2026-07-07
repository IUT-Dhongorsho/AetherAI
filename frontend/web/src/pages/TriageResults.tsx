import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const TriageResults = () => {
  const [isExpanded, setIsExpanded] = useState(true);
  const navigate = useNavigate();

  return (
    <div className="max-w-container-max mx-auto p-md md:p-lg lg:p-xl">
      {/* Context Header */}
      <div className="flex flex-col md:flex-row md:items-end justify-between mb-lg border-b border-outline-variant pb-md">
        <div>
          <div className="flex items-center gap-sm mb-xs">
            <span className="font-mono-sm text-mono-sm text-secondary bg-surface-container-highest px-xs py-[2px] rounded">ID: PT-89921-X</span>
            <span className="font-mono-sm text-mono-sm text-secondary flex items-center gap-[2px]">
              <span className="material-symbols-outlined text-[14px]">schedule</span> 14:02, Today
            </span>
          </div>
          <h1 className="font-display text-display text-on-surface">Analysis Complete</h1>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-12 gap-lg">
        {/* Primary Focus Area (Cols 1-8) */}
        <div className="col-span-1 md:col-span-8 flex flex-col gap-lg">
          {/* RED STATE: Critical Triage Alert */}
          <div className="bg-error-container border-l-[6px] border-error rounded-r-xl p-md md:p-lg shadow-sm relative overflow-hidden flex flex-col sm:flex-row gap-md sm:gap-lg items-start">
            <div className="absolute inset-0 bg-gradient-to-r from-error/10 to-transparent pointer-events-none"></div>
            <div className="bg-error/10 p-sm rounded-full flex-shrink-0 z-10">
              <span className="material-symbols-outlined text-error font-display text-display icon-fill" style={{ fontSize: '48px', lineHeight: '48px' }}>warning</span>
            </div>
            <div className="z-10 flex-1">
              <span className="font-label-md text-label-md text-on-error-container uppercase tracking-widest font-bold mb-xs block opacity-80">CRITICAL PRIORITY MATCH</span>
              <h2 className="font-headline-lg text-headline-lg text-on-error-container mb-sm">High Suspicion of TB/Pneumonia</h2>
              <div className="bg-surface-container-lowest/60 border border-error/20 rounded-lg p-md mb-md backdrop-blur-sm">
                <h3 className="font-label-md text-label-md text-on-error-container font-semibold flex items-center gap-xs mb-xs">
                  <span className="material-symbols-outlined text-[16px]">integration_instructions</span>
                  Clinical Instructions
                </h3>
                <p className="font-body-lg text-body-lg text-on-error-container">
                  Refer immediately for GeneXpert test. Instruct patient to wear an N95 mask immediately and isolate.
                </p>
              </div>
              <div className="flex flex-wrap gap-md mt-sm">
                <button className="bg-primary text-on-primary font-label-md text-label-md px-md py-sm rounded-lg flex items-center gap-xs hover:bg-primary-container hover:text-on-primary-container transition-colors shadow-sm">
                  <span className="material-symbols-outlined text-[18px]">picture_as_pdf</span>
                  Generate Referral PDF
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
                  <span className="font-label-md text-label-md text-secondary mb-xs">Primary Finding</span>
                  <span className="font-body-lg text-body-lg text-on-surface font-medium leading-tight">
                    ResNet50 detected distinct <span className="text-error font-bold">crackles</span> in lower lobes.
                  </span>
                </div>
                <div className="bg-surface-bright border border-outline-variant rounded-lg p-md flex-1 flex flex-col justify-center relative overflow-hidden">
                  <div className="absolute right-0 top-0 w-16 h-16 bg-primary/5 rounded-bl-full pointer-events-none"></div>
                  <span className="font-label-md text-label-md text-secondary mb-xs">Model Confidence</span>
                  <div className="flex items-baseline gap-xs">
                    <span className="font-display text-display text-primary tracking-tighter">94</span>
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
          
          {/* YELLOW STATE: Warning Alert Card */}
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

          {/* GREEN STATE: Safe Alert Card */}
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

          <div className="bg-surface-container-lowest border-l-[4px] border-outline rounded-r-lg p-md shadow-sm opacity-60">
            <div className="flex items-start gap-sm">
              <span className="material-symbols-outlined text-secondary mt-[2px]">info</span>
              <div>
                <div className="flex justify-between items-center mb-xs">
                  <span className="font-mono-sm text-mono-sm text-secondary">PT-89918-W</span>
                  <span className="font-label-md text-label-md text-secondary">1 hr ago</span>
                </div>
                <h4 className="font-body-md text-body-md font-semibold text-on-surface">Baseline Scan Complete</h4>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TriageResults;
