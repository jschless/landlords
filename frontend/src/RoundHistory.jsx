import React, { useState } from "react";
import {
  Box,
  Heading,
  Text,
  VStack,
  Image,
  Divider,
  HStack,
  Button,
} from "@chakra-ui/react";

function RoundHistory({ roundHistory }) {
  const [showHistory, setShowHistory] = useState(false);
  const [showWinningHandOnly, setShowWinningHandOnly] = useState(true); // Toggle for winning hand or all hands

  // Helper function to calculate total cards used in a round
  const getTotalCards = (arr) => {
    let totalCards = 0;

    arr.forEach((item) => {
      const handCards = item[1].hand_cards || [];
      const kickerCards = item[1].kicker_cards || [];

      totalCards += handCards.length + kickerCards.length;
    });

    return totalCards;
  };

  // Find the last non-zero hand in each round (the winning hand)
  const getWinningHand = (round) => {
    const validHands = round.filter(([, hand]) => hand.base > 0); // Filter hands with base > 0
    return validHands[validHands.length - 1]; // Return the last non-zero hand
  };

  return (
    <Box p={5}>
      {/* Toggle for showing round history */}
      <Button
        onClick={() => setShowHistory(!showHistory)}
        colorScheme="teal"
        mb={4}
      >
        {showHistory ? "Hide Round History" : "Show Round History"}
      </Button>

      {/* Toggle for showing all hands or just the winning hand */}
      {showHistory && (
        <>
          <Button
            onClick={() => setShowWinningHandOnly(!showWinningHandOnly)}
            colorScheme="blue"
            mb={4}
          >
            {showWinningHandOnly ? "Show All Hands" : "Show Winning Hand Only"}
          </Button>

          <VStack spacing={4} align="stretch">
            <Heading size="md" mb={4}>
              Round History
            </Heading>

            {roundHistory.map((round, roundIndex) => {
              const totalCards = getTotalCards(round);
              const [winner, winningHand] = getWinningHand(round);

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

                  {showWinningHandOnly ? (
                    // Show winning hand
                    <>
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
                    </>
                  ) : (
                    // Show all hands in the round
                    <>
                      {round.map(([player, hand], index) => (
                        <Box key={index} mb={2}>
                          <Text fontSize="md">
                            <strong>{player}'s Hand:</strong>
                          </Text>
                          <HStack spacing={2}>
                            {hand.hand_cards.map((card, cardIndex) => (
                              <Image
                                key={cardIndex}
                                src={`${process.env.PUBLIC_URL}/cards/${card}.png`}
                                alt={`Card ${card}`}
                                boxSize="50px"
                                objectFit="cover"
                              />
                            ))}
                          </HStack>
                        </Box>
                      ))}
                    </>
                  )}

                  <Text fontSize="md" mt={3}>
                    <strong>Total Cards Played:</strong> {totalCards}
                  </Text>
                  <Divider mt={3} />
                </Box>
              );
            })}
          </VStack>
        </>
      )}
    </Box>
  );
}

export default RoundHistory;
