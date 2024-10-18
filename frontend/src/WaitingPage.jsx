import React from "react";
import {
  Box,
  Heading,
  Text,
  List,
  ListItem,
  Container,
  Stack,
  useColorModeValue,
} from "@chakra-ui/react";

function WaitingPage({ gameData }) {
  return (
    <Container maxW="container.sm" p={6} centerContent>
      <Stack spacing={6} align="center" textAlign="center">
        <Heading as="h1" size="xl">
          Game Lobby: {gameData.game_id}
        </Heading>
        <Text fontSize="lg" color={useColorModeValue("gray.600", "gray.300")}>
          Waiting for {2 - gameData.players.length} player
          {gameData.players.length === 1 ? "" : "s"} to join. Here's who's
          currently here:
        </Text>
        <Box
          borderWidth={1}
          borderRadius="md"
          borderColor={useColorModeValue("gray.200", "gray.700")}
          p={4}
          bg={useColorModeValue("white", "gray.800")}
          width="full"
        >
          <List spacing={3} textAlign="left">
            <ListItem>
              {/* <Text fontWeight="bold">You:</Text> */}
              {gameData.username}
            </ListItem>
            {gameData.players.map((player, index) => (
              <ListItem key={index} pl={4}>
                {player.username}
              </ListItem>
            ))}
          </List>
        </Box>
      </Stack>
    </Container>
  );
}

export default WaitingPage;
