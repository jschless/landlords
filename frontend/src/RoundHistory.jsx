import React, { useState } from "react";
import { Box, Heading, Text, VStack, Image, Divider, HStack, Button } from "@chakra-ui/react";

function RoundHistory({ roundHistory }) {
  const [showHistory, setShowHistory] = useState(true);

  // Helper function to calculate total cards used in a round
  const getTotalCards = (hand) => {
    return hand.hand_cards.length + hand.kicker_cards.length;
  };

  // Find the last non-zero hand in each round
  const getWinningHand = (round) => {
    const validHands = round.filter(([, hand]) => hand.base > 0); // Filter hands with a base > 0
    return validHands[validHands.length - 1]; // Return the last non-zero hand
  };

  return (
    <Box p={5}>
      {/* Toggle Button */}
      <Button
        onClick={() => setShowHistory(!showHistory)}
        colorScheme="teal"
        mb={4}
      >
        {showHistory ? "Hide Round History" : "Show Round History"}
      </Button>

      {/* Conditionally render the RoundHistory based on the toggle state */}
      {showHistory && (
        <VStack spacing={4} align="stretch">
          <Heading size="md" mb={4}>
            Round History
          </Heading>
          {roundHistory.map((round, roundIndex) => {
            const [winner, winningHand] = getWinningHand(round);
            const totalCards = getTotalCards(winningHand);

            return (
              <Box
                key={roundIndex}
                p={4}
                borderWidth="1px"
                borderRadius="md"
                bg="gray.50"
                boxShadow="sm"
                width="100%"
              >
                <Heading size="sm" mb={2}>
                  Round {roundIndex + 1}
                </Heading>
                <Text fontSize="md">
                  <strong>Winner:</strong> {winner}
                </Text>

                <Text fontSize="md" mb={2}>
                  <strong>Winning Hand:</strong>
                </Text>
                <HStack spacing={2}>
                  {winningHand.hand_cards.map((card, cardIndex) => (
                    <Image
                      key={cardIndex}
                      src={`${process.env.PUBLIC_URL}/cards/${card}.png`}
                      alt={`Card ${card}`}
                      boxSize="50px"
                      objectFit="cover"
                    />
                  ))}
                </HStack>

                <Text fontSize="md" mt={3}>
                  <strong>Total Cards Played:</strong> {totalCards}
                </Text>
                <Divider mt={3} />
              </Box>
            );
          })}
        </VStack>
      )}
    </Box>
  );
}

export default RoundHistory;
