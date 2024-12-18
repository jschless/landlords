import React from "react";
import { Box, Text, Fade } from "@chakra-ui/react";

const AlertMessage = ({ messages }) => {
  return (
    <>
      {messages.map((alert, i) => (
        <Fade key={alert.id + i} in={true}>
          <Box
            p={4}
            bg="red.500"
            color="white"
            borderRadius="md"
            boxShadow="md"
            mb={4}
            textAlign="center"
          >
            <Text fontWeight="bold">{alert.message}</Text>
          </Box>
        </Fade>
      ))}
    </>
  );
};

export default AlertMessage;
