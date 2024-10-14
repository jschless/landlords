import React from "react";
import { Box, Flex, Image, Text, Heading } from "@chakra-ui/react";

const Round = ({ hands, bidValue, handType, currentPlayer }) => {
  return (
    <Box textAlign="center" p={4} bg="gray.50" borderRadius="md" shadow="md">
      {/* Header displaying bid value, hand type, and current player's turn */}
      <Box mb={4}>
        <Heading as="h4" size="md" color="teal.500">
          Bid Value: {bidValue}
        </Heading>
        <Text fontSize="lg" fontWeight="bold">
          Hand Type: {handType}
        </Text>
        <Text fontSize="lg" fontWeight="bold" color="blue.500">
          It's {currentPlayer}'s turn!
        </Text>
      </Box>

      <Flex direction="column" alignItems="center">
        {hands.map((hand, index) => (
          <Flex key={index} alignItems="center" mb={4}>
            <Flex
              direction="column"
              alignItems="center"
              borderWidth={1}
              borderColor="gray.300"
              borderRadius="md"
              p={2}
              mr={4}
            >
              <Text fontWeight="bold" mb={2}>
                Hand
              </Text>
              <Flex direction="row" justifyContent="center">
                {hand.hand_cards.map((card, i) => (
                  <Box
                    key={i}
                    p={1}
                    borderWidth={1}
                    borderColor="black"
                    borderRadius="md"
                    mx={1}
                    transition="transform 0.2s"
                    _hover={{ transform: "scale(1.1)" }}
                  >
                    <Image
                      src={`${process.env.PUBLIC_URL}/cards/${card}.png`}
                      alt={`Card ${card}`}
                      boxSize="50px"
                      objectFit="cover"
                    />
                  </Box>
                ))}
              </Flex>
            </Flex>
            <Box width="20px" /> {/* Spacer */}

            {/* Conditionally render the kicker section if there are kicker cards */}
            {hand.kicker_cards.length > 0 && (
              <Flex
                direction="column"
                alignItems="center"
                borderWidth={1}
                borderColor="gray.300"
                borderRadius="md"
                p={2}
              >
                <Text fontWeight="bold" mb={2}>
                  Kicker
                </Text>
                <Flex direction="row" justifyContent="center">
                  {hand.kicker_cards.map((card, i) => (
                    <Box
                      key={i}
                      p={1}
                      borderWidth={1}
                      borderColor="black"
                      borderRadius="md"
                      mx={1}
                      transition="transform 0.2s"
                      _hover={{ transform: "scale(1.1)" }}
                    >
                      <Image
                        src={`${process.env.PUBLIC_URL}/cards/${card}.png`}
                        alt={`Card ${card}`}
                        boxSize="50px"
                        objectFit="cover"
                      />
                    </Box>
                  ))}
                </Flex>
              </Flex>
            )}
          </Flex>
        ))}
      </Flex>
    </Box>
  );
};

export default Round;
