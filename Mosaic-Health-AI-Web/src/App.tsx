import { Box, CssBaseline } from '@mui/joy';
import { CssVarsProvider, extendTheme } from '@mui/joy/styles';
import NavBar from './components/Navbar';
import Left_Pane from './components/Left_Pane';
import Data_Insights from './components/Data_Insights';
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

  const [transcript, setTranscript] = useState("");

  return (
    <CssVarsProvider
      defaultMode="system"
      theme={my_theme}
      modeStorageKey="joy-identify-system-mode"
    >
      <CssBaseline />
      <NavBar />
      <Box sx={{ display: 'flex', width: '100%', flexFlow: 1 }}>
        <Left_Pane />
        <Data_Insights />
      </Box>
    </CssVarsProvider >
  );
}