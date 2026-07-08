import { useState, useEffect } from 'react';
import { useNavigate, useLocation, Navigate } from 'react-router-dom';

const TriageResults = () => {
  const [isExpanded, setIsExpanded] = useState(true);
  const [isVisible, setIsVisible] = useState(false);
  const navigate = useNavigate();
  const { state } = useLocation();

  const triageData = state?.triageData;
  if (!triageData) {
    return <Navigate to="/intake" replace />;
  }

  // Trigger entrance animation
  useEffect(() => {
    const timer = setTimeout(() => setIsVisible(true), 50);
    return () => clearTimeout(timer);
  }, []);

  // --- 1. THEME MAPPING (Crisp & Professional) ---
  const getTriageTheme = () => {
    switch (triageData.triage_level) {
      case "RED":
        return {
          border: "border-red-500",
          bgLight: "bg-red-50/80",
          text: "text-red-700",
          textDark: "text-red-900",
          icon: "warning",
          iconBg: "bg-red-100 text-red-600",
          gradient: "from-red-500/5 to-transparent",
          badge: "bg-red-500 text-white",
        };
      case "YELLOW":
        return {
          border: "border-yellow-500",
          bgLight: "bg-yellow-50/80",
          text: "text-yellow-700",
          textDark: "text-yellow-900",
          icon: "notification_important",
          iconBg: "bg-yellow-100 text-yellow-600",
          gradient: "from-yellow-500/5 to-transparent",
          badge: "bg-yellow-500 text-white",
        };
      default: // GREEN
        return {
          border: "border-green-500",
          bgLight: "bg-green-50/80",
          text: "text-green-700",
          textDark: "text-green-900",
          icon: "check_circle",
          iconBg: "bg-green-100 text-green-600",
          gradient: "from-green-500/5 to-transparent",
          badge: "bg-green-500 text-white",
        };
    }
  };

  const theme = getTriageTheme();

  // --- 2. HELPERS ---
  const renderCitations = () => {
    if (!triageData.citations || triageData.citations.length === 0) return null;
    return (
      <div className="mt-4 pt-4 border-t border-outline-variant">
        <h4 className="text-xs font-bold uppercase tracking-wider text-secondary mb-1">
          Evidence Basis
        </h4>
        <ul className="text-sm list-disc pl-4 text-on-surface-variant space-y-0.5">
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
      alert("PDF report not available for this session.");
    }
  };

  // --- 3. RENDER ---
  return (
    <div className="max-w-6xl mx-auto px-4 py-6 md:px-8 md:py-10">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-end justify-between mb-8 border-b border-outline-variant pb-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-xs font-mono text-secondary bg-surface-container-highest px-2 py-0.5 rounded">
              ID: {triageData.patient_id}
            </span>
            <span className="text-xs font-mono text-secondary flex items-center gap-1">
              <span className="material-symbols-outlined text-[14px]">schedule</span> Just Now
            </span>
          </div>
          <h1 className="font-display text-3xl md:text-4xl text-on-surface tracking-tight">
            Analysis Complete
          </h1>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* --- PRIMARY CONTENT (Cols 1-8) --- */}
        <div className="lg:col-span-8 flex flex-col gap-6">
          
          {/* Dynamic Triage Card with Entrance Animation */}
          <div
            className={`transform transition-all duration-700 ease-out ${
              isVisible ? 'translate-y-0 opacity-100' : 'translate-y-8 opacity-0'
            }`}
          >
            <div
              className={`bg-surface-container-lowest border-l-[6px] ${theme.border} rounded-xl shadow-sm overflow-hidden relative`}
            >
              {/* Subtle Gradient Overlay */}
              <div
                className={`absolute inset-0 bg-gradient-to-br ${theme.gradient} pointer-events-none`}
              ></div>

              <div className="relative z-10 p-6 md:p-8 flex flex-col sm:flex-row gap-5 sm:gap-8 items-start">
                {/* Icon */}
                <div
                  className={`${theme.iconBg} p-4 rounded-full flex-shrink-0 shadow-sm`}
                >
                  <span
                    className="material-symbols-outlined"
                    style={{ fontSize: '40px', lineHeight: '40px' }}
                  >
                    {theme.icon}
                  </span>
                </div>

                {/* Content */}
                <div className="flex-1 w-full">
                  <div className="flex flex-wrap items-center gap-3 mb-1">
                    <span
                      className={`text-xs font-bold uppercase tracking-widest ${theme.text}`}
                    >
                      {triageData.triage_level} Priority Match
                    </span>
                    <span
                      className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${theme.badge} uppercase tracking-wider`}
                    >
                      {Math.round((triageData.diagnosis?.confidence || 0) * 100)}% Confidence
                    </span>
                  </div>

                  <h2
                    className={`text-2xl font-bold mb-4 ${theme.textDark}`}
                  >
                    {triageData.diagnosis?.primary || "Condition Analyzed"}
                  </h2>

                  {/* Clinical Instructions Box */}
                  <div
                    className={`${theme.bgLight} border ${theme.border} rounded-lg p-4 md:p-5 backdrop-blur-sm`}
                  >
                    <h3 className="text-xs font-semibold flex items-center gap-1.5 text-secondary uppercase tracking-wider mb-2">
                      <span className="material-symbols-outlined text-[16px]">
                        integration_instructions
                      </span>
                      Clinical Instructions
                    </h3>
                    <p className="text-base md:text-lg font-medium text-on-surface">
                      {triageData.action_text}
                    </p>
                    {renderCitations()}
                  </div>

                  {/* Actions */}
                  <div className="flex flex-wrap gap-3 mt-6">
                    <button
                      onClick={handleDownloadPDF}
                      className="bg-primary text-on-primary text-sm font-bold px-5 py-2.5 rounded-lg flex items-center gap-2 shadow-sm hover:bg-primary/90 hover:shadow-md hover:scale-[1.02] transition-all duration-200"
                    >
                      <span className="material-symbols-outlined text-[18px]">
                        picture_as_pdf
                      </span>
                      Download Referral PDF
                    </button>
                    <button
                      onClick={() => navigate('/intake')}
                      className="bg-surface-container text-on-surface border border-outline-variant text-sm font-bold px-5 py-2.5 rounded-lg flex items-center gap-2 hover:bg-surface-container-higher hover:shadow-sm transition-all duration-200"
                    >
                      <span className="material-symbols-outlined text-[18px]">
                        add
                      </span>
                      Start New Patient
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* --- AI INSIGHTS BENTO (Spectrogram + Metrics) --- */}
          <div className="bg-surface-container-lowest border border-outline-variant rounded-xl p-5 shadow-sm">
            <div
              className="flex items-center justify-between mb-4 cursor-pointer group"
              onClick={() => setIsExpanded(!isExpanded)}
            >
              <h3 className="text-lg font-bold text-on-surface flex items-center gap-2">
                <span className="material-symbols-outlined text-primary">memory</span>
                AI Diagnostic Insights
              </h3>
              <span
                className={`material-symbols-outlined text-secondary group-hover:text-primary transition-transform duration-300 ${
                  isExpanded ? '' : '-rotate-90'
                }`}
              >
                expand_more
              </span>
            </div>

            <div
              className={`grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 transition-all duration-500 ease-in-out origin-top ${
                isExpanded
                  ? 'max-h-[800px] opacity-100 mt-1'
                  : 'max-h-0 opacity-0 mt-0 overflow-hidden'
              }`}
            >
              {/* Spectrogram Visualization Card */}
              <div className="sm:col-span-2 bg-surface-bright border border-outline-variant rounded-xl p-4 overflow-hidden group relative">
                <div className="flex justify-between items-center mb-3">
                  <span className="text-xs font-semibold text-secondary uppercase tracking-wider">
                    Audio Spectrogram Analysis
                  </span>
                  <span className="text-[10px] font-mono text-primary flex items-center gap-1">
                    <span className="material-symbols-outlined text-[14px]">graphic_eq</span> Live
                  </span>
                </div>
                {/* CSS Spectrogram (Dynamic Colorful Bars) */}
                <div className="relative h-20 w-full rounded-lg bg-surface-container-low/50 overflow-hidden flex items-end justify-around p-1">
                  {[...Array(32)].map((_, i) => {
                    const height = 20 + Math.random() * 60; // Simulate varying frequencies
                    const hue = 180 + Math.sin(i * 0.8) * 40; // Teal to Blue spectrum
                    return (
                      <div
                        key={i}
                        className="w-1.5 rounded-t-sm transition-all duration-300 hover:scale-y-110 origin-bottom"
                        style={{
                          height: `${height}%`,
                          backgroundColor: `hsl(${hue}, 80%, 60%)`,
                          opacity: 0.7 + Math.random() * 0.3,
                          animationDelay: `${i * 30}ms`,
                        }}
                      />
                    );
                  })}
                  <div className="absolute inset-0 bg-gradient-to-t from-surface-bright/10 to-transparent pointer-events-none"></div>
                </div>
              </div>

              {/* Metrics Stack */}
              <div className="flex flex-col gap-3">
                <div className="bg-surface-bright border border-outline-variant rounded-xl p-4 flex-1 flex flex-col justify-center">
                  <span className="text-[10px] font-bold uppercase tracking-wider text-secondary">
                    Model Used
                  </span>
                  <span className="text-sm font-bold text-on-surface leading-tight">
                    ResNet50 + Gemini 3.5 Flash Fusion
                  </span>
                </div>
                <div className="bg-surface-bright border border-outline-variant rounded-xl p-4 flex-1 flex flex-col justify-center relative overflow-hidden">
                  <div className="absolute right-0 top-0 w-12 h-12 bg-primary/5 rounded-bl-full pointer-events-none"></div>
                  <span className="text-[10px] font-bold uppercase tracking-wider text-secondary">
                    Diagnostic Confidence
                  </span>
                  <div className="flex items-baseline gap-1">
                    <span className="text-3xl font-bold text-primary tracking-tight">
                      {Math.round((triageData.diagnosis?.confidence || 0) * 100)}
                    </span>
                    <span className="text-lg font-bold text-primary">%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* --- SECONDARY CONTENT (Cols 9-12) --- */}
        <div className="lg:col-span-4 flex flex-col gap-4">
          <h3 className="text-lg font-bold text-on-surface border-b border-outline-variant pb-2">
            Recent Queue Activity
          </h3>

          {/* Recent Activity Item 1 */}
          <div className="bg-surface-container-lowest border-l-4 border-tertiary rounded-lg p-4 shadow-sm hover:shadow-md transition-shadow cursor-default group">
            <div className="flex items-start gap-3">
              <span className="material-symbols-outlined text-tertiary text-[20px] mt-0.5">
                warning
              </span>
              <div className="flex-1">
                <div className="flex justify-between items-center mb-1">
                  <span className="text-xs font-mono text-secondary">PT-89920-Y</span>
                  <span className="text-[10px] font-mono text-secondary">10 min ago</span>
                </div>
                <h4 className="text-sm font-semibold text-on-surface mb-0.5">
                  Medical Review Recommended
                </h4>
                <p className="text-sm text-on-surface-variant">
                  Refer to clinic within 48 hours for follow-up.
                </p>
              </div>
            </div>
          </div>

          {/* Recent Activity Item 2 */}
          <div className="bg-surface-container-lowest border-l-4 border-primary rounded-lg p-4 shadow-sm hover:shadow-md transition-shadow cursor-default group opacity-80">
            <div className="flex items-start gap-3">
              <span className="material-symbols-outlined text-primary text-[20px] mt-0.5">
                check_circle
              </span>
              <div className="flex-1">
                <div className="flex justify-between items-center mb-1">
                  <span className="text-xs font-mono text-secondary">PT-89919-Z</span>
                  <span className="text-[10px] font-mono text-secondary">45 min ago</span>
                </div>
                <h4 className="text-sm font-semibold text-on-surface mb-0.5">
                  Viral/Common Cold
                </h4>
                <p className="text-sm text-on-surface-variant font-medium">
                  DO NOT dispense antibiotics.
                </p>
              </div>
            </div>
          </div>

          {/* Empty State / Future Queue */}
          <div className="text-center py-6 border border-dashed border-outline-variant rounded-lg bg-surface-container-low">
            <span className="material-symbols-outlined text-secondary text-[32px]">
              history
            </span>
            <p className="text-sm text-secondary mt-1">More patient results will appear here.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TriageResults;