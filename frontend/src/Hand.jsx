import React, { useState } from "react";
import { Box, Image, Button, Flex } from "@chakra-ui/react";

function Hand({ myCards, onSubmit, promptMove }) {
  const [selectedCards, setSelectedCards] = useState([]);
  const [selectedKickers, setSelectedKickers] = useState([]);

  const handleCardClick = (e, card, index) => {
    if (e.button === 0) {
      // Left-click
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
      console.log("submit happened", selectedCards, selectedKickers);
      onSubmit(selectedCards, selectedKickers);
      setSelectedCards([]);
      setSelectedKickers([]);
    }
  };

  return (
    <Box position="relative">
      {/* Card display */}
      <Flex
        justifyContent="center"
        p={20}
        mb={20} // Add margin bottom for spacing
        width="100%"
        wrap="wrap"
      >
        {myCards.map((card, index) => (
          <Image
            key={index}
            src={`${process.env.PUBLIC_URL}/cards/${card}.png`}
            alt={`Card ${card}`}
            boxSize="80px"
            m={1}
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

      {/* Submit button */}
      {promptMove && (
        <Button
          onClick={handleSubmit}
          mt={4}
          p={4}
          colorScheme="teal"
          position="absolute"
          bottom={-10}
          left="50%"
          transform="translateX(-50%)"
        >
          Submit Selected Cards
        </Button>
      )}
    </Box>
  );
}

export default Hand;
