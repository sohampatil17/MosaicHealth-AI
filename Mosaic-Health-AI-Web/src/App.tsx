import { Box, CssBaseline } from '@mui/joy';
import { CssVarsProvider, extendTheme } from '@mui/joy/styles';
import NavBar from './components/Navbar';
import Data_Insights from './components/Data_Insights';
import Transcription from './components/Transcription';
import Report from './components/Report';

const my_theme = extendTheme({
  colorSchemes: {
    light: {
      palette: {
        background: {
        }
      }
    },
    dark: {
      palette: {
        background: {
        }
      }
    }
  }
});

export default function App() {

  return (
    <CssVarsProvider
      defaultMode="system"
      theme={my_theme}
      modeStorageKey="joy-identify-system-mode"
    >
      <CssBaseline />
      <NavBar />
      <Box sx={{ display: 'flex', width: '100%' }}>
        <Box sx={{ display: 'flex', flexDirection: 'column', flexGrow: 1 }}>
          <Transcription />
          <Report />
        </Box>
        <Data_Insights />
      </Box>
    </CssVarsProvider >
  );
}