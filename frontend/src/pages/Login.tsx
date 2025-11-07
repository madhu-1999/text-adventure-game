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
  Stack,
} from "@mui/material";
import { useState } from "react";
import { Link as RouterLink } from "react-router-dom";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = () => {};
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
            <Stack
              spacing={2}
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
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
              <TextField
                margin="normal"
                required
                fullWidth
                id="password"
                label="Password"
                name="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              <Button
                fullWidth
                variant="contained"
                sx={{ mt: 3, mb: 2 }}
                onClick={handleLogin}
              >
                Login
              </Button>
            </Stack>
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
