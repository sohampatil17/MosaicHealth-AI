import { useState, useEffect, useRef } from 'react';
import { Box, Button, Card, Typography } from '@mui/joy';
import KeyboardVoiceIcon from '@mui/icons-material/KeyboardVoice';
import axios from 'axios';

// Define the props type
interface TranscriptionProps {
  transcript: string;
  setTranscript: React.Dispatch<React.SetStateAction<string>>;
  setImportantData: React.Dispatch<React.SetStateAction<any>>;
  setLoadingDataSuggestions: React.Dispatch<React.SetStateAction<boolean>>;
}

function Transcription({ transcript, setTranscript, setImportantData, setLoadingDataSuggestions }: TranscriptionProps) {

  const [isListening, setIsListening] = useState(false);
  const [interimTranscript, setInterimTranscript] = useState('');
  const transcriptRef = useRef(transcript);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  // Update the ref whenever the transcript state changes
  useEffect(() => {
    transcriptRef.current = transcript;
  }, [transcript]);

  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      const recognition = new SpeechRecognition();
      recognition.continuous = true;
      recognition.interimResults = true;

      recognition.onstart = () => {
        setIsListening(true);
      };

      recognition.onresult = (event: any) => {
        setInterimTranscript("");
        for (var i = event.resultIndex; i < event.results.length; i++) {
          var transcript = event.results[i][0].transcript;
          transcript.replace("\n", "<br>");
          if (event.results[i].isFinal) {
            setTranscript((prevTranscript) => prevTranscript + ' ' + transcript + '.');
            transcriptRef.current = transcript;
          }
          else {
            setInterimTranscript((prevTranscript) => prevTranscript + ' ' + transcript);
          }
        }
      };

      recognition.onend = () => {
        setIsListening(false);
        setLoadingDataSuggestions(true);

        axios.post('http://127.0.0.1:5000/process_transcript', { transcript: transcriptRef.current })
          .then((response) => {
            setLoadingDataSuggestions(false);
            const result = JSON.parse(response.data.result); // Assuming response.data.result is a stringified JSON
            setImportantData(result);
          })
          .catch((error) => {
            console.error('There was an error processing the transcript:', error);
          });
      };

      if (isListening) {
        recognition.start();
      } else {
        recognition.stop();
      }

      return () => {
        recognition.stop();
      };
    }
  }, [isListening, setTranscript, setImportantData, setLoadingDataSuggestions]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [transcript, interimTranscript]);

  return (
    <Card color='primary' sx={{ margin: 2, marginRight: 0, marginBottom: 0, justifyContent: 'center', height: '12vh', display: 'flex', flexDirection: 'row' }}>
      <Button
        sx={{
          minWidth: 200,
          maxWidth: 200,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
        onClick={() => setIsListening((prevState) => !prevState)}
      >
        <Box component="span" sx={{ display: 'flex', alignItems: 'center' }}>
          {isListening ? (
            <>
              {/* 'Transcribing...' Button */}
              <Box
                component="img"
                src="/public/assets/speech-animation.gif" // Your GIF file path
                sx={{ width: 30, height: 'auto', marginRight: 1 }} // Adjust the size as needed
                alt="Transcribing"
              />
              Stop Transcription
            </>
          ) : (
            <>
              {/* 'Start Transcription' Button */}
              <Box
                component={KeyboardVoiceIcon}
                sx={{ width: 30, height: 30, marginRight: 1 }} // Match the size and margin with the GIF
              />
              Start Transcription
            </>
          )}
        </Box>
      </Button>
      <Card sx={{ flexGrow: 1, overflowY: 'auto', paddingBottom: 0 }}>
        <Typography sx={{ marginBottom: 0, paddingBottom: 0 }}>{transcript} {interimTranscript}</Typography>
        {/* Invisible div at the bottom of the Card content */}
        <div
          ref={messagesEndRef}
          style={{
            height: 0, // Set height to 0
            margin: 0, // Remove margins
            padding: 0, // Remove padding
            border: 'none', // Ensure there's no border
          }}
        />
      </Card>
    </Card >
  );
};

export default Transcription;