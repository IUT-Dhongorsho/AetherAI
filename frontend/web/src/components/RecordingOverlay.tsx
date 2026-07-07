import React from 'react';
import { useAudioRecorder } from '../lib/useAudioRecorder';

interface RecordingOverlayProps {
  onCancel: () => void;
  onComplete: (audioBlob: Blob) => void;
}

const RecordingOverlay: React.FC<RecordingOverlayProps> = ({ onCancel, onComplete }) => {
  const { phase, errorMessage, timeLeft, cancelRecording, audioUrl, proceedToAnalysis } = useAudioRecorder(onComplete, 5);

  const handleCancel = () => {
    cancelRecording();
    onCancel();
  };

  const formattedTime = `00:0${timeLeft}`;

  return (
    <>
      <div className="fixed inset-0 bg-on-surface/40 backdrop-blur-[4px] z-40"></div>
      <div className="fixed inset-0 z-50 flex justify-center items-center p-md">
        <div className="relative bg-surface w-full max-w-[512px] rounded-xl border border-outline-variant shadow-[0_4px_12px_rgba(0,0,0,0.08)] p-xl flex flex-col items-center text-center overflow-hidden">
          
          {/* Main Content (Blurred while requesting permissions) */}
          <div className={`w-full flex flex-col items-center transition-all duration-300 ${phase === 'requesting' ? 'blur-sm opacity-40 select-none pointer-events-none' : ''}`}>
            
            {phase === 'review' ? (
              <div className="w-full flex flex-col items-center mb-xl animate-in fade-in zoom-in duration-300">
                <div className="w-20 h-20 rounded-full bg-primary-container text-on-primary-container flex justify-center items-center mb-md shadow-sm">
                  <span className="material-symbols-outlined text-[36px]">play_circle</span>
                </div>
                <h3 className="font-headline-md text-headline-md text-on-surface mb-md">Review Recording</h3>
                
                {audioUrl && (
                  <audio 
                    controls 
                    src={audioUrl} 
                    className="w-full max-w-[300px] mb-md outline-none"
                  >
                    Your browser does not support the audio element.
                  </audio>
                )}
                
                <p className="font-body-md text-body-md text-secondary">
                  Please review the audio before sending it to the AI for analysis.
                </p>
              </div>
            ) : (
              <>
                <div className="relative w-24 h-24 flex justify-center items-center mb-xl">
                  {phase !== 'error' && (
                    <>
                      <div className={`absolute inset-0 rounded-full pulse-ring ${phase === 'listening' ? 'bg-primary-container' : 'bg-tertiary-container'}`}></div>
                      <div className={`absolute inset-0 rounded-full scale-125 pulse-ring ${phase === 'listening' ? 'bg-primary/20' : 'bg-tertiary/20'}`} style={{ animationDelay: '0.5s' }}></div>
                    </>
                  )}
                  <div className={`relative w-16 h-16 rounded-full flex justify-center items-center shadow-lg z-10 ${phase === 'error' ? 'bg-error text-on-error' : phase === 'listening' ? 'bg-primary text-on-primary' : 'bg-tertiary text-on-tertiary'}`}>
                    <span className="material-symbols-outlined" style={{ fontSize: '32px', fontVariationSettings: "'FILL' 1" }}>
                      {phase === 'error' ? 'mic_off' : phase === 'listening' ? 'mic' : 'troubleshoot'}
                    </span>
                  </div>
                </div>

                {phase !== 'error' && (
                  <div className="flex items-end gap-2 h-16 mb-lg">
                    {[1, 2, 3, 4, 5, 6, 7].map((i) => (
                      <div 
                        key={i} 
                        className={`w-2 rounded-full visualizer-bar bar-${i} h-full transform origin-bottom ${phase === 'listening' ? 'bg-primary' : 'bg-tertiary-container'}`}
                        style={phase === 'analyzing' ? { animationDuration: `${Math.random() * 0.5 + 0.2}s` } : {}}
                      ></div>
                    ))}
                  </div>
                )}

                <div className="mb-xl w-full">
                  <h2 className="font-headline-md text-headline-md text-on-surface mb-sm transition-opacity duration-500">
                    {phase === 'error' ? 'Microphone Error' : phase === 'listening' ? 'Listening for Cough Acoustics...' : 'AI Agents Analyzing Acoustics and Symptoms...'}
                  </h2>
                  <p className="font-body-md text-body-md text-secondary font-mono-sm transition-opacity duration-500">
                    {phase === 'error' ? errorMessage : phase === 'listening' ? formattedTime : 'Processing multi-modal data...'}
                  </p>
                </div>
              </>
            )}

            <div className="flex gap-4 mt-auto">
              <button 
                onClick={handleCancel}
                className="relative z-30 bg-surface text-error border border-error hover:bg-error-container font-label-md text-label-md px-lg py-sm rounded transition-colors focus:outline-none focus:ring-2 focus:ring-error focus:ring-offset-2"
              >
                {phase === 'error' ? 'Close' : 'Cancel'}
              </button>
              
              {phase === 'review' && (
                <button 
                  onClick={proceedToAnalysis}
                  className="relative z-30 bg-primary text-on-primary hover:bg-primary-container hover:text-on-primary-container font-label-md text-label-md px-lg py-sm rounded transition-colors shadow-sm focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2"
                >
                  Analyze Acoustics
                </button>
              )}
            </div>
          </div>

          {/* Requesting Overlay Message */}
          {phase === 'requesting' && (
            <div className="absolute inset-0 z-20 flex flex-col items-center justify-center p-lg animate-in fade-in zoom-in duration-300">
              <span className="material-symbols-outlined text-[48px] text-primary mb-md animate-bounce">
                lock_open
              </span>
              <h3 className="font-headline-md text-headline-md text-on-surface mb-2">
                Allow Microphone Access
              </h3>
              <p className="font-body-md text-body-md text-secondary">
                Please click "Allow" in your browser's popup to start the acoustic recording.
              </p>
            </div>
          )}

        </div>
      </div>
    </>
  );
};

export default RecordingOverlay;
