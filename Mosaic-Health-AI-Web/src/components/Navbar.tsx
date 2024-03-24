import { Card, Typography, Box } from '@mui/joy';

export default function NavBar() {

    return (
        <Card color='primary' variant='soft' sx={{ margin: 0, height: 50, justifyContent: 'center', alignItems: 'center' }}>
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <Typography level='h2'>Mosaic Health</Typography>
            </Box>
        </Card>
    );
}

