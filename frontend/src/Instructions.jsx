import React from "react";
import { Box, Tooltip, Icon, Text, VStack, HStack } from "@chakra-ui/react";
import { InfoOutlineIcon } from "@chakra-ui/icons";
import { FaMousePointer } from "react-icons/fa"; // Additional icon for mouse instructions
import { BsFillShiftFill } from "react-icons/bs"; // Shift icon for extra clarity

const Instructions = () => {
  return (
    <Tooltip
      label={
        <VStack align="start" spacing={3}>
          <Text fontSize="lg" fontWeight="bold" color="teal.300">
            How to Play
          </Text>
          <HStack>
            <Icon as={FaMousePointer} boxSize={4} color="teal.500" />
            <Text fontSize="md">Right-click: Select a card for hand</Text>
          </HStack>
          <HStack>
            <Icon as={BsFillShiftFill} boxSize={4} color="teal.500" />
            <Icon as={FaMousePointer} boxSize={4} color="teal.500" />
            <Text fontSize="md">
              Shift + Right-click: Select a card for discard
            </Text>
          </HStack>
          <Text fontSize="md">
            The peasants are in purple, and the landlord is in yellow.
          </Text>
          <Text fontSize="md">
            When it's your turn, you can click a pre-made move to auto-submit
            that move.
          </Text>
        </VStack>
      }
      bg="gray.800"
      color="white"
      borderRadius="md"
      p={4}
      hasArrow
      placement="right"
      fontSize="md"
    >
      <Box display="flex" alignItems="center" cursor="pointer">
        <Icon
          as={InfoOutlineIcon}
          boxSize={6}
          color="teal.500"
          _hover={{ transform: "scale(1.2)", color: "teal.400" }}
          transition="0.3s"
        />
        <Text ml={2} color="teal.500" fontWeight="bold">
          Help
        </Text>
      </Box>
    </Tooltip>
  );
};

export default Instructions;
