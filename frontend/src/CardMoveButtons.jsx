import React from 'react';
import { Flex, ButtonGroup, Button, Image, Stack, Box, Heading} from '@chakra-ui/react';

const CardMoveButtons = ({ possibleMoves, handleMove }) => {
    return (
        <>
          <Heading align="center">Pick a card</Heading>
        <Flex width="100%" justify="center" wrap="wrap"> {/* Centered */}
            <ButtonGroup spacing={4}> {/* Added spacing for buttons */}
                {possibleMoves.map((move, index) => {
                    const handCardImages = move.hand_cards.map((card, index) => (
                        <Image
                          key={`${card}-${index}`}
                            src={`${process.env.PUBLIC_URL}/cards/${card}.png`}
                            alt={`Card ${card}`} 
                            boxSize="50px" 
                            margin="0 2" 
                        />
                    ));

                    const kickerCardImages = move.kicker_cards.map((card, index) => (
                        <Image 
                          key={`${card}-${index}`}
                          src={`${process.env.PUBLIC_URL}/cards/${card}.png`}
                            alt={`Kicker ${card}`} 
                            boxSize="40px" 
                            margin="0 2" 
                        />
                    ));

                    return (
                        <Button
                          key={index}
                            onClick={() => handleMove(move)}
                            marginY={2} 
                        >
                            <Stack direction="row" spacing={2}>
                                {handCardImages}
                            </Stack>
                            {kickerCardImages.length > 0 && (
                                <Box>
                                    {kickerCardImages}
                                </Box>
                            )}
                        </Button>
                    );
                })}
            </ButtonGroup>
        </Flex>
        </>
    );
};

export default CardMoveButtons;
