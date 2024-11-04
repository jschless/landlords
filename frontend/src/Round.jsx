import React, { useEffect, useRef } from "react";
import { Box, Text, Heading, VStack, HStack, Badge } from "@chakra-ui/react";
import Card from "./Card.jsx";

const Round = ({ hands, bidValue, currentPlayer }) => {
  const scrollRef = useRef();

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [hands]);

  return (
    <Box
      textAlign="center"
      p={4}
      gap={20}
      bg="gray.50"
      borderRadius="md"
      shadow="md"
      flex="3"
    >
      <Heading size="lg">Playing Area</Heading>

      <VStack
        spacing={2}
        align="center"
        maxHeight="500px"
        overflowY="auto"
        scrollBehavior="smooth"
        ref={scrollRef}
      >
        {hands.map(([player, hand], index) => (
          <Box
            key={index}
            p={4}
            borderWidth={2}
            borderColor="gray.300"
            borderRadius="lg"
            boxShadow="md"
            bg="white"
            width="100%"
          >
            <HStack spacing={4} align="center">
              {/* Player Details */}
              <VStack align="flex-start" spacing={1}>
                <HStack>
                  <Badge colorScheme="blue" variant="solid" fontSize="lg">
                    {index + 1}
                  </Badge>
                  <Text fontWeight="semibold" fontSize="lg">
                    {player} {player === currentPlayer && "(Current Player)"}
                  </Text>
                </HStack>
                {bidValue && (
                  <Text fontSize="md" color="gray.600">
                    Current Bid: {bidValue}
                  </Text>
                )}
              </VStack>

              {/* Hand Display */}
              <VStack
                spacing={1}
                align="center"
                borderWidth={1}
                borderColor="gray.300"
                borderRadius="md"
                p={3}
              >
                <Text fontWeight="bold" fontSize="md" color="gray.500">
                  Hand
                </Text>
                {hand ? (
                  <HStack spacing={1}>
                    {hand.hand_cards.map((card, i) => (
                      <Card key={`handcard-${i}`} card={card} />
                    ))}
                  </HStack>
                ) : (
                  <Text fontWeight="bold" color="red.500">
                    Pass
                  </Text>
                )}
              </VStack>

              {/* Kicker Display */}
              {hand && hand.kicker_cards.length > 0 && (
                <VStack
                  spacing={1}
                  align="center"
                  borderWidth={1}
                  borderColor="gray.300"
                  borderRadius="md"
                  p={3}
                >
                  <Text fontWeight="bold" fontSize="md" color="gray.500">
                    Kicker
                  </Text>
                  <HStack spacing={1}>
                    {hand.kicker_cards.map((card, i) => (
                      <Card key={`kickercard-${i}`} card={card} />
                    ))}
                  </HStack>
                </VStack>
              )}
            </HStack>
          </Box>
        ))}
      </VStack>
    </Box>
  );
};

export default Round;
