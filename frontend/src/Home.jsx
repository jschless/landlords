import React from "react";
import { useNavigate } from "react-router-dom";

function Home() {
  const navigate = useNavigate();

  const createGame = async () => {
    try {
      const response = await fetch("http://localhost:8000/create_game", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error("Failed to create game");
      }

      const data = await response.json();
      const gameId = data.game_id;
      navigate(`/game/${gameId}`);
    } catch (error) {
      console.error("Error creating game:", error);
    }
  };

  return (
    <div>
      <h1>Welcome to the Game!</h1>
      <button onClick={createGame}>Create Game</button>
    </div>
  );
}

export default Home;
