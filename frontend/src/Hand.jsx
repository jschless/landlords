import React, { useState } from "react";
import { Box, Image, Button, Flex, Text } from "@chakra-ui/react";

function Hand({ myCards, onSubmit, promptMove, isLandlord }) {
  const [selectedCards, setSelectedCards] = useState([]);
  const [selectedKickers, setSelectedKickers] = useState([]);
  const label = isLandlord ? "Landlord" : "Peasant";
  const bg_color = isLandlord ? "yellow.300" : "purple.300";

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
      borderWidth={1}
      borderColor="gray.300"
      borderRadius="md"
      bg={bg_color}
      shadow="md"
      p={4}
    >
      <Text as="h3" fontSize="lg" fontWeight="bold" mb={4}>
        {label}
      </Text>

      <Flex
        direction="column"
        justify="space-between"
        height="100%"
      >
        {/* Card container with horizontal scrolling */}
        <Flex
          direction="row"
          justify="center"
          wrap="wrap"
          flex="1"
          mb={4}
        >
          {myCards.map((card, index) => (
            <Image
              key={index}
              src={`${process.env.PUBLIC_URL}/cards/${card}.png`}
              alt={`Card ${card}`}
              boxSize="80px"
              m={2}
              border={
                selectedCards.some((c) => c.index === index)
                  ? "3px solid blue"
                  : selectedKickers.some((c) => c.index === index)
                    ? "3px solid orange"
                    : "none"
              }
              cursor="pointer"
              onClick={(e) => handleCardClick(e, card, index)}
            />
          ))}
        </Flex>

        {/* Submit button positioned at the bottom */}
        {promptMove && (
          <Button
            onClick={handleSubmit}
            colorScheme="teal"
            alignSelf="center"
          >
            Submit Selected Cards
          </Button>
        )}
      </Flex>
    </Box>
  );
}

export default Hand;
