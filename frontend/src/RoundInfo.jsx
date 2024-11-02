import React, { useEffect } from "react";
import {
  Box,
  Heading,
  Text,
  Stack,
  Flex,
  useColorModeValue,
  Image,
} from "@chakra-ui/react";
import { motion, useAnimation } from "framer-motion";
import Card from "./Card.jsx";

const MotionText = motion.create(Text);

function RoundInfo({ gameData }) {
  const controls = useAnimation();
  const lastHand = gameData.cur_round[gameData.cur_round.length - 1]?.[1];

  useEffect(() => {
    controls.start({
      scale: [1, 1.3, 1],
      transition: { duration: 1.5 },
    });
  }, [gameData.bid, controls]);

  return (
    <Box
      p={6}
      borderWidth={1}
      borderRadius="lg"
      borderColor={useColorModeValue("gray.300", "gray.600")}
      bg={useColorModeValue("white", "gray.700")}
      boxShadow="lg"
      maxWidth="600px"
      textAlign="center"
      m="auto"
    >
      <Stack spacing={4}>
        <MotionText
          fontSize="2xl"
          fontWeight="bold"
          color={useColorModeValue("blue.500", "blue.300")}
          animate={controls}
        >
          Current Bet: {gameData.bid}
        </MotionText>

        <Box>
          <Heading
            as="h3"
            size="md"
            mb={2}
            color={useColorModeValue("gray.600", "gray.300")}
          >
            Hand to Beat:
          </Heading>
          <Flex justify="center" gap={2}>
            {lastHand?.hand_cards?.map((card, i) => (
                <Card key={i} card={card}/>
            ))}
          </Flex>
        </Box>
      </Stack>
    </Box>
  );
}

export default RoundInfo;
