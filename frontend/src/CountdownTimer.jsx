import { Box, Text, Badge } from "@chakra-ui/react";

function CountdownTimer({ promptMove, moveTimer }) {
  return (
    <>
      {promptMove && (
        <Box
          display="flex"
          alignItems="center"
          justifyContent="center"
          padding="20px"
          backgroundColor="teal.500"
          borderRadius="md"
          boxShadow="lg"
          color="white"
          width="200px"
          mx="auto"
        >
          <Text fontSize="xl" fontWeight="bold">
            Time left:
          </Text>
          <Badge ml={3} fontSize="2xl" colorScheme="yellow" variant="solid">
            {moveTimer}
          </Badge>
        </Box>
      )}
    </>
  );
}

export default CountdownTimer;
