import React from "react";
import {
  Flex,
  Box,
  Heading,
  List,
  ListItem,
  Text,
  Icon,
  useColorModeValue,
  VStack,
} from "@chakra-ui/react";
import { FaStar } from "react-icons/fa"; // Ensure react-icons is installed

function Scoreboard({ scoreboard }) {
  // Get the colors outside of the mapping function
  const listItemBgColor = useColorModeValue("white", "gray.600");
  const listItemHoverColor = useColorModeValue("gray.200", "gray.500");
  const textColor = useColorModeValue("teal.600", "teal.300");

  return (
    <Flex
      justify="space-between"
      p={4}
      bg={useColorModeValue("gray.100", "gray.700")}
      borderRadius="md"
    >
      <Box>
        <Heading size="md" mb={3} textAlign="center">
          Scoreboard
        </Heading>
        <VStack align="stretch">
          <List spacing={3}>
            {Object.entries(scoreboard).map(([name, score], index) => (
              <ListItem
                key={index}
                p={2}
                borderRadius="md"
                bg={listItemBgColor} // Use the color variable
                boxShadow="md"
                _hover={{ bg: listItemHoverColor, transform: "scale(1.02)" }}
                transition="all 0.2s"
              >
                <Flex align="center" justify="space-between">
                  <Text fontWeight="bold" color={textColor}>
                    {" "}
                    {/* Use the text color variable */}
                    {name}
                  </Text>
                  <Flex align="center">
                    <Icon as={FaStar} color="yellow.400" mr={1} />{" "}
                    {/* Star icon for visual interest */}
                    <Text>{score}</Text>
                  </Flex>
                </Flex>
              </ListItem>
            ))}
          </List>
        </VStack>
      </Box>
    </Flex>
  );
}

export default Scoreboard;
