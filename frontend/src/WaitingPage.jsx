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
  IconButton,
  useClipboard,
  Tooltip,
  HStack,
} from "@chakra-ui/react";

import { CopyIcon } from "@chakra-ui/icons";

function WaitingPage({ gameData }) {
  const currentUrl = window.location.href;
  const { hasCopied, onCopy } = useClipboard(currentUrl);

  return (
    <Container maxW="container.sm" p={6} centerContent>
      <Stack spacing={6} align="center" textAlign="center">
        <Heading size="lg">Dough Dizhu Lobby</Heading>
        <Heading size="sm">Game ID: {gameData.game_id}</Heading>

        <HStack spacing={4} align="center">
          <Text fontSize="lg" color={useColorModeValue("gray.600", "gray.300")}>
            Click to copy and share the link with a friend!
          </Text>
          <Tooltip label={hasCopied ? "Copied!" : "Copy link"} fontSize="md">
            <IconButton
              icon={<CopyIcon />}
              onClick={onCopy}
              aria-label="Copy game link"
              variant="outline"
              colorScheme="teal"
            />
          </Tooltip>
        </HStack>

        <Text fontSize="lg" color={useColorModeValue("gray.600", "gray.300")}>
          Waiting for {2 - gameData.players.length} player
          {gameData.players.length === 1 ? "" : "s"} to join. Here’s who’s
          currently here:
        </Text>

        <Box
          borderWidth={2}
          borderRadius="md"
          borderColor={useColorModeValue("gray.300", "gray.600")}
          p={4}
          bg={useColorModeValue("white", "gray.900")}
          width="full"
          boxShadow="lg"
        >
          <List spacing={3} textAlign="left">
            <ListItem fontWeight="bold">1. {gameData.username} (you)</ListItem>
            {gameData.players.map((player, index) => (
              <ListItem key={index} fontWeight="medium">
                {index + 2}. {player.username}
              </ListItem>
            ))}
          </List>
        </Box>
      </Stack>
    </Container>
  );
}

export default WaitingPage;
