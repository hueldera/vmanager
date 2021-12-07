import React, { Component } from "react";
import { Routes, Route } from "react-router-dom";

import { Container, Flex } from "@chakra-ui/react";

import Dashboard from "./pages/Dashboard";

export default function App() {
  return (
    <Container maxW="container.lg">
      <Flex direction="column">
        <Routes>
          <Route path="/" element={<Dashboard />} />
        </Routes>
      </Flex>
    </Container>
  );
}
