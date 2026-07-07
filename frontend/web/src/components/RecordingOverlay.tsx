import { useState, useEffect } from 'react';

interface RecordingOverlayProps {
  onCancel: () => void;
  onComplete: () => void;
}

const RecordingOverlay: React.FC<RecordingOverlayProps> = ({ onCancel, onComplete }) => {
  const [phase, setPhase] = useState<'listening' | 'analyzing'>('listening');

  useEffect(() => {
    const timer = setTimeout(() => {
      setPhase('analyzing');
      const completeTimer = setTimeout(() => {
        onComplete();
      }, 3000); // simulate 3s analyzing
      return () => clearTimeout(completeTimer);
    }, 5000); // 5s recording

    return () => clearTimeout(timer);
  }, [onComplete]);

  return (
    <>
      <div className="fixed inset-0 bg-on-surface/40 backdrop-blur-[4px] z-40"></div>
      <div className="fixed inset-0 z-50 flex justify-center items-center p-md">
        <div className="relative bg-surface w-full max-w-lg rounded-xl border border-outline-variant shadow-[0_4px_12px_rgba(0,0,0,0.08)] p-xl flex flex-col items-center text-center">
          
          <div className="relative w-24 h-24 flex justify-center items-center mb-xl">
            <div className={`absolute inset-0 rounded-full pulse-ring ${phase === 'listening' ? 'bg-primary-container' : 'bg-tertiary-container'}`}></div>
            <div className={`absolute inset-0 rounded-full scale-125 pulse-ring ${phase === 'listening' ? 'bg-primary/20' : 'bg-tertiary/20'}`} style={{ animationDelay: '0.5s' }}></div>
            <div className={`relative w-16 h-16 rounded-full flex justify-center items-center shadow-lg z-10 ${phase === 'listening' ? 'bg-primary text-on-primary' : 'bg-tertiary text-on-tertiary'}`}>
              <span className="material-symbols-outlined" style={{ fontSize: '32px', fontVariationSettings: "'FILL' 1" }}>
                {phase === 'listening' ? 'mic' : 'troubleshoot'}
              </span>
            </div>
          </div>

          <div className="flex items-end gap-2 h-16 mb-lg">
            {[1, 2, 3, 4, 5, 6, 7].map((i) => (
              <div 
                key={i} 
                className={`w-2 rounded-full visualizer-bar bar-${i} h-full transform origin-bottom ${phase === 'listening' ? 'bg-primary' : 'bg-tertiary-container'}`}
                style={phase === 'analyzing' ? { animationDuration: `${Math.random() * 0.5 + 0.2}s` } : {}}
              ></div>
            ))}
          </div>

          <div className="mb-xl w-full">
            <h2 className="font-headline-md text-headline-md text-on-surface mb-sm transition-opacity duration-500">
              {phase === 'listening' ? 'Listening for Cough Acoustics...' : 'AI Agents Analyzing Acoustics and Symptoms...'}
            </h2>
            <p className="font-body-md text-body-md text-secondary font-mono-sm transition-opacity duration-500">
              {phase === 'listening' ? '00:05' : 'Processing multi-modal data...'}
            </p>
          </div>

          <button 
            onClick={onCancel}
            className="bg-surface text-error border border-error hover:bg-error-container font-label-md text-label-md px-lg py-sm rounded transition-colors focus:outline-none focus:ring-2 focus:ring-error focus:ring-offset-2"
          >
            Cancel Recording
          </button>
        </div>
      </div>
    </>
  );
};

export default RecordingOverlay;
