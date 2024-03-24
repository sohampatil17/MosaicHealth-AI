import { Card, Typography, Box } from '@mui/joy';

export default function NavBar() {

    return (
        <Card color='primary' variant='soft' sx={{ margin: 0, height: 50, justifyContent: 'center' }}>
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <img src="/public/assets/mosaic-icon.svg" alt="Logo" width="30" height="30" />
                <Typography level='h3'>Mosaic Health</Typography>
            </Box>
        </Card>
    );
}

