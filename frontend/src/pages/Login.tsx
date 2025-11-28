import { LockOutlined } from "@mui/icons-material";
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
  Alert,
} from "@mui/material";
import { useReducer, useState, type ChangeEvent, type FormEvent } from "react";
import { Link as RouterLink, useNavigate } from "react-router-dom";
import type { FormAction } from "./pages.types";
import { FormActionType } from "./pages.types";

interface FormState {
  username: string;
  password: string;
  usernameError: boolean;
  passwordError: boolean;
}

const initialState: FormState = {
  // Input values
  username: "",
  password: "",

  // Validation status for basic fields
  usernameError: false,
  passwordError: false,
};

function reducer(state: FormState, action: FormAction) {
  switch (action.type) {
    case FormActionType.UPDATE: {
      const { field, value } = action.payload;
      return { ...state, [field]: value };
    }
    case FormActionType.VALIDATE: {
      const { username, password } = state;
      // Basic field checks
      const usernameValid = username.trim() !== "";
      const passwordValid = password.trim() !== "";

      return {
        ...state,
        usernameError: !usernameValid,
        passwordError: !passwordValid,
      };
    }
    case FormActionType.RESET:
      return initialState;
  }
}

const BASE_URL = import.meta.env.VITE_BASE_URL;
function Login() {
  const [state, dispatch] = useReducer(reducer, initialState);
  const [backendError, setBackendError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setBackendError("");
    dispatch({ type: FormActionType.VALIDATE });

    const isValid = state.username.trim() && state.password.trim();
    if (!isValid) return;

    try {
      const formData = new FormData();
      formData.append("username", state.username);
      formData.append("password", state.password);

      const response = await fetch(`${BASE_URL}/users/login`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      if (response.ok) {
        // Reset form fields
        dispatch({ type: "RESET_FORM" });
        //Store token
        localStorage.setItem("authToken", data.access_token);
        // Redirect to the login page
        navigate("/");
      } else {
        // Handle 400 Bad Request, 500 Internal Error, etc.
        console.log("Error", data);
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
      type: "UPDATE_FIELD",
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

            <Typography variant="h5">Login</Typography>
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
              onSubmit={handleLogin}
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
                error={state.usernameError}
                helperText={state.usernameError ? "Username is required" : ""}
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
                error={state.passwordError}
                helperText={state.passwordError ? "Password is required" : ""}
              />
              <Button
                type="submit"
                fullWidth
                variant="contained"
                sx={{ mt: 3, mb: 2 }}
              >
                Login
              </Button>
            </Box>
            <Grid container justifyContent={"flex-end"} width={"100%"} pr={2}>
              <Grid>
                <Link
                  component={RouterLink}
                  to="/register"
                  color="text.primary"
                >
                  Don't have an account? Register
                </Link>
              </Grid>
            </Grid>
          </Paper>
        </Container>
      </Box>
    </>
  );
}

export default Login;
