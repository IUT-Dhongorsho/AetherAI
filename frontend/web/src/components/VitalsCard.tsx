import React, { useState, useRef, useEffect } from 'react';

export default function VitalsCard({ onComplete, onCancel }: { onComplete: (blob: Blob) => void, onCancel: () => void }) {
  const [recording, setRecording] = useState(false);
  const [timeLeft, setTimeLeft] = useState(10);
  const videoRef = useRef<HTMLVideoElement>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const streamRef = useRef<MediaStream | null>(null);

  useEffect(() => {
    const initCamera = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        streamRef.current = stream;
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      } catch (err) {
        console.error("Error accessing camera:", err);
      }
    };
    initCamera();
    return () => {
      streamRef.current?.getTracks().forEach(track => track.stop());
    };
  }, []);

  const startRecording = () => {
    if (!streamRef.current) return;
    
    // Check supported types because webm might not be supported everywhere
    let options = {};
    if (MediaRecorder.isTypeSupported('video/webm')) {
        options = { mimeType: 'video/webm' };
    }
    const mediaRecorder = new MediaRecorder(streamRef.current, options);
    mediaRecorderRef.current = mediaRecorder;
    chunksRef.current = [];

    mediaRecorder.ondataavailable = (e) => chunksRef.current.push(e.data);
    mediaRecorder.onstop = () => {
      const type = options.mimeType || 'video/mp4';
      const blob = new Blob(chunksRef.current, { type: type });
      onComplete(blob);
    };

    mediaRecorder.start();
    setRecording(true);
    
    let time = 10;
    setTimeLeft(time);
    const timer = setInterval(() => {
      time -= 1;
      setTimeLeft(time);
      if (time <= 0) {
        clearInterval(timer);
        mediaRecorder.stop();
      }
    }, 1000);
  };

  return (
    <div className="fixed inset-0 bg-background/80 backdrop-blur-sm flex items-center justify-center z-50">
      <div className="bg-surface border border-surface-border p-6 rounded-2xl shadow-xl max-w-md w-full flex flex-col items-center gap-4">
        <h3 className="text-xl font-bold text-text-primary">Vitals Scan</h3>
        <p className="text-text-secondary text-center">Look into the camera for 10 seconds to measure Heart Rate and Respiratory Rate.</p>
        
        <div className="relative w-full aspect-video bg-black rounded-lg overflow-hidden border border-surface-border">
          <video ref={videoRef} autoPlay muted playsInline className="w-full h-full object-cover" />
          <div className="absolute inset-0 border-2 border-primary-500/50 m-8 rounded-lg pointer-events-none"></div>
        </div>
        
        {!recording ? (
          <button onClick={startRecording} className="bg-primary-500 hover:bg-primary-600 text-white px-6 py-3 rounded-xl font-medium shadow-btn transition-colors w-full">
            Start Scan
          </button>
        ) : (
          <div className="text-3xl font-bold text-primary-500 animate-pulse">
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
