import { CssBaseline } from '@mui/joy';
import { CssVarsProvider, extendTheme } from '@mui/joy/styles';

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
      {/*<DarkModeDetector />*/}
      <TodoList />
    </CssVarsProvider>
  );
}