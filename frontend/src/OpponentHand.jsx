import React from "react";
import { Box, Flex, Image, Text } from "@chakra-ui/react";
import Card from "./Card.jsx";
function OpponentHand({
  username,
  exposedCards,
  nCards,
  landlord_username,
  current_player_username,
}) {
  const label = landlord_username === username ? "Landlord" : "Peasant";
  const bg_color = landlord_username === username ? "yellow.300" : "purple.300";

  const border_color =
    current_player_username === username ? "green.300" : "gray.300";
  const border_width = current_player_username === username ? 8 : 1;
  return (
    <Box
      textAlign="center"
      my={3}
      borderWidth={border_width}
      borderColor={border_color}
      borderRadius="md"
      bg={bg_color}
      shadow="md"
      maxWidth="200px"
      p={3} // Padding for some space inside the box
      transition="0.2s" // Transition for hover effects
      _hover={{ shadow: "lg", bg: "gray.50" }} // Hover effect
      flex="1"
    >
      <Flex
        direction="column" // Change direction to column
        alignItems="center" // Center-align the items
      >
        <Text as="h3" fontSize="lg" fontWeight="bold" mb={2}>
          {username}
        </Text>
        <Text as="h3" fontSize="md" fontWeight="bold" mb={8}>
          {label}
        </Text>

        {exposedCards.map((card, index) => (
            <Card index={index} card={card}/>
        ))}
        <Card index={99} card={"back-black"}/>
        <Text fontSize="lg" fontWeight="bold">
          {nCards} left
        </Text>
      </Flex>
    </Box>
  );
}

export default OpponentHand;
