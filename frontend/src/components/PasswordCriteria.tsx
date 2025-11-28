import { CheckCircleOutline, HighlightOff } from "@mui/icons-material";
import { Typography, Box } from "@mui/material";
import type { ReactNode } from "react";
type Props = {
  isValid: boolean;
  children: ReactNode;
};
export default function PasswordCriteria({ isValid, children }: Props) {
  const IconComponent = isValid ? CheckCircleOutline : HighlightOff;
  return (
    <Box sx={{ display: "flex", alignItems: "center", mt: 0.5 }}>
      <IconComponent color={isValid ? "success" : "error"} />
      <Typography
        variant="caption"
        color={isValid ? "success.main" : "error.main"}
        sx={{ marginLeft: 2 }}
      >
        {children}
      </Typography>
    </Box>
  );
}
