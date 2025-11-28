// src/theme.ts
import { createTheme } from "@mui/material/styles";

const darkTheme = createTheme({
  palette: {
    mode: "dark", // Enable the dark mode base settings
    background: {
      default: "#121212", // The main page background color
      paper: "#121212ff", // Background color for cards, dialogs, etc.
    },
    primary: {
      main: "#ad65f4",
    },
    secondary: {
      main: "#FF5733",
    },
    text: {
      primary: "#FFFFFF", // Pure white for primary text (your recommended #FFFFFF)
      secondary: "#B0B0B0", // A lighter gray for secondary text
    },
  },
  components: {
    MuiOutlinedInput: {
      styleOverrides: {
        root: {
          backgroundColor: "#333131ff",
          transition: "background-color 0.3s ease",
          // Default border color when not focused
          "& .MuiOutlinedInput-notchedOutline": {
            borderColor: "#B0B0B0", // e.g., your secondary text color
          },
          // Hover state border color
          "&:hover .MuiOutlinedInput-notchedOutline": {
            borderColor: "#FFFFFF", // e.g., your primary text color on hover
          },
          // Focused state border color (will use primary.main by default if you don't define here)
          "&.Mui-focused .MuiOutlinedInput-notchedOutline": {
            borderColor: "#ad65f4", // Your primary main color
          },
        },
      },
    },

    MuiFormLabel: {
      // Targets labels across all form components (TextField, Select, Checkbox, etc.)
      styleOverrides: {
        asterisk: {
          color: "#FF5733", // Use your desired color here (e.g., your secondary color)
        },
      },
    },
  },
});

export default darkTheme;
