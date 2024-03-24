import { useState, useEffect, useRef } from 'react';
import { Box, Button, Card, Typography } from '@mui/joy';
import KeyboardVoiceIcon from '@mui/icons-material/KeyboardVoice';
import axios from 'axios';

const placeholderImportantData = [
  {
    reasoning: "Mentioned *muscle pain* which can be caused by vitamin d deficiency",
    category: "Time In Daylight",
    data1_time: "6 month",
    data1_type: "mean",
    data2_time: "3 month",
    data2_type: "trend"
  },
  {
    reasoning: "Shortness of breath might indicate oxygen issues",
    category: "Oxygen Saturation",
    data1_time: "1 week",
    data1_type: "min",
    data2_time: "6 month",
    data2_type: "mean"
  },
];

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

  // set up transcription listener on component mount
  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      const recognition = new SpeechRecognition();
      recognition.continuous = true;
      recognition.interimResults = true;

      recognition.onstart = () => {
        console.log("transcrption started");
        setIsListening(true);
      };

      recognition.onend = () => {
        setIsListening(false);
        setLoadingDataSuggestions(true);
        console.log("transcrption ended");

        // Make a POST request to send the transcript to your Flask backend
        axios.post('http://127.0.0.1:5000/process_transcript', { transcript })
          .then(response => {
            // Handle the response from Flask, assuming it's the modified important data
            setLoadingDataSuggestions(false);
            console.log(response);
            const result = JSON.parse(response.data.result); // This is the content returned from Flask
            console.log(result);
            //setImportantData(result);
          })
          .catch(error => {
            console.error('There was an error processing the transcript:', error);
          });
      };

      recognition.onresult = (event: any) => {
        setInterimTranscript("");
        for (var i = event.resultIndex; i < event.results.length; i++) {
          var transcript = event.results[i][0].transcript;
          transcript.replace("\n", "<br>");
          if (event.results[i].isFinal) {
            setTranscript((prevTranscript) => prevTranscript + ' ' + transcript + '.');
          }
          else {
            setInterimTranscript((prevTranscript) => prevTranscript + ' ' + transcript);
          }
        }
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
  }, [isListening]);

  // Create a ref for the Card component that needs to auto-scroll
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  // Use useEffect to scroll to the bottom every time transcript or interimTranscript changes
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