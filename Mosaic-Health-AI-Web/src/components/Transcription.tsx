import React, { useState, useEffect, useRef } from 'react';
import Button from '@mui/joy/Button'; // Import MUI Joy UI Button
import { keyframes } from '@emotion/react';

declare global {
  interface Window {
    webkitSpeechRecognition: any;
  }
}

const pulseAnimation = keyframes`
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
  }
`;

const Transcription: React.FC = () => {
  const recognitionRef = useRef<typeof window.webkitSpeechRecognition | null>(null);
  const [isRecording, setIsRecording] = useState(false);
  const [transcript, setTranscript] = useState('');

  useEffect(() => {
    recognitionRef.current = new window.webkitSpeechRecognition();
    recognitionRef.current.continuous = true;
    recognitionRef.current.interimResults = true;

    recognitionRef.current.onresult = (event: any) => {
      let interimTranscript = '';
      for (let i = event.resultIndex; i < event.results.length; i++) {
        const transcript = event.results[i][0].transcript;
        if (event.results[i].isFinal) {
          setTranscript(prevTranscript => prevTranscript + transcript + '.');
        } else {
          interimTranscript += transcript;
        }
      }
    };

    recognitionRef.current.onerror = (event: any) => {
      console.error('Speech recognition error:', event.error);
    };

    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
    };
  }, []);

  const toggleRecording = () => {
    if (recognitionRef.current) {
      if (isRecording) {
        recognitionRef.current.stop();
      } else {
        recognitionRef.current.start();
        setTranscript('');
      }
    }
    setIsRecording(!isRecording);
  };

  return (
    <div>
      <Button
        onClick={toggleRecording}
        variant={isRecording ? 'outlined' : 'solid'}
        color={isRecording ? 'danger' : 'primary'}
        sx={{
          animation: isRecording ? `${pulseAnimation} 1s infinite` : 'none',
        }}
      >
        {isRecording ? 'Stop Recording' : 'Start Recording'}
      </Button>
      <div>
        <p>Transcript:</p>
        <div>{transcript}</div>
      </div>
    </div>
  );
};

export default Transcription;
