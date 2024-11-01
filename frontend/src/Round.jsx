import React from "react";
import {
  Box,
  Flex,
  Image,
  Text,
  Heading,
  Button,
  VStack,
  HStack,
  Badge,
  useClipboard,
} from "@chakra-ui/react";
import { CopyIcon } from "@chakra-ui/icons";

const Round = ({ hands, bidValue, currentPlayer }) => {
  const currentUrl = window.location.href;
  const { hasCopied, onCopy } = useClipboard(currentUrl);

  return (
    <Box textAlign="center" p={4} bg="gray.50" borderRadius="md" shadow="md" flex="3" overflowY="auto" maxHeight="600px">
      <VStack spacing={6} align="center">
        <Heading size="lg">Playing Area</Heading>

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
              <VStack spacing={1} align="center" borderWidth={1} borderColor="gray.300" borderRadius="md" p={3}>
                <Text fontWeight="bold" fontSize="md" color="gray.500">
                  Hand
                </Text>
                {hand ? (
                  <HStack spacing={1}>
                    {hand.hand_cards.map((card, i) => (
                      <Box
                        key={i}
                        p={1}
                        borderWidth={1}
                        borderColor="black"
                        borderRadius="md"
                        transition="transform 0.2s"
                        _hover={{ transform: "scale(1.1)" }}
                        bg="gray.50"
                      >
                        <Image
                          src={`${process.env.PUBLIC_URL}/cards/${card}.png`}
                          alt={`Card ${card}`}
                          boxSize="50px"
                          objectFit="cover"
                        />
                      </Box>
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
                <VStack spacing={1} align="center" borderWidth={1} borderColor="gray.300" borderRadius="md" p={3}>
                  <Text fontWeight="bold" fontSize="md" color="gray.500">
                    Kicker
                  </Text>
                  <HStack spacing={1}>
                    {hand.kicker_cards.map((card, i) => (
                      <Box
                        key={i}
                        p={1}
                        borderWidth={1}
                        borderColor="black"
                        borderRadius="md"
                        transition="transform 0.2s"
                        _hover={{ transform: "scale(1.1)" }}
                        bg="gray.50"
                      >
                        <Image
                          src={`${process.env.PUBLIC_URL}/cards/${card}.png`}
                          alt={`Card ${card}`}
                          boxSize="50px"
                          objectFit="cover"
                        />
                      </Box>
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
