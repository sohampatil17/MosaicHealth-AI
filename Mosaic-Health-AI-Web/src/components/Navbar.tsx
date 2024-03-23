import { Card, Typography, Box } from '@mui/joy';

export default function NavBar() {

    return (
        <Card color='primary' variant='soft' sx={{ margin: 0, height: 50, justifyContent: 'center' }}>
            <Box sx={{ display: 'flex', alignItems: 'center', marginTop: '10px' }}>
        <Typography level='h3'>Mosaic Health</Typography>
        <img src="./src/assets/mosaic-icon.svg" alt="Logo" width="50" height="50" />
    </Box>
        </Card>
    );
}
            
    