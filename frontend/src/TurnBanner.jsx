import React from "react";
import { Box, Text } from "@chakra-ui/react";

function TurnBanner({ gameDataUid, uid }) {
  // Check if it's the player's turn
  const isYourTurn = gameDataUid === uid;

  return (
    <>
      {isYourTurn && (
        <Box
          bg="green.200" // Light green background
          p={2}          // Padding to make the banner stand out
          textAlign="center"
          width="100%"    // Full-width banner
        >
          <Text fontSize="lg" fontWeight="bold" color="black">
            It's your turn!
          </Text>
        </Box>
      )}
    </>
  );
}

export default TurnBanner;
