import React from "react";
import {
  Flex,
  ButtonGroup,
  Button,
  Stack,
  Box,
  Text,
  Heading,
} from "@chakra-ui/react";
import Card from "./Card.jsx";

const CardMoveButtons = ({ possibleMoves, handleMove }) => {
  return (
    <>
      <Stack direction="column" gap={2}>
        <Heading align="center">Recommended Moves</Heading>
        <Flex width="100%" justify="center" wrap="wrap">
          <ButtonGroup spacing={4}>
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
                  marginY={6}
                  bg="blue.300"
                  height="100px"
                >
                  <Stack direction="column">
                    <Stack direction="row" spacing={0}>
                      {handCardImages}

                      {kickerCardImages.length > 0 && (
                        <Box>{kickerCardImages}</Box>
                      )}
                    </Stack>
                    <Text>{move.win_rate}</Text>
                  </Stack>
                </Button>
              );
            })}
          </ButtonGroup>
        </Flex>
      </Stack>
    </>
  );
};
export default CardMoveButtons;
