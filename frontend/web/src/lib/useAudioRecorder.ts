import { useState, useRef, useEffect } from 'react';

export const useAudioRecorder = (
  onComplete: (audioBlob: Blob) => void,
  maxDurationSeconds: number = 5
) => {
  const [phase, setPhase] = useState<'requesting' | 'listening' | 'review' | 'analyzing' | 'error'>('requesting');
  const [errorMessage, setErrorMessage] = useState('');
  const [timeLeft, setTimeLeft] = useState(maxDurationSeconds);
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
  const [audioUrl, setAudioUrl] = useState<string | null>(null);
  
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  const isCancelledRef = useRef(false);
  const timerRef = useRef<number | null>(null);
  const countdownIntervalRef = useRef<number | null>(null);

  const cleanup = () => {
    if (timerRef.current) clearTimeout(timerRef.current);
    if (countdownIntervalRef.current) clearInterval(countdownIntervalRef.current);
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      mediaRecorderRef.current.stop();
    }
  };

  useEffect(() => {
    // Flag to handle React StrictMode double-mounting async bugs
    let isEffectActive = true;
    
    // Reset state when effect runs
    isCancelledRef.current = false;
    audioChunksRef.current = [];
    setPhase('requesting');
    setTimeLeft(maxDurationSeconds);

    const startRecording = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        
        // If the component unmounted or was cancelled while we were waiting for permissions
        if (!isEffectActive || isCancelledRef.current) {
          stream.getTracks().forEach(track => track.stop());
          return;
        }

        setPhase('listening');
        const mediaRecorder = new MediaRecorder(stream);
        mediaRecorderRef.current = mediaRecorder;
        
        mediaRecorder.ondataavailable = (event) => {
          if (event.data.size > 0 && isEffectActive && !isCancelledRef.current) {
            audioChunksRef.current.push(event.data);
          }
        };

        mediaRecorder.onstop = () => {
          // Stop all audio tracks to turn off the mic indicator
          stream.getTracks().forEach(track => track.stop());
          
          // Do nothing further if cancelled or unmounted
          if (!isEffectActive || isCancelledRef.current) return;
          
          const blob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
          setAudioBlob(blob);
          
          // Using a functional update to ensure we don't capture an old audioUrl state in cleanup
          setAudioUrl((oldUrl) => {
            if (oldUrl) URL.revokeObjectURL(oldUrl);
            return URL.createObjectURL(blob);
          });
          
          setPhase('review');
        };

        mediaRecorder.start();

        // Start countdown
        countdownIntervalRef.current = window.setInterval(() => {
          setTimeLeft((prev) => {
            if (prev <= 1) {
              if (countdownIntervalRef.current) clearInterval(countdownIntervalRef.current);
              return 0;
            }
            return prev - 1;
          });
        }, 1000);

        // Stop automatically after max duration
        timerRef.current = window.setTimeout(() => {
          if (mediaRecorder.state === 'recording') {
            mediaRecorder.stop();
          }
        }, maxDurationSeconds * 1000);

      } catch (err) {
        if (!isEffectActive) return;
        console.error("Error accessing microphone:", err);
        setPhase('error');
        setErrorMessage("Microphone access denied or unavailable.");
      }
    };

    startRecording();

    return () => {
      isEffectActive = false;
      cleanup();
    };
  }, [maxDurationSeconds]); // Removed onComplete from dependencies to avoid restarts if it changes

  useEffect(() => {
    // Cleanup URL on unmount
    return () => {
      if (audioUrl) {
        URL.revokeObjectURL(audioUrl);
      }
    };
  }, [audioUrl]);

  const cancelRecording = () => {
    isCancelledRef.current = true;
    cleanup();
  };

  const proceedToAnalysis = () => {
    if (!audioBlob) return;
    setPhase('analyzing');
    
    // Simulate 2 seconds of local analyzing before passing the blob up
    setTimeout(() => {
      onComplete(audioBlob);
    }, 2000);
  };

  return { phase, errorMessage, timeLeft, cancelRecording, audioUrl, proceedToAnalysis };
};
