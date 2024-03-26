import { Card, Typography, Box, Button } from '@mui/joy';

interface NavbarProps {
    setTranscript: React.Dispatch<React.SetStateAction<string>>;
    setOutline: React.Dispatch<React.SetStateAction<string>>;
    setImportantData: React.Dispatch<React.SetStateAction<any>>;
}

export default function NavBar({ setTranscript, setOutline, setImportantData }: NavbarProps) {

    function handleClear() {
        setTranscript("");
        setOutline("");
        setImportantData([]);
    }

    return (
        <Card color='primary' variant='soft' sx={{ margin: 0, height: 60, justifyContent: 'center', alignItems: 'center' }}>
            <Box sx={{ display: 'flex', width: '100%', alignItems: 'center', justifyContent: 'space-between' }}>
                <Box sx={{ visibility: 'hidden' }}>
                    <Button>clear</Button> {/* Invisible button to balance the layout */}
                </Box>
                <Typography level='h2' sx={{ textAlign: 'center', flexGrow: 1 }}>Mosaic Health</Typography>
                <Box>
                    <Button color='danger' onClick={handleClear}>Clear Page</Button> {/* Actual button on the far right */}
                </Box>
            </Box>
        </Card>
    );
}

