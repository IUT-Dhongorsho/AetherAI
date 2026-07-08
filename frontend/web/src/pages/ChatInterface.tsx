import React, { useState, useEffect, useRef } from 'react';
import CoughCard from '../components/CoughCard';
import VitalsCard from '../components/VitalsCard';

interface Message {
  id: string;
  role: 'user' | 'model' | 'system';
  content: string;
}

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isRecordingVoice, setIsRecordingVoice] = useState(false);
  const [activeCard, setActiveCard] = useState<'none' | 'cough' | 'vitals'>('none');
  const [patientId] = useState('temp-patient-123'); // Often from auth or intake state
  
  const recognitionRef = useRef<any>(null);

  useEffect(() => {
    // Setup Web Speech API
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (SpeechRecognition) {
      const recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = 'en-US'; 
      
      recognition.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript;
        setInput((prev) => prev + (prev ? ' ' : '') + transcript);
      };
      
      recognition.onend = () => {
        setIsRecordingVoice(false);
      };
      
      recognitionRef.current = recognition;
    }
  }, []);

  const toggleVoiceRecording = () => {
    if (isRecordingVoice) {
      recognitionRef.current?.stop();
      setIsRecordingVoice(false);
    } else {
      recognitionRef.current?.start();
      setIsRecordingVoice(true);
    }
  };

  const sendMessage = async () => {
    if (!input.trim()) return;
    
    const newMsg: Message = { id: Date.now().toString(), role: 'user', content: input };
    setMessages(prev => [...prev, newMsg]);
    setInput('');
    
    try {
      const response = await fetch('http://localhost:8000/api/v1/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ patient_id: patientId, message: input })
      });
      
      const data = await response.json();
      
      if (data.type === 'message') {
        setMessages(prev => [...prev, { id: Date.now().toString(), role: 'model', content: data.content }]);
      } else if (data.type === 'tool_trigger') {
        if (data.action === 'show_cough_card') {
          setActiveCard('cough');
        } else if (data.action === 'show_vitals_card') {
          setActiveCard('vitals');
        } else if (data.action === 'generate_prescription') {
          setMessages(prev => [...prev, { id: Date.now().toString(), role: 'system', content: `Diagnosis complete: ${data.data.diagnosis}` }]);
        }
      }
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  const handleTestComplete = async (testType: string, blob: Blob) => {
    setActiveCard('none');
    
    const formData = new FormData();
    formData.append('patient_id', patientId);
    formData.append('test_type', testType);
    formData.append('file', blob, testType === 'cough' ? 'cough.wav' : 'vitals.webm');
    
    try {
      const response = await fetch('http://localhost:8000/api/v1/test/upload', {
        method: 'POST',
        body: formData
      });
      const data = await response.json();
      setMessages(prev => [...prev, { id: Date.now().toString(), role: 'system', content: `Test ${testType} uploaded. Results: ${JSON.stringify(data.results)}` }]);
      
      // Auto-trigger the next chat iteration to let model know we got the results
      const followupResponse = await fetch('http://localhost:8000/api/v1/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ patient_id: patientId, message: "I have completed the test." })
      });
      const fData = await followupResponse.json();
      if (fData.type === 'message') {
        setMessages(prev => [...prev, { id: Date.now().toString(), role: 'model', content: fData.content }]);
      } else if (fData.type === 'tool_trigger') {
        if (fData.action === 'show_cough_card') {
          setActiveCard('cough');
        } else if (fData.action === 'show_vitals_card') {
          setActiveCard('vitals');
        } else if (fData.action === 'generate_prescription') {
          setMessages(prev => [...prev, { id: Date.now().toString(), role: 'system', content: `Diagnosis complete: ${fData.data.diagnosis}` }]);
        }
      }
      
    } catch (error) {
      console.error('Error uploading test:', error);
    }
  };

  return (
    <div className="flex flex-col h-[80vh] max-w-4xl mx-auto bg-surface border border-surface-border rounded-xl shadow-glass overflow-hidden">
      <div className="bg-surface-elevated p-4 border-b border-surface-border flex justify-between items-center">
        <h2 className="text-xl font-semibold text-text-primary">AetherAI Doctor</h2>
      </div>
      
      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-background">
        {messages.map(msg => (
          <div key={msg.id} className={`flex ${msg.role === 'user' ? 'justify-end' : msg.role === 'system' ? 'justify-center' : 'justify-start'}`}>
            <div className={`max-w-[70%] p-3 rounded-2xl ${
              msg.role === 'user' ? 'bg-primary-500 text-white rounded-br-none' : 
              msg.role === 'system' ? 'bg-surface-elevated text-text-secondary text-sm italic' :
              'bg-surface-elevated text-text-primary rounded-bl-none border border-surface-border'
            }`}>
              {msg.content}
            </div>
          </div>
        ))}
      </div>
      
      <div className="p-4 bg-surface border-t border-surface-border flex gap-2">
        <button 
          onClick={toggleVoiceRecording}
          className={`p-3 rounded-full flex-shrink-0 transition-colors ${isRecordingVoice ? 'bg-error-500 text-white animate-pulse' : 'bg-surface-elevated text-text-secondary hover:text-primary-500'}`}
        >
          {isRecordingVoice ? '⏹' : '🎤'}
        </button>
        <input 
          type="text" 
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && sendMessage()}
          placeholder="Type or speak your symptoms..."
          className="flex-1 bg-surface-elevated border border-surface-border rounded-xl px-4 py-2 text-text-primary focus:outline-none focus:border-primary-500"
        />
        <button 
          onClick={sendMessage}
          className="bg-primary-500 hover:bg-primary-600 text-white px-6 py-2 rounded-xl transition-colors font-medium shadow-btn"
        >
          Send
        </button>
      </div>

      {activeCard === 'cough' && (
        <CoughCard onComplete={(blob) => handleTestComplete('cough', blob)} onCancel={() => setActiveCard('none')} />
      )}
      {activeCard === 'vitals' && (
        <VitalsCard onComplete={(blob) => handleTestComplete('vitals', blob)} onCancel={() => setActiveCard('none')} />
      )}
    </div>
  );
}
