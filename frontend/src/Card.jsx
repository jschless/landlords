import React from "react";
import { Image, Box } from "@chakra-ui/react";

function Card({ index, card, border, onClick }) {
  return (
    <Box transition="transform 0.2s" _hover={{ transform: "scale(1.1)" }}>
      <Image
        src={`${process.env.PUBLIC_URL}/cards/${card}.png`}
        alt={`Card ${card}`}
        boxSize="60px"
        m={1}
        border={border}
        cursor="pointer"
        onClick={onClick}
      />
    </Box>
  );
}

export default Card;
