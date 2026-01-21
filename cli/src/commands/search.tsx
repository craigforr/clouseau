import { Box, Text } from 'ink';

interface SearchCommandProps {
  query: string;
}

export function SearchCommand({ query }: SearchCommandProps) {
  return (
    <Box flexDirection="column">
      <Text>Searching: {query}</Text>
    </Box>
  );
}
