import React, { useState } from "react";
import {
  Box,
  Heading,
  Text,
  Radio,
  RadioGroup,
  HStack,
  Button,
  useColorModeValue,
} from "@chakra-ui/react";

function BetComponent({ lastBid, submitBet }) {
  const [bet, setBet] = useState("");

  return (
    <Box p={4} bg={useColorModeValue("gray.50", "gray.800")} borderRadius="md" boxShadow="md">
      <Heading size="md" mb={4} textAlign="center">
        Make Your Bet:
      </Heading>
      <RadioGroup onChange={setBet} value={bet}>
        <HStack spacing={4} mb={4}>
          <Radio value="0" colorScheme="teal">
            Pass
          </Radio>
          {/* Dynamically create radio buttons from last_bid + 1 to 3 */}
          {[...Array(3 - lastBid)].map((_, index) => {
            const bidValue = lastBid + index + 1; // starts at last_bid + 1
            return (
              <Radio key={bidValue} value={String(bidValue)} colorScheme="teal">
                {bidValue}
              </Radio>
            );
          })}
        </HStack>
      </RadioGroup>
      <Button
        onClick={() => submitBet(bet)}
        colorScheme="teal"
        width="full"
        isDisabled={!bet} // Disable button if no bet is selected
      >
        Submit Bet
      </Button>
      {bet && (
        <Text mt={2} fontSize="sm" color="gray.500" textAlign="center">
          You selected: {bet}
        </Text>
      )}
    </Box>
  );
}

export default BetComponent;
