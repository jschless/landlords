import React from "react";
import {
  Flex,
  ButtonGroup,
  Button,
  Stack,
  Box,
  Heading,
} from "@chakra-ui/react";
import Card from "./Card.jsx";

const CardMoveButtons = ({ possibleMoves, handleMove }) => {
  return (
    <>
      <Heading align="center">Recommended Moves</Heading>
      <Flex width="100%" justify="center" wrap="wrap">
        <ButtonGroup spacing={2}>
          {possibleMoves.map((move, index) => {
            const handCardImages = move.hand_cards.map((card, outerIndex) => (
              <Card key={`handcard-${outerIndex}-${index}`} card={card} />
            ));

            const kickerCardImages = move.kicker_cards.map(
              (card, outerIndex) => (
                <Card key={`kickercard-${outerIndex}-${index}`} card={card} />
              ),
            );

            return (
              <Button
                key={`button-${index}`}
                onClick={() => handleMove(move)}
                marginY={2}
              >
                <Stack direction="row" spacing={2}>
                  {handCardImages}
                </Stack>
                {kickerCardImages.length > 0 && <Box>{kickerCardImages}</Box>}
              </Button>
            );
          })}
        </ButtonGroup>
      </Flex>
    </>
  );
};
export default CardMoveButtons;
