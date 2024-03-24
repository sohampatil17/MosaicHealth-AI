import { Card, Typography } from '@mui/joy';
import Transcription from './Transcription'; 

export default function Left_Pane() {

    return (
        <Card color='primary' sx={{ margin: 2, marginRight: 0, justifyContent: 'center', flexGrow: 1, height: 'calc(100vh - 80px)' }}>
            <Transcription/>
        </Card >
    );
}