import React from "react";
import { Badge } from "@chakra-ui/react";

interface RiskBadgeProps {
  riskLevel: number;
}

export default function RiskBadge({ riskLevel }: RiskBadgeProps) {
  let text, colorScheme;
  if (riskLevel <= 3.9) {
    text = "Baixo";
    colorScheme = "teal";
  } else if (riskLevel <= 6.9) {
    text = "Médio";
    colorScheme = "yellow";
  } else if (riskLevel <= 8.9) {
    text = "Alto";
    colorScheme = "orange";
  } else {
    text = "Crítico";
    colorScheme = "red";
  }
  return <Badge colorScheme={colorScheme}>{text}</Badge>;
}
