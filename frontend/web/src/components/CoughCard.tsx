import React, { useState, useRef } from 'react';

export default function CoughCard({ onComplete, onCancel }: { onComplete: (blob: Blob) => void, onCancel: () => void }) {
  const [recording, setRecording] = useState(false);
  const [timeLeft, setTimeLeft] = useState(5);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      chunksRef.current = [];

      mediaRecorder.ondataavailable = (e) => chunksRef.current.push(e.data);
      mediaRecorder.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: 'audio/wav' });
        onComplete(blob);
        stream.getTracks().forEach(track => track.stop());
      };

      mediaRecorder.start();
      setRecording(true);
      
      let time = 5;
      setTimeLeft(time);
      const timer = setInterval(() => {
        time -= 1;
        setTimeLeft(time);
        if (time <= 0) {
          clearInterval(timer);
          mediaRecorder.stop();
        }
      }, 1000);
    } catch (err) {
      console.error("Error accessing microphone:", err);
    }
  };

  return (
    <div className="fixed inset-0 bg-background/80 backdrop-blur-sm flex items-center justify-center z-50">
      <div className="bg-surface border border-surface-border p-6 rounded-2xl shadow-xl max-w-md w-full flex flex-col items-center gap-4">
        <h3 className="text-xl font-bold text-text-primary">Cough Analysis</h3>
        <p className="text-text-secondary text-center">We need to record a 5-second audio clip of your cough.</p>
        
        {!recording ? (
          <button onClick={startRecording} className="bg-error-500 hover:bg-error-600 text-white px-6 py-3 rounded-xl font-medium shadow-btn transition-colors w-full">
            Start Recording
          </button>
        ) : (
          <div className="text-3xl font-bold text-error-500 animate-pulse">
            {timeLeft}s
          </div>
        )}
        
        <button onClick={onCancel} className="text-text-secondary hover:text-text-primary">
          Cancel
        </button>
      </div>
    </div>
  );
}
