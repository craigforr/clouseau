import { Box, Text } from 'ink';

interface ConfigCommandProps {
  action: 'show' | 'edit' | 'reset';
}

export function ConfigCommand({ action }: ConfigCommandProps) {
  return (
    <Box flexDirection="column">
      <Text>Config {action}</Text>
    </Box>
  );
}
