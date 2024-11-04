import React, { useState } from "react";
import { Box, Button, Flex, Text } from "@chakra-ui/react";
import Card from "./Card.jsx";

function Hand({
  myCards,
  onSubmit,
  promptMove,
  isLandlord,
  username,
  current_player_username,
  visibleCards
}) {
  const [selectedCards, setSelectedCards] = useState([]);
  const [selectedKickers, setSelectedKickers] = useState([]);
  const label = isLandlord ? "Landlord" : "Peasant";
  const bg_color = isLandlord ? "yellow.300" : "purple.300";
  const border_color =
    current_player_username === username ? "green.300" : "gray.300";
  const border_width = current_player_username === username ? 8 : 1;

  // Count occurrences in visibleCards
  const visibleCardCounts = visibleCards.reduce((acc, card) => {
    acc[card] = (acc[card] || 0) + 1;
    return acc;
  }, {});

  // Filter myCards to only include the remaining instances
  const remainingMyCards = [];
  myCards.forEach(card => {
    if (visibleCardCounts[card]) {
      visibleCardCounts[card]--;
    } else {
      remainingMyCards.push(card);
    }
  });

  const handleCardClick = (e, card, index) => {
    if (e.button === 0) {
      if (e.shiftKey) {
        // If shift key is pressed, add/remove from selectedKickers list
        if (selectedKickers.some((c) => c.index === index)) {
          setSelectedKickers(selectedKickers.filter((c) => c.index !== index));
        } else {
          setSelectedKickers([...selectedKickers, { card, index }]);
        }
      } else {
        // Add/remove from selectedCards list
        if (selectedCards.some((c) => c.index === index)) {
          setSelectedCards(selectedCards.filter((c) => c.index !== index));
        } else {
          setSelectedCards([...selectedCards, { card, index }]);
        }
      }
    }
    console.log(selectedCards);
  };

  const handleSubmit = () => {
    if (selectedCards.length >= 0) {
      onSubmit(selectedCards, selectedKickers);
      setSelectedCards([]);
      setSelectedKickers([]);
    }
  };

  return (
    <Box
      position="relative"
      textAlign="center"
      borderWidth={border_width}
      borderColor={border_color}
      borderRadius="md"
      bg={bg_color}
      shadow="md"
      p={4}
    >
      <Text as="h3" fontSize="lg" fontWeight="bold" mb={2}>
        {username}
      </Text>
      <Text as="h3" fontSize="md" fontWeight="bold" mb={8}>
        {label}
      </Text>

      <Flex direction="column" justify="space-between" height="100%">
        {/* Display visible cards */}
        <Text fontSize="md" fontWeight="bold" mb={2}>
          Visible Cards
        </Text>
        <Flex direction="row" justify="center" wrap="wrap" flex="1" mb={4}>
          {visibleCards.map((card, index) => (
            <Card
              key={`visible-${index}`}
              card={card}
              index={index}
              border={
                selectedCards.some((c) => c.index === index)
                  ? "3px solid blue"
                  : selectedKickers.some((c) => c.index === index)
                    ? "3px solid orange"
                    : "none"
              }
              onClick={(e) => handleCardClick(e, card, index)}
            />
          ))}
        </Flex>

        {/* Display remaining cards */}
        <Text fontSize="md" fontWeight="bold" mb={2}>
          Other Cards
        </Text>
        <Flex direction="row" justify="center" wrap="wrap" flex="1" mb={4}>
          {remainingMyCards.map((card, index) => (
            <Card
              key={`mycard-${index}`}
              card={card}
              index={visibleCards.length+index}
              border={
                selectedCards.some((c) => c.index === visibleCards.length+index)
                  ? "3px solid blue"
                  : selectedKickers.some((c) => c.index === visibleCards.length+index)
                    ? "3px solid orange"
                    : "none"
              }
              onClick={(e) => handleCardClick(e, card, visibleCards.length+index)}
            />
          ))}
        </Flex>

        {/* Submit button positioned at the bottom */}
        {promptMove && (
          <Button onClick={handleSubmit} colorScheme="teal" alignSelf="center">
            Submit Selected Cards
          </Button>
        )}
      </Flex>
    </Box>
  );
}

export default Hand;
