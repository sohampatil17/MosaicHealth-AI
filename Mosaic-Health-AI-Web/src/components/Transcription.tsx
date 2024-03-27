import { useState, useEffect, useRef } from 'react';
import { Box, Button, Card, Modal, ModalClose, Sheet, Typography } from '@mui/joy';
import KeyboardVoiceIcon from '@mui/icons-material/KeyboardVoice';
import axios from 'axios';
import { v4 as uuidv4 } from 'uuid';
import React from 'react';

// Define the props type
interface TranscriptionProps {
  transcript: string;
  setTranscript: React.Dispatch<React.SetStateAction<string>>;
  setImportantData: React.Dispatch<React.SetStateAction<any>>;
  setLoadingDataSuggestions: React.Dispatch<React.SetStateAction<boolean>>;
}

// Define a type for the displayed words
type DisplayedWord = {
  id: string;
  word: string;
  delay: number;
};

function Transcription({ transcript, setTranscript, setImportantData, setLoadingDataSuggestions }: TranscriptionProps) {

  const transcriptRef = useRef(transcript);

  const [isListening, setIsListening] = useState(false);
  const [interimTranscript, setInterimTranscript] = useState('');
  const [displayedWords, setDisplayedWords] = useState<DisplayedWord[]>([]);
  const [transcriptModalOpen, setTranscriptModalOpan] = useState(false);
  const [copyButtonText, setCopyButtonText] = useState('Copy Report');

  // function to handle clicking the 'copy text' button
  const handleCopyText = async () => {
    try {
      await navigator.clipboard.writeText(transcript);
      setCopyButtonText('Report Copied!'); // Update button text on successful copy
      setTimeout(() => setCopyButtonText('Copy Report'), 2000); // Reset button text after 2 seconds
    } catch (err) {
      console.error('Failed to copy: ', err);
    }
  };


  // Update the ref whenever the transcript state changes
  useEffect(() => {
    transcriptRef.current = transcript;
  }, [transcript]);

  // Speech recognition hook
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
        //setInterimTranscript("");
        for (var i = event.resultIndex; i < event.results.length; i++) {
          var transcript = event.results[i][0].transcript;
          transcript.replace("\n", "<br>");
          if (event.results[i].isFinal) {

            // end of a phrase of dictation
            const finishedPhraseWords = transcript.split(' ').map((word: string, index: number) => {
              return {
                id: uuidv4(),
                word,
                delay: index * 0.2 // Calculate the delay based on the index
              };
            });
            setDisplayedWords(finishedPhraseWords);
            setTranscript((prevTranscript) => prevTranscript + ' ' + transcript + '.\n');
            transcriptRef.current = transcript;
          }
          else {
            setInterimTranscript(transcript);
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

  return (
    <Card color='primary' sx={{ justifyContent: 'center', height: '100px', maxHeight: '80px', display: 'flex', flexDirection: 'row' }}>
      <Button
        sx={{
          minWidth: 100,
          maxWidth: 100,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
        onClick={() => setIsListening((prevState) => !prevState)}
      >
        <Box component="span" sx={{ display: 'flex', alignItems: 'center' }}>
          {isListening ? (
            // End Transcription Button
            <>
              <Box
                component="img"
                src="/public/assets/speech-animation.gif" // Your GIF file path
                sx={{ width: 30, height: 'auto', marginRight: 1 }} // Adjust the size as needed
                alt="End"
              />
              End
            </>
          ) : (
            // Start Transcription' Button
            <>
              <Box
                component={KeyboardVoiceIcon}
                sx={{ width: 30, height: 30, marginRight: 1 }} // Match the size and margin with the GIF
              />
              Start
            </>
          )}
        </Box>
      </Button>
      <Card sx={{ flexGrow: 1, justifyContent: 'flex-start', flexDirection: 'row', gap: 1, padding: 1 }}>
        {displayedWords.map(({ id, word, delay }) => (
          <Box
            key={id} // Unique key for each word to trigger animations correctly
            component="span"
            sx={{
              animation: `fadein 1s ${delay * 0.3}s both`,
              '@keyframes fadein': {
                from: { opacity: 0 },
                to: { opacity: 1 },
              },
              alignSelf: 'center'
            }}
          >
            {word}
          </Box>
        ))}
      </Card>
      <Button variant="outlined" color="neutral" onClick={() => setTranscriptModalOpan(true)}>
        Transcript
      </Button>
      <Modal
        aria-labelledby="modal-title"
        aria-describedby="modal-desc"
        open={transcriptModalOpen}
        onClose={() => setTranscriptModalOpan(false)}
        sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}
      >
        <Sheet
          variant="outlined"
          sx={{
            maxWidth: 500,
            minWidth: 500,
            borderRadius: 'md',
            p: 3,
            boxShadow: 'lg',
          }}
        >
          <ModalClose variant="plain" sx={{ m: 1 }} />
          <Typography
            level="h2"
            mb={1}
          >
            Transcript
          </Typography>
          <Card variant='soft' sx={{ margin: '1' }}>
            <Typography id="modal-desc" textColor="text.tertiary" sx={{ maxHeight: 400, overflowY: 'auto' }}>
              {transcript ? (
                // we have to do this weirdness with fragments to get multiline text in the transcript
                transcript.split('\n').map((line, index) => (
                  <React.Fragment key={index}>
                    {line}
                    <br />
                  </React.Fragment>
                ))
              ) : (
                "Start dictation then view your full transcript here"
              )}
            </Typography>
          </Card>
          <Button variant="soft" onClick={handleCopyText} sx={{ marginTop: 2, justifySelf: 'center', width: '100%' }}>
            {copyButtonText}
          </Button>
        </Sheet>
      </Modal>
    </Card >
  );
};

export default Transcription;