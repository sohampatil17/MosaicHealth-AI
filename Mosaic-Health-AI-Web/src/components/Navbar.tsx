import { Card, Typography } from '@mui/joy';

export default function NavBar() {

    return (
        <Card color='primary' variant='soft' sx={{ margin: 0, height: 50, justifyContent: 'center' }}>
            <Typography level='h3'>Mosaic Health</Typography>
        </Card >
    );
}