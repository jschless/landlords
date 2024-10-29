import React from "react";
import { useNavigate } from "react-router-dom";
import {
  Box,
  Button,
  Container,
  Heading,
  Text,
  Stack,
  useColorModeValue,
} from "@chakra-ui/react";

function Home() {
  const navigate = useNavigate();

  const createGame = async () => {
    try {
      const response = await fetch("http://134.122.123.229:8000/create_game", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error("Failed to create game");
      }

      const data = await response.json();
      const gameId = data.game_id;
      navigate(`/game/${gameId}`);
    } catch (error) {
      console.error("Error creating game:", error);
    }
  };

  return (
    <Container maxW="container.lg" p={4} centerContent>
      <Stack spacing={6} align="center" textAlign="center">
        <Heading as="h1" size="2xl" mb={4}>
          Welcome to the Game!
        </Heading>
        <Text fontSize="lg" color={useColorModeValue("gray.600", "gray.300")}>
          This is an interactive card game platform where you can create and
          join games with friends or other players. Test your skills, enjoy the
          competition, and have fun!
        </Text>
        <Button
          onClick={createGame}
          colorScheme="teal"
          size="lg"
          px={8}
          variant="solid"
        >
          Create Game
        </Button>
      </Stack>
      {/* Optional styling for better aesthetics */}
      <Box
        position="absolute"
        bottom="20px"
        left="50%"
        transform="translateX(-50%)"
        color={useColorModeValue("gray.500", "gray.400")}
        fontSize="sm"
      ></Box>
    </Container>
  );
}

export default Home;
