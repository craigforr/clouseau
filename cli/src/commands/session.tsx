import { Box, Text } from 'ink';

interface SessionCommandProps {
  action: 'list' | 'show' | 'delete';
  sessionId?: string;
}

export function SessionCommand({ action, sessionId }: SessionCommandProps) {
  return (
    <Box flexDirection="column">
      <Text>Session {action}: {sessionId || 'all'}</Text>
    </Box>
  );
}
