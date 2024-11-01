<Box
  key={i}
  p={1}
  borderWidth={1}
  borderColor="black"
  borderRadius="md"
  mx={1}
  transition="transform 0.2s"
  _hover={{ transform: "scale(1.1)" }}
>
  <Image
    src={`${process.env.PUBLIC_URL}/cards/${card}.png`}
    alt={`Card ${card}`}
    boxSize="50px"
    objectFit="cover"
  />
</Box>;
