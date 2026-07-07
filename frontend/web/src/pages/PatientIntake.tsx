import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import RecordingOverlay from '../components/RecordingOverlay';

const PatientIntake = () => {
  const [isRecording, setIsRecording] = useState(false);
  const navigate = useNavigate();

  const handleRecordComplete = (audioBlob: Blob) => {
    console.log("Recording complete. Audio blob size:", audioBlob.size);
    setIsRecording(false);
    // TODO: Send audioBlob to the FastAPI backend
    navigate('/results');
  };

  return (
    <>
      <div className="max-w-4xl mx-auto p-md md:p-lg space-y-lg mt-md relative">
        {/* Page Header */}
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 border-b border-outline-variant pb-md">
          <div>
            <h2 className="font-display text-display text-on-surface">Patient Intake</h2>
            <p className="font-body-md text-body-md text-secondary mt-1">Record patient context and initiate cough sound analysis.</p>
          </div>
          <div className="bg-surface-container-low px-4 py-2 border border-outline-variant rounded-lg flex items-center gap-3">
            <span className="material-symbols-outlined text-primary">schedule</span>
            <div>
              <p className="font-label-md text-label-md text-secondary uppercase tracking-wider">Current Session</p>
              <p className="font-mono-sm text-mono-sm text-on-surface font-medium">PT-9482-B</p>
            </div>
          </div>
        </div>

        {/* Bento Layout Container */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-lg relative">
          {/* Patient Context Form (Left Col on Desktop) */}
          <div className="lg:col-span-7 space-y-md">
            <div className="bg-surface-container-lowest border border-outline-variant rounded-xl p-lg shadow-sm">
              <div className="flex items-center gap-2 mb-md border-b border-outline-variant pb-3">
                <span className="material-symbols-outlined text-primary">medical_information</span>
                <h3 className="font-headline-md text-headline-md text-on-surface">Contextual Indicators</h3>
              </div>
              <form className="space-y-6">
                {/* Numeric Inputs */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-md">
                  <div>
                    <label className="block font-label-md text-label-md text-on-surface-variant mb-1" htmlFor="patient_age">Patient Age (Years)</label>
                    <input className="w-full bg-surface-bright border border-outline-variant rounded-lg px-3 py-2 font-mono-sm text-mono-sm focus:border-primary focus:ring-1 focus:ring-primary transition-all shadow-sm" id="patient_age" max="120" min="0" placeholder="e.g. 45" type="number" />
                  </div>
                  <div>
                    <label className="block font-label-md text-label-md text-on-surface-variant mb-1" htmlFor="cough_duration">Days with Cough</label>
                    <input className="w-full bg-surface-bright border border-outline-variant rounded-lg px-3 py-2 font-mono-sm text-mono-sm focus:border-primary focus:ring-1 focus:ring-primary transition-all shadow-sm" id="cough_duration" min="1" placeholder="e.g. 7" type="number" />
                  </div>
                </div>

                {/* Symptoms Checkboxes */}
                <div>
                  <label className="block font-label-md text-label-md text-on-surface-variant mb-3">Reported Symptoms</label>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    <label className="flex items-center p-3 border border-outline-variant rounded-lg hover:bg-surface-container-low cursor-pointer transition-colors group has-[:checked]:bg-surface-container has-[:checked]:border-primary">
                      <input className="rounded border-outline-variant text-primary focus:ring-primary mr-3 w-5 h-5 transition-all" type="checkbox" />
                      <div className="flex-1">
                        <span className="block font-body-md text-body-md font-medium text-on-surface group-has-[:checked]:text-primary-fixed-variant">Fever</span>
                        <span className="block font-label-md text-label-md text-secondary mt-0.5">&gt; 38°C / 100.4°F</span>
                      </div>
                    </label>
                    <label className="flex items-center p-3 border border-outline-variant rounded-lg hover:bg-surface-container-low cursor-pointer transition-colors group has-[:checked]:bg-surface-container has-[:checked]:border-primary">
                      <input className="rounded border-outline-variant text-primary focus:ring-primary mr-3 w-5 h-5 transition-all" type="checkbox" />
                      <div className="flex-1">
                        <span className="block font-body-md text-body-md font-medium text-on-surface group-has-[:checked]:text-primary-fixed-variant">Weight Loss</span>
                        <span className="block font-label-md text-label-md text-secondary mt-0.5">Unexplained recently</span>
                      </div>
                    </label>
                    <label className="flex items-center p-3 border border-outline-variant rounded-lg hover:bg-surface-container-low cursor-pointer transition-colors group has-[:checked]:bg-surface-container has-[:checked]:border-primary">
                      <input className="rounded border-outline-variant text-primary focus:ring-primary mr-3 w-5 h-5 transition-all" type="checkbox" />
                      <div className="flex-1">
                        <span className="block font-body-md text-body-md font-medium text-on-surface group-has-[:checked]:text-primary-fixed-variant">Night Sweats</span>
                        <span className="block font-label-md text-label-md text-secondary mt-0.5">Drenching sweats</span>
                      </div>
                    </label>
                    <label className="flex items-center p-3 border border-outline-variant rounded-lg hover:bg-surface-container-low cursor-pointer transition-colors group has-[:checked]:bg-surface-container has-[:checked]:border-primary">
                      <input className="rounded border-outline-variant text-primary focus:ring-primary mr-3 w-5 h-5 transition-all" type="checkbox" />
                      <div className="flex-1">
                        <span className="block font-body-md text-body-md font-medium text-on-surface group-has-[:checked]:text-primary-fixed-variant">Shortness of Breath</span>
                        <span className="block font-label-md text-label-md text-secondary mt-0.5">At rest or mild exertion</span>
                      </div>
                    </label>
                  </div>
                </div>
              </form>
            </div>
          </div>

          {/* Action Area (Right Col on Desktop) */}
          <div className="lg:col-span-5 space-y-md">
            <div className="bg-surface-container-low border border-primary/20 rounded-xl p-lg shadow-sm flex flex-col items-center justify-center text-center relative overflow-hidden h-full min-h-[300px]">
              <div className="absolute inset-0 bg-gradient-to-br from-primary/5 to-transparent pointer-events-none"></div>
              <div className="relative z-10 w-full flex flex-col items-center">
                <h3 className="font-headline-md text-headline-md text-on-surface mb-2">Acoustic Analysis</h3>
                <p className="font-body-md text-body-md text-secondary mb-xl max-w-[320px]">Ensure the microphone is positioned ~30cm from the patient in a quiet environment.</p>
                <button
                  onClick={() => setIsRecording(true)}
                  className="w-32 h-32 rounded-full bg-surface-container-lowest border border-outline-variant shadow-sm flex flex-col items-center justify-center gap-2 hover:border-primary hover:shadow-[0_0_15px_rgba(0,104,95,0.2)] transition-all group relative"
                >
                  <div className="absolute inset-0 rounded-full border-2 border-primary opacity-0 scale-90 group-hover:opacity-100 group-hover:animate-[ping_2s_cubic-bezier(0,0,0.2,1)_infinite]"></div>
                  <span className="material-symbols-outlined text-[48px] text-primary group-hover:scale-110 transition-transform duration-300">mic</span>
                  <span className="font-label-md text-label-md text-primary font-bold">RECORD</span>
                </button>
                <div className="mt-xl w-full max-w-[320px] bg-surface border border-outline-variant rounded-lg p-3 flex items-center justify-between shadow-sm">
                  <div className="flex items-center gap-2">
                    <span className="material-symbols-outlined text-secondary text-[16px]">settings_voice</span>
                    <span className="font-label-md text-label-md text-on-surface-variant">Input Level</span>
                  </div>
                  <div className="flex gap-1 h-3 items-end">
                    <div className="w-1.5 h-1 bg-primary/20 rounded-sm"></div>
                    <div className="w-1.5 h-2 bg-primary/40 rounded-sm"></div>
                    <div className="w-1.5 h-3 bg-primary rounded-sm animate-pulse"></div>
                    <div className="w-1.5 h-2 bg-outline-variant rounded-sm"></div>
                    <div className="w-1.5 h-1 bg-outline-variant rounded-sm"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Quick Alert / Guidance */}
        <div className="bg-surface-container-highest border-l-4 border-l-tertiary-container border border-y-outline-variant border-r-outline-variant rounded-r-lg p-md flex gap-3 shadow-sm mt-md">
          <span className="material-symbols-outlined text-tertiary-container shrink-0 mt-0.5">info</span>
          <div>
            <h4 className="font-label-md text-label-md font-bold text-on-surface mb-1">Standard Operating Procedure</h4>
            <p className="font-body-md text-body-md text-secondary">If the patient exhibits persistent high fever or severe shortness of breath, refer immediately to urgent care or emergency services regardless of acoustic triage results.</p>
          </div>
        </div>
      </div>
      
      {isRecording && <RecordingOverlay onCancel={() => setIsRecording(false)} onComplete={handleRecordComplete} />}
    </>
  );
};

export default PatientIntake;
