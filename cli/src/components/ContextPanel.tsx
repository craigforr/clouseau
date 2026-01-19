import { Box, Text } from 'ink';

interface ContextPanelProps {
  used: number;
  total: number;
}

export function ContextPanel({ used, total }: ContextPanelProps) {
  const percentage = ((used / total) * 100).toFixed(1);
  return (
    <Box>
      <Text>Context: {used}/{total} ({percentage}%)</Text>
    </Box>
  );
}
