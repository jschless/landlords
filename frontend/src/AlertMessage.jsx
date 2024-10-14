import React, { useEffect, useState } from "react";
import { Box, Text, Fade } from "@chakra-ui/react";

const AlertMessage = ({ message, duration = 3000 }) => {
  const [isVisible, setIsVisible] = useState(true);

  useEffect(() => {
    // Set a timer to hide the alert after the specified duration
    const timer = setTimeout(() => {
      setIsVisible(false);
    }, duration);

    // Cleanup the timer when the component unmounts
    return () => clearTimeout(timer);
  }, [duration]);

  return (
    <Fade in={isVisible}>
      <Box
        p={4}
        bg="red.500"
        color="white"
        borderRadius="md"
        boxShadow="md"
        mb={4}
        textAlign="center"
      >
        <Text fontWeight="bold">{message}</Text>
      </Box>
    </Fade>
  );
};

export default AlertMessage;
