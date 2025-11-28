import {
  Avatar,
  Box,
  Button,
  Container,
  CssBaseline,
  Grid,
  TextField,
  Typography,
  Link,
  Paper,
  FormHelperText,
  Alert,
} from "@mui/material";
import { LockOutlined } from "@mui/icons-material";
import { useReducer, useState, type ChangeEvent, type FormEvent } from "react";
import { Link as RouterLink, useNavigate } from "react-router-dom";
import PasswordCriteria from "../components/PasswordCriteria";
import type { FormAction } from "./pages.types";
import { FormActionType } from "./pages.types";
interface FormState {
  username: string;
  email: string;
  password: string;
  confirmPassword: string;

  usernameError: boolean;
  emailError: boolean;
  confirmPasswordError: boolean;

  isValidLength: boolean;
  hasUppercase: boolean;
  hasLowercase: boolean;
  hasDigit: boolean;
  hasSpecialChar: boolean;

  showErrors: boolean;
}

const initialState: FormState = {
  // Input values
  username: "",
  email: "",
  password: "",
  confirmPassword: "",

  // Validation status for basic fields
  usernameError: false,
  emailError: false,
  confirmPasswordError: false,

  // Validation status for password criteria
  isValidLength: false,
  hasUppercase: false,
  hasLowercase: false,
  hasDigit: false,
  hasSpecialChar: false,

  // Global form states
  showErrors: false,
};

function reducer(state: FormState, action: FormAction) {
  switch (action.type) {
    case "UPDATE_FIELD": {
      const { field, value } = action.payload;
      const newState = { ...state, [field]: value };

      // Re-validate password criteria if the updated field is 'password'
      if (field === "password") {
        newState.isValidLength = value.length >= 8;
        newState.hasUppercase = /[A-Z]/.test(value);
        newState.hasLowercase = /[a-z]/.test(value);
        newState.hasDigit = /[0-9]/.test(value);
        newState.hasSpecialChar = /[!@#$%^&*+=]/.test(value);
      }
      return newState;
    }
    case "VALIDATE_FORM": {
      const { username, email, password, confirmPassword } = state;

      // Basic field checks
      const usernameValid = username.trim() !== "";
      const emailValid = email.trim() !== "";
      // Password checks based on current state booleans
      const passwordValid =
        state.isValidLength &&
        state.hasUppercase &&
        state.hasLowercase &&
        state.hasDigit &&
        state.hasSpecialChar;
      //Confirm passwords match
      const passwordMatch = password === confirmPassword && passwordValid;

      return {
        ...state,
        showErrors: true,
        usernameError: !usernameValid,
        emailError: !emailValid,
        confirmPasswordError: !passwordMatch,
        isFormValid: usernameValid && emailValid && passwordValid,
      };
    }
    case "RESET_FORM":
      return initialState;
  }
}
const BASE_URL = import.meta.env.VITE_BASE_URL;
const Register = () => {
  const [state, dispatch] = useReducer(reducer, initialState);
  const [backendError, setBackendError] = useState("");
  const navigate = useNavigate();

  const handleRegister = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setBackendError("");
    dispatch({ type: FormActionType.VALIDATE });

    const isValid =
      state.username.trim() &&
      state.email.trim() &&
      state.hasDigit &&
      state.isValidLength &&
      state.hasLowercase &&
      state.hasUppercase &&
      state.hasSpecialChar &&
      state.password === state.confirmPassword;

    if (!isValid) {
      return;
    }

    try {
      const response = await fetch(`${BASE_URL}/users/register`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          id: -1,
          username: state.username,
          email: state.email,
          password: state.password,
        }),
      });

      const data = await response.json();
      if (response.ok) {
        // Reset form fields
        dispatch({ type: FormActionType.RESET });
        // Redirect to the login page
        navigate("/login");
      } else {
        // Handle 400 Bad Request, 500 Internal Error, etc.
        let errorMsg = "An unknown error occurred";

        if (data && typeof data.detail === "string") {
          errorMsg = data.detail;
        } else {
          errorMsg = data.detail[0].msg;
        }

        setBackendError(errorMsg);
      }
    } catch (error) {
      // Handle network errors (e.g., backend server is down)
      console.error("Network error:", error);
      setBackendError("Could not connect to the backend server");
    }
  };

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    dispatch({
      type: FormActionType.UPDATE,
      payload: { field: e.target.name, value: e.target.value },
    });
  };

  return (
    <>
      <CssBaseline />
      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          minHeight: "100vh",
          bgcolor: "background.default",
        }}
      >
        <Container maxWidth="xs">
          <Paper
            elevation={3}
            sx={{
              pt: 2,
              pb: 2,
              display: "flex",
              flexDirection: "column",
              alignSelf: "center",
              alignItems: "center",
            }}
          >
            <Avatar sx={{ m: 1, bgcolor: "primary.light" }}>
              <LockOutlined />
            </Avatar>

            <Typography variant="h5">Register</Typography>
            {backendError && (
              <Alert
                severity="error"
                sx={{ width: "100%", mt: 2, whiteSpace: "pre-wrap" }}
              >
                {backendError}
              </Alert>
            )}
            <Box
              component="form"
              onSubmit={handleRegister}
              sx={{
                p: 4,
                width: "100%",
                justifyContent: "center",
                alignItems: "center",
              }}
            >
              <TextField
                margin="normal"
                required
                fullWidth
                id="username"
                label="Username"
                name="username"
                autoFocus
                value={state.username}
                onChange={handleChange}
                error={state.usernameError && state.showErrors}
                helperText={
                  state.usernameError && state.showErrors
                    ? "Username is required"
                    : ""
                }
              />
              <TextField
                margin="normal"
                required
                fullWidth
                id="email"
                label="Email Address"
                name="email"
                value={state.email}
                onChange={handleChange}
                error={state.emailError && state.showErrors}
                helperText={
                  state.emailError && state.showErrors
                    ? "Email is required"
                    : ""
                }
              />
              <TextField
                margin="normal"
                required
                fullWidth
                id="password"
                label="Password"
                name="password"
                type="password"
                value={state.password}
                onChange={handleChange}
                error={
                  state.showErrors &&
                  (!state.isValidLength ||
                    !state.hasSpecialChar ||
                    !state.hasUppercase ||
                    !state.hasLowercase ||
                    !state.hasDigit)
                }
              />
              <TextField
                margin="normal"
                required
                fullWidth
                id="confirmPassword"
                label="Confirm Password"
                name="confirmPassword"
                type="password"
                value={state.confirmPassword}
                onChange={handleChange}
                error={state.showErrors && state.confirmPasswordError}
                helperText={
                  state.showErrors && state.confirmPasswordError
                    ? "Passwords do not match"
                    : ""
                }
              />
              <Box sx={{ mt: 2, ml: 1 }}>
                <FormHelperText>
                  Password must meet following criteria:
                </FormHelperText>
                <PasswordCriteria isValid={state.isValidLength}>
                  Minimum 8 characters long
                </PasswordCriteria>
                <PasswordCriteria isValid={state.hasUppercase}>
                  Atleast one uppercase character
                </PasswordCriteria>
                <PasswordCriteria isValid={state.hasLowercase}>
                  Atleast one lowercase character
                </PasswordCriteria>
                <PasswordCriteria isValid={state.hasDigit}>
                  Atleast one digit (0-9)
                </PasswordCriteria>
                <PasswordCriteria isValid={state.hasSpecialChar}>
                  Atleast one special character (@#$%^&+=)
                </PasswordCriteria>
              </Box>
              <Button
                type="submit"
                fullWidth
                variant="contained"
                sx={{ mt: 3, mb: 2 }}
              >
                Register
              </Button>
            </Box>
            <Grid container justifyContent={"flex-end"} width={"100%"} pr={2}>
              <Grid>
                <Link component={RouterLink} to="/login" color="text.primary">
                  Already have an account? Login
                </Link>
              </Grid>
            </Grid>
          </Paper>
        </Container>
      </Box>
    </>
  );
};

export default Register;
