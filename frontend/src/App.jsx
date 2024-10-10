import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Home from "./Home";
import GameLobby from "./GameLobby";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/game/:id" element={<GameLobby />} />
      </Routes>
    </Router>
  );
}

export default App;
