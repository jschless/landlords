import React, { useEffect } from "react";
import { Box, Heading, Text, Stack, useColorModeValue } from "@chakra-ui/react";
import { motion, useAnimation } from "framer-motion";

const MotionText = motion(Text);

function RoundInfo({ gameData }) {
  const controls = useAnimation();

  useEffect(() => {
    controls.start({
      scale: [1, 1.5, 1],
      transition: { duration: 2 },
    });
  }, [gameData.bid, controls]);

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
        <MotionText
          fontSize="md"
          color={useColorModeValue("gray.600", "gray.300")}
          animate={controls}
        >
          Bet Stakes: {gameData.bid}
        </MotionText>
        <Text fontSize="md" color={useColorModeValue("gray.600", "gray.300")}>
          Hand Type:{" "}
          {gameData.cur_round.length > 0
            ? gameData.cur_round[0][1].string_repr
            : "None"}
        </Text>
      </Stack>
    </Box>
  );
}

export default RoundInfo;
