import React, { useState, useEffect } from 'react';
import Button from '@mui/joy/Button'; // Import MUI Joy UI Button
import { keyframes } from '@emotion/react';
declare global {
    
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
    

    const [isRecording, setIsRecording] = useState(false);


    /*const toggleRecording = () => {
        if (recognitionRef.current) {
            if (isRecording) {
                recognitionRef.current.stop();
            } else {
                recognitionRef.current.start();
            }
        }
        setIsRecording(!isRecording);
    };
    */

    return (
        <div>
            <Button 
                //onClick={toggleRecording}
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
                <div></div>
            </div>
        </div>
    );
};

export default Transcription;
