import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import RecordingOverlay from '../components/RecordingOverlay';

const PatientIntake = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const navigate = useNavigate();

  // Form State
  const [age, setAge] = useState('');
  const [duration, setDuration] = useState('');
  const [symptoms, setSymptoms] = useState({
    fever: false,
    weightLoss: false,
    nightSweats: false,
    shortnessOfBreath: false
  });

  const handleSymptomChange = (symptom: keyof typeof symptoms) => {
    setSymptoms(prev => ({ ...prev, [symptom]: !prev[symptom] }));
  };

  const handleRecordComplete = async (audioBlob: Blob) => {
    setIsRecording(false);
    setIsSubmitting(true);

    try {
      // Build notes string from symptoms
      const activeSymptoms = Object.entries(symptoms)
        .filter(([_, isActive]) => isActive)
        .map(([key]) => key.replace(/([A-Z])/g, ' $1').toLowerCase());
      
      let notes = `Symptoms: ${activeSymptoms.join(', ') || 'None'}. `;
      if (duration) notes += `Cough duration: ${duration} days.`;

      const formData = new FormData();
      // Ensure the backend receives a .wav file (even if it's technically a webm blob from the browser, we tell FastAPI it's wav or mp3 to bypass strict validation, or let FastAPI handle it)
      formData.append('audio', audioBlob, 'recording.wav');
      formData.append('pharmacist_notes', notes);
      if (age) formData.append('age', age);

      const response = await fetch('/api/v1/predict', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.statusText}`);
      }

      const data = await response.json();
      
      // Navigate to results and pass the API response data
      navigate('/results', { state: { triageData: data } });

    } catch (error) {
      console.error("Submission failed:", error);
      alert("Failed to analyze audio. Please ensure the FastAPI backend is running on port 8000.");
    } finally {
      setIsSubmitting(false);
    }
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
          {/* Patient Context Form */}
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
                    <input 
                      className="w-full bg-surface-bright border border-outline-variant rounded-lg px-3 py-2 font-mono-sm text-mono-sm focus:border-primary focus:ring-1 focus:ring-primary transition-all shadow-sm" 
                      id="patient_age" 
                      max="120" min="0" 
                      placeholder="e.g. 45" 
                      type="number"
                      value={age}
                      onChange={(e) => setAge(e.target.value)}
                    />
                  </div>
                  <div>
                    <label className="block font-label-md text-label-md text-on-surface-variant mb-1" htmlFor="cough_duration">Days with Cough</label>
                    <input 
                      className="w-full bg-surface-bright border border-outline-variant rounded-lg px-3 py-2 font-mono-sm text-mono-sm focus:border-primary focus:ring-1 focus:ring-primary transition-all shadow-sm" 
                      id="cough_duration" 
                      min="1" 
                      placeholder="e.g. 7" 
                      type="number"
                      value={duration}
                      onChange={(e) => setDuration(e.target.value)}
                    />
                  </div>
                </div>

                {/* Symptoms Checkboxes */}
                <div>
                  <label className="block font-label-md text-label-md text-on-surface-variant mb-3">Reported Symptoms</label>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    <label className="flex items-center p-3 border border-outline-variant rounded-lg hover:bg-surface-container-low cursor-pointer transition-colors group has-[:checked]:bg-surface-container has-[:checked]:border-primary">
                      <input checked={symptoms.fever} onChange={() => handleSymptomChange('fever')} className="rounded border-outline-variant text-primary focus:ring-primary mr-3 w-5 h-5 transition-all" type="checkbox" />
                      <div className="flex-1">
                        <span className="block font-body-md text-body-md font-medium text-on-surface group-has-[:checked]:text-primary-fixed-variant">Fever</span>
                        <span className="block font-label-md text-label-md text-secondary mt-0.5">&gt; 38°C / 100.4°F</span>
                      </div>
                    </label>
                    <label className="flex items-center p-3 border border-outline-variant rounded-lg hover:bg-surface-container-low cursor-pointer transition-colors group has-[:checked]:bg-surface-container has-[:checked]:border-primary">
                      <input checked={symptoms.weightLoss} onChange={() => handleSymptomChange('weightLoss')} className="rounded border-outline-variant text-primary focus:ring-primary mr-3 w-5 h-5 transition-all" type="checkbox" />
                      <div className="flex-1">
                        <span className="block font-body-md text-body-md font-medium text-on-surface group-has-[:checked]:text-primary-fixed-variant">Weight Loss</span>
                        <span className="block font-label-md text-label-md text-secondary mt-0.5">Unexplained recently</span>
                      </div>
                    </label>
                    <label className="flex items-center p-3 border border-outline-variant rounded-lg hover:bg-surface-container-low cursor-pointer transition-colors group has-[:checked]:bg-surface-container has-[:checked]:border-primary">
                      <input checked={symptoms.nightSweats} onChange={() => handleSymptomChange('nightSweats')} className="rounded border-outline-variant text-primary focus:ring-primary mr-3 w-5 h-5 transition-all" type="checkbox" />
                      <div className="flex-1">
                        <span className="block font-body-md text-body-md font-medium text-on-surface group-has-[:checked]:text-primary-fixed-variant">Night Sweats</span>
                        <span className="block font-label-md text-label-md text-secondary mt-0.5">Drenching sweats</span>
                      </div>
                    </label>
                    <label className="flex items-center p-3 border border-outline-variant rounded-lg hover:bg-surface-container-low cursor-pointer transition-colors group has-[:checked]:bg-surface-container has-[:checked]:border-primary">
                      <input checked={symptoms.shortnessOfBreath} onChange={() => handleSymptomChange('shortnessOfBreath')} className="rounded border-outline-variant text-primary focus:ring-primary mr-3 w-5 h-5 transition-all" type="checkbox" />
                      <div className="flex-1">
                        <span className="block font-body-md text-body-md font-medium text-on-surface group-has-[:checked]:text-primary-fixed-variant">Shortness of Breath</span>
                        <span className="block font-label-md text-label-md text-secondary mt-0.5">At rest/exertion</span>
                      </div>
                    </label>
                  </div>
                </div>
              </form>
            </div>
          </div>

          {/* Action Area */}
          <div className="lg:col-span-5 space-y-md">
            <div className="bg-surface-container-low border border-primary/20 rounded-xl p-lg shadow-sm flex flex-col items-center justify-center text-center relative overflow-hidden h-full min-h-[300px]">
              <div className="absolute inset-0 bg-gradient-to-br from-primary/5 to-transparent pointer-events-none"></div>
              <div className="relative z-10 w-full flex flex-col items-center">
                <h3 className="font-headline-md text-headline-md text-on-surface mb-2">Acoustic Analysis</h3>
                <p className="font-body-md text-body-md text-secondary mb-xl max-w-[320px]">Ensure the microphone is positioned ~30cm from the patient in a quiet environment.</p>
                
                <button
                  disabled={isSubmitting}
                  onClick={() => setIsRecording(true)}
                  className={`w-32 h-32 rounded-full bg-surface-container-lowest border shadow-sm flex flex-col items-center justify-center gap-2 transition-all relative group ${isSubmitting ? 'border-secondary opacity-70 cursor-not-allowed' : 'border-outline-variant hover:border-primary hover:shadow-[0_0_15px_rgba(0,104,95,0.2)]'}`}
                >
                  {!isSubmitting && <div className="absolute inset-0 rounded-full border-2 border-primary opacity-0 scale-90 group-hover:opacity-100 group-hover:animate-[ping_2s_cubic-bezier(0,0,0.2,1)_infinite]"></div>}
                  {isSubmitting ? (
                    <span className="material-symbols-outlined text-[48px] text-secondary animate-spin">autorenew</span>
                  ) : (
                    <span className="material-symbols-outlined text-[48px] text-primary group-hover:scale-110 transition-transform duration-300">mic</span>
                  )}
                  <span className={`font-label-md text-label-md font-bold ${isSubmitting ? 'text-secondary' : 'text-primary'}`}>
                    {isSubmitting ? 'ANALYZING' : 'RECORD'}
                  </span>
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
      </div>
      
      {isRecording && <RecordingOverlay onCancel={() => setIsRecording(false)} onComplete={handleRecordComplete} />}
    </>
  );
};

export default PatientIntake;
