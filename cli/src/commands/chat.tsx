import React from 'react';
import { Box, Text } from 'ink';

interface ChatCommandProps {
  sessionId?: string;
}

export function ChatCommand({ sessionId }: ChatCommandProps) {
  return (
    <Box flexDirection="column">
      <Text>Chat Session: {sessionId || 'new'}</Text>
    </Box>
  );
}
