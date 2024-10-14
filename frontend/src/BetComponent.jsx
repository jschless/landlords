import React, { useState } from "react";
import {
  Box,
  Heading,
  Text,
  Button,
  HStack,
  useColorModeValue,
} from "@chakra-ui/react";

function BetComponent({ lastBid, submitBet }) {
  const [bet, setBet] = useState("");

  return (
    <Box
      p={4}
      bg={useColorModeValue("gray.50", "gray.800")}
      borderRadius="md"
      boxShadow="md"
      textAlign="center"
    >
      <Heading size="md" mb={4}>
        Make Your Bet:
      </Heading>
      <HStack spacing={4} mb={4} justifyContent="center">
        {/* Pass Button */}
        <Button
          onClick={() => {
            setBet("0");
            submitBet("0"); // Submit immediately on click if needed
          }}
          colorScheme="teal"
          flex="1"
          size="lg"
        >
          Pass
        </Button>

        {/* Dynamically create buttons from last_bid + 1 to 3 */}
        {[...Array(3 - lastBid)].map((_, index) => {
          const bidValue = lastBid + index + 1; // starts at last_bid + 1
          return (
            <Button
              key={bidValue}
              onClick={() => {
                setBet(String(bidValue));
                submitBet(String(bidValue)); // Submit immediately on click if needed
              }}
              colorScheme="teal"
              flex="1"
              size="lg"
            >
              {bidValue}
            </Button>
          );
        })}
      </HStack>

      {bet && (
        <Text mt={2} fontSize="sm" color="gray.500">
          You selected: {bet}
        </Text>
      )}
    </Box>
  );
}

export default BetComponent;
