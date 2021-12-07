import React from "react";
import { Flex, Text, Box, UnorderedList, ListItem } from "@chakra-ui/react";
import { NavLink } from "react-router-dom";

const isActiveStyle = {
  fontWeight: "bold",
  color: "#3182CE",
};

export default function Header() {
  const isActive = ({ isActive }: { isActive: boolean }) =>
    isActive ? isActiveStyle : undefined;
  return (
    <Box m={5}>
      <Flex
        direction="row"
        align="center"
        justify="space-between"
        wrap="wrap"
        mb={2}
      >
        <Text
          lineHeight={0.9}
          color="black"
          fontSize="4xl"
          fontWeight="extrabold"
        >
          Gestão de Vulnerabilidades
        </Text>
        <UnorderedList py={5} m={0} styleType="none">
          <ListItem display="inline">
            <NavLink to="/" style={isActive}>
              Dashboard
            </NavLink>
          </ListItem>
        </UnorderedList>
      </Flex>
      <hr />
    </Box>
  );
}
