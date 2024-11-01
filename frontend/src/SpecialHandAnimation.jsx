import React, { useEffect, useState } from "react";
import { Box, Image } from "@chakra-ui/react";
import { motion } from "framer-motion";

const MotionBox = motion.create(Box);

function SpecialHandAnimation({ type }) {
  const [show, setShow] = useState(true);

  useEffect(() => {
    const timeout = setTimeout(() => setShow(false), 3000); // 3 seconds
    return () => clearTimeout(timeout);
  }, []);

  if (!show) return null;

  return (
    <MotionBox
      position="absolute"
      top="50%"
      left="50%"
      transform="translate(-50%, -50%)"
      zIndex="overlay"
      pointerEvents="none"
    >
      {type === "bomb" && (
        <MotionBox
          initial={{ scale: 0 }}
          animate={{ scale: [1, 3, 0], opacity: [1, 0.5, 0] }}
          transition={{ duration: 3 }}
        >
          <Image
            src={`${process.env.PUBLIC_URL}/effects/bomb.webp`}
            alt="Bomb"
            boxSize="300px"
          />
        </MotionBox>
      )}

      {type === "airplane" && (
        <MotionBox
          initial={{ x: "-100vw" }}
          animate={{ x: "100vw" }}
          transition={{ duration: 5 }}
        >
          <Image
            src={`${process.env.PUBLIC_URL}/effects/airplane.webp`}
            alt="Flying Airplane"
            boxSize="300px"
          />
        </MotionBox>
      )}
    </MotionBox>
  );
}

export default SpecialHandAnimation;
