import React from "react";
import { Box, Flex, Image, Text, Heading } from "@chakra-ui/react";

const Round = ({ hands, bidValue, currentPlayer }) => {
  return (
    <Box
      textAlign="center"
      p={4}
      bg="gray.50"
      borderRadius="md"
      shadow="md"
      flex="3"
    >
      <Heading>Playing Area</Heading>

      <Flex direction="column" alignItems="center">
        {hands.map(([player, hand], index) => (
          <Flex key={index} alignItems="center" mb={4}>
            <Text p={0} m={2}>
              ({index + 1}) {player}
            </Text>
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
              {hand ? ( // Check if hand is not null
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
              ) : (
                <Text fontWeight="bold" color="red.500"> {/* Display "Pass" if hand is null */}
                  Pass
                </Text>
              )}
            </Flex>
            <Box width="20px" /> {/* Spacer */}
            {/* Conditionally render the kicker section if there are kicker cards */}
            {hand && hand.kicker_cards.length > 0 && ( // Check if hand is not null before rendering kicker cards
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
