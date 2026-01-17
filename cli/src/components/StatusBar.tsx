import React from 'react';
import { Box, Text } from 'ink';

interface StatusBarProps {
  status: string;
  model?: string;
}

export function StatusBar({ status, model }: StatusBarProps) {
  return (
    <Box justifyContent="space-between">
      <Text>{status}</Text>
      {model && <Text dimColor>Model: {model}</Text>}
    </Box>
  );
}
