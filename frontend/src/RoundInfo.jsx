import React from "react";
import {
  Box,
  Heading,
  Text,
  Stack,
  useColorModeValue,
} from "@chakra-ui/react";

function RoundInfo({ gameData }) {

  return (
    <Box
      p={4}
      borderWidth={1}
      borderRadius="md"
      m={2}
      borderColor={useColorModeValue("gray.200", "gray.700")}
      bg={useColorModeValue("white", "gray.800")}
      boxShadow="md"
    >
      <Stack spacing={2} textAlign="center">
        <Heading as="h2" size="lg">
          Current turn: {gameData.current_player_username}
        </Heading>
        <Text fontSize="md" color={useColorModeValue("gray.600", "gray.300")}>
          Current landlord: {gameData.landlord_username}
        </Text>
        <Text fontSize="md" color={useColorModeValue("gray.600", "gray.300")}>
          Bet Stakes: {gameData.bid}
        </Text>
        <Text fontSize="md" color={useColorModeValue("gray.600", "gray.300")}>
          Hand Type: {gameData.cur_round.length > 0? gameData.cur_round[0][1].string_repr: "None"}
        </Text>
      </Stack>
    </Box>
  );
}

export default RoundInfo;
