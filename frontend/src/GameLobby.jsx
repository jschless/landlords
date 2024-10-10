import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import BetComponent from "./BetComponent";
import Hand from "./Hand";
import OpponentHand from "./OpponentHand";

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
}

function setCookie(name, value, days) {
  const expires = new Date(Date.now() + days * 864e5).toUTCString();
  document.cookie = `${name}=${encodeURIComponent(value)}; expires=${expires}; path=/`;
}

function GameLobby() {
  const { id } = useParams(); // Get game ID from URL
  const [gameData, setGameData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [socket, setSocket] = useState(null);
  const [lastBid, setLastBid] = useState(0);
  const [promptMove, setPromptMove] = useState(false);
  const [promptBet, setPromptBet] = useState(false);

  useEffect(() => {
    const fetchGameData = async () => {
      try {
        const response = await fetch(`http://localhost:8000/game/${id}`);

        if (!response.ok) {
          throw new Error("Game not found");
        }

        const data = await response.json();
        setGameData(data);
        setLoading(false);
      } catch (error) {
        setError(error.message);
        setLoading(false);
      }
    };

    fetchGameData();

    let uniqueId = getCookie("uniqueId");
    if (!uniqueId) {
      uniqueId = "user_" + Math.random().toString(36).substr(2, 9);
      setCookie("uniqueId", uniqueId, 7); // Set cookie for 7 days
    }

    const ws = new WebSocket(
      `ws://localhost:8000/ws/game/${id}?id=${uniqueId}`,
    );

    ws.onopen = () => {
      console.log("WebSocket connection established");
    };

    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      console.log(message);

      if (message.action === "update") {
        // Updates screen with new data
        setGameData(message);
      } else if (message.action === "alert") {
        // TODO: Display an alert banner on top of screen
        console.log(message.text);
      } else if (message.action === "make_a_move") {
        // Prompt player for move
        setPromptMove(true);
      } else if (message.action === "make_a_bid") {
        // Prompt for a bet
        setLastBid(message.last_bid);
        setPromptBet(true);
      }
    };

    ws.onclose = () => {
      console.log("WebSocket connection closed");
    };

    setSocket(ws);

    return () => {
      ws.close();
    };
  }, [id]);

  const submitMove = (selectedCards, selectedKickers) => {
    if (socket && promptMove) {
      const message = {
        action: "move",
        cards: selectedCards,
        kickers: selectedKickers,
      };
      console.log("Sending selected cards:", message);
      socket.send(JSON.stringify(message));
      setPromptMove(false);
    }
  };

  const submitBet = (bet) => {
    if (socket && bet) {
      const message = { action: "bet", bet };
      socket.send(JSON.stringify(message));
      setPromptBet(false);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <div>
        <h1>Game Lobby: {gameData.game_id}</h1>
        {gameData.username !== "" && <h2>User: {gameData.username}</h2>}
        {!gameData.started && (
          <div>
            <h2>
              Waiting for {2 - gameData.players.length} player
              {gameData.players.length === 1 ? "" : "s"} to join... players
              currently here:
            </h2>
            <ul>
              {gameData.players.map((player, index) => (
                <li key={index}>{player.username}</li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* FOR DEBUG PURPOSES */}
      <pre>{JSON.stringify(gameData, null, 2)}</pre>

      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          padding: "20px",
        }}
      >
        {/* Left Opponent */}
        {gameData.started &&
          gameData.players &&
          gameData.players.length > 0 && (
            <OpponentHand
              username={gameData.players[0].username}
              exposedCards={gameData.players[0].exposed_cards}
              nCards={gameData.players[0].n_cards}
            />
          )}

        {/* Right Opponent */}
        {gameData.started &&
          gameData.players &&
          gameData.players.length > 1 && (
            <OpponentHand
              username={gameData.players[1].username}
              exposedCards={gameData.players[1].exposed_cards}
              nCards={gameData.players[1].n_cards}
            />
          )}
      </div>

      <div>
        {gameData.started &&
          gameData.my_cards &&
          gameData.my_cards.length > 0 && (
            <Hand
              myCards={gameData.my_cards}
              promptMove={promptMove}
              onSubmit={submitMove}
            />
          )}
      </div>

      {promptBet && <BetComponent lastBid={lastBid} submitBet={submitBet} />}
    </div>
  );
}

export default GameLobby;
