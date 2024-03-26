import { Box, CssBaseline } from '@mui/joy';
import { CssVarsProvider, extendTheme } from '@mui/joy/styles';
import NavBar from './components/Navbar';
import Data_Insights from './components/Data_Insights';
import Transcription from './components/Transcription';
import Report from './components/Report';
import { useState } from 'react';

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

  const [transcript, setTranscript] = useState('');
  const [importantData, setImportantData] = useState<any[]>([]);
  const [outline, setOutline] = useState<string>("");
  const [loadingDataSuggestions, setLoadingDataSuggestions] = useState(false);

  return (
    <CssVarsProvider
      defaultMode="system"
      theme={my_theme}
      modeStorageKey="joy-identify-system-mode"
    >
      <CssBaseline />
      <NavBar setTranscript={setTranscript} setImportantData={setImportantData} setOutline={setOutline} />
      <Box sx={{ display: 'flex', width: '100%' }}>
        <Box sx={{ display: 'flex', flexDirection: 'column', flexGrow: 1, maxWidth: '50%', minWidth: '50%' }}>
          <Transcription transcript={transcript} setTranscript={setTranscript} setImportantData={setImportantData} setLoadingDataSuggestions={setLoadingDataSuggestions} />
          <Data_Insights importantData={importantData} setOutline={setOutline} loadingDataSuggestions={loadingDataSuggestions} transcript={transcript} />
        </Box>
        <Report outline={outline} />
      </Box>
    </CssVarsProvider >
  );
}