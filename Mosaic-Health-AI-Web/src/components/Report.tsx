import { useEffect, useState } from 'react';
import { Card, Typography, Box, Button, Textarea } from '@mui/joy';

interface ReportProps {
    outline: string;
}


export default function Report({ outline }: ReportProps) {
    const [text, setText] = useState('');
    const [copyButtonText, setCopyButtonText] = useState('Copy Report');

    // Load outline into text area if it ever changes 
    useEffect(() => {
        setText(outline);
    }, [outline]);

    // function to handle clicking the 'copy text' button
    const handleCopyText = async () => {
        try {
            await navigator.clipboard.writeText(text);
            setCopyButtonText('Report Copied!'); // Update button text on successful copy
            setTimeout(() => setCopyButtonText('Copy Report'), 2000); // Reset button text after 2 seconds
        } catch (err) {
            console.error('Failed to copy: ', err);
        }
    };

    return (
        <Card variant='outlined' color='primary' sx={{ justifyItems: 'top', alignItems: 'center', flexGrow: 1, justifyContent: 'space-between' }}>
            <Typography level='h2' sx={{ marginBottom: 1, marginTop: 1, alignSelf: 'start' }}>Report Builder</Typography>
            <Box sx={{ display: 'flex', flexDirection: 'column', width: '100%' }}>
                <Textarea
                    maxRows={14}
                    placeholder='Select important data then click "Generate Report Outline" or start your own from scratch'
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    sx={{ flexGrow: 1, marginBottom: 1, paddingBottom: 2, height: 'calc(100vh - 240px)' }}
                />
                <Button variant="soft" onClick={handleCopyText}>{copyButtonText}</Button>
            </Box>
        </Card>
    );
}
