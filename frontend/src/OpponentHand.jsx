import React from "react";
import { Box, Flex, Image, Text } from "@chakra-ui/react";

function OpponentHand({ username, exposedCards, nCards }) {
  return (
    <Box
      textAlign="center"
      my={3}
      borderWidth={1}
      borderColor="gray.300"
      borderRadius="md"
      bg="white"
      shadow="md"
      maxWidth="200px"
      p={3} // Padding for some space inside the box
      transition="0.2s" // Transition for hover effects
      _hover={{ shadow: "lg", bg: "gray.50" }} // Hover effect
    >
      <Text as="h3" fontSize="lg" fontWeight="bold" mb={8}>
        {username}
      </Text>
      <Flex
        direction="column" // Change direction to column
        alignItems="center" // Center-align the items
      >
        {exposedCards.map((card, index) => (
          <Image
            key={index}
            src={`${process.env.PUBLIC_URL}/cards/${card}.png`}
            alt={`Card ${card}`}
            boxSize="80px"
            objectFit="cover"
            mb={1} // Margin bottom for spacing between cards
            borderRadius="md" // Rounded corners for the cards
            transition="transform 0.2s" // Transition for hover effects on cards
            _hover={{ transform: "scale(1.1)" }} // Card hover effect
          />
        ))}
        <Image
          src={`${process.env.PUBLIC_URL}/cards/back-black.png`}
          alt="Number of cards"
          boxSize="80px"
          objectFit="cover"
          mb={1} // Margin bottom for spacing
          borderRadius="md" // Rounded corners for the back card
          transition="transform 0.2s"
          _hover={{ transform: "scale(1.1)" }} // Card hover effect
        />
        <Text fontSize="lg" fontWeight="bold">
          {nCards} left
        </Text>
      </Flex>
    </Box>
  );
}

export default OpponentHand;
