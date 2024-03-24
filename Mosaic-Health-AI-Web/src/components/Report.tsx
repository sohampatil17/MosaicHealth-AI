import { useState } from 'react';
import { Card, Typography, Box, Button, Textarea } from '@mui/joy';

export default function Report() {
    const [text, setText] = useState('');
    const [copyButtonText, setCopyButtonText] = useState('Copy Text');

    const handleGenerateReport = () => {
        // Todo: Implement logic to generate the report
        console.log('Generating AI Report Outline...');
    };

    const handleCopyText = async () => {
        try {
            await navigator.clipboard.writeText(text);
            setCopyButtonText('Text Copied!'); // Update button text on successful copy
            setTimeout(() => setCopyButtonText('Copy Text'), 2000); // Reset button text after 2 seconds
        } catch (err) {
            console.error('Failed to copy: ', err);
        }
    };

    return (
        <Card variant='outlined' color='primary' sx={{ margin: 2, justifyItems: 'top', alignItems: 'center', flexGrow: 1 }}>
            <Typography level='h3' sx={{ marginBottom: 1 }}>Report Builder</Typography>
            <Box sx={{ display: 'flex', flexDirection: 'column', width: '100%' }}>
                <Textarea
                    maxRows={14}
                    placeholder='Select important data then click "Generate Report Outline" or start your own from scratch'
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    sx={{ flexGrow: 1, marginBottom: 1, paddingBottom: 2, height: '60vh' }}
                    startDecorator={
                        <Box sx={{ display: 'flex', flexDirection: 'row', gap: 1 }}>
                            <Button variant="soft" onClick={handleGenerateReport}>✨Generate Report Outline✨</Button>
                            <Button variant="soft" onClick={handleCopyText}>{copyButtonText}</Button>
                        </Box>
                    }
                />
            </Box>
        </Card>
    );
}
