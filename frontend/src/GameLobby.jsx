import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import BetComponent from "./BetComponent";
import Hand from "./Hand";
import OpponentHand from "./OpponentHand";
import Round from "./Round";
import Scoreboard from "./Scoreboard";
import AlertMessage from "./AlertMessage";
import WaitingPage from "./WaitingPage";
import RoundInfo from "./RoundInfo";
import RoundHistory from "./RoundHistory";
import TurnBanner from "./TurnBanner";
import CardMoveButtons from "./CardMoveButtons";
import { Heading, Text, Container, Highlight, Box, Flex, List, ListItem } from '@chakra-ui/react';
import { completeGameTestData } from "./test_sets.js";
const testMode = false;

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
    const [alertMessage, setAlertMessage] = useState(null);
    const [showAlert, setShowAlert] = useState(false);
    const [uniqueId, setUniqueId] = useState(""); // Add uniqueId to the state
    const [possibleMoves, setPossibleMoves] = useState(null);
    
    

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

      if (testMode){
          setGameData(completeGameTestData);
          setLoading(false);
          setPromptMove(false);
          setPromptBet(false);
          // setShowAlert(true);
          // setAlertMessage("Test alert: you made a bad move");
          // setTimeout(() => { 
          //     setShowAlert(false);
          //     // setShowAlert(true);
          // }, 3000); // 3000 ms = 3 seconds
          // setTimeout(() => {
          //     setAlertMessage("Test 2");
          //     setShowAlert(true);
          //     // setShowAlert(true);
          // }, 4000); // 3000 ms = 3 seconds

          // setShowAlert(false);
      } else {
          fetchGameData();          
      }

    let uniqueIdCook = getCookie("uniqueId");
    if (!uniqueIdCook) {
      uniqueIdCook = "user_" + Math.random().toString(36).substr(2, 9);
      setCookie("uniqueId", uniqueIdCook, 7); // Set cookie for 7 days
    }
    setUniqueId(uniqueIdCook); // Save the uniqueId in the state
    
    const ws = new WebSocket(
      `ws://localhost:8000/ws/game/${id}?id=${uniqueIdCook}`,
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
          console.log("RECEIVED ALERT", message);
          setAlertMessage(message.message);
          setShowAlert(true);
          setTimeout(() => {
              setShowAlert(false);
          }, 3000);
      } else if (message.action === "make_a_move") {
          // Prompt player for move
          console.log("REQUEST FOR MOVE", message);
          setPossibleMoves(message.possible_moves);
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
        cards: selectedCards.map(c => c.card),
        kickers: selectedKickers.map(c => c.card),
      };
      console.log("Sending selected cards:", message);
      socket.send(JSON.stringify(message));
      setPromptMove(false);
    }
  };

    const handleMove = (move) => {
        if (socket && promptMove) {
            const message = {
                action: "move",
                cards: move.hand_cards,
                kickers: move.kicker_cards,
      };
      console.log("Sending selected cards:", message);
      socket.send(JSON.stringify(message));
      setPromptMove(false);        // Implement your move handling logic here
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
    if (!gameData.started){
        return <WaitingPage gameData={gameData}/>

    }

          return (
              <>
              <Container maxW="container.xl" p={4}>

      {/* Header Section */}
      <Flex justify="space-between" p={4} bg="gray.100">
        <Scoreboard scoreboard={gameData.scoreboard} />
        
        <Heading size="lg">Game Lobby: {gameData.game_id}</Heading>
        
        <RoundHistory roundHistory={gameData.round_history}/>
      </Flex>

                {showAlert && <AlertMessage message={alertMessage} />}

                <TurnBanner gameDataUid={gameData.current_player_uid} uid={uniqueId}/>
                <RoundInfo gameData={gameData}/>

      {/* Opponent Hands and Round Display */}
                <Flex justify="space-between" p={4} gap={4}>
        {/* Left Opponent */}
        {gameData.started && gameData.players && gameData.players.length > 0 && (
          <OpponentHand
            username={gameData.players[0].username}
            exposedCards={gameData.players[0].exposed_cards}
            nCards={gameData.players[0].n_cards}
          />
        )}

        {/* Display of Going Hand */}
                  {gameData.started && <Round hands={gameData.cur_round} bidValue={gameData.bid} />}

        {/* Right Opponent */}
        {gameData.started && gameData.players && gameData.players.length > 1 && (
          <OpponentHand
            username={gameData.players[1].username}
            exposedCards={gameData.players[1].exposed_cards}
            nCards={gameData.players[1].n_cards}
          />
        )}
      </Flex>

      {/* Hand Component */}
        <Hand
          myCards={gameData.my_cards}
          promptMove={promptMove}
          onSubmit={submitMove}
        />

                {possibleMoves && possibleMoves.length > 0 && promptMove && <CardMoveButtons possibleMoves={possibleMoves} handleMove={handleMove} />}
                
      {/* Bet Component */}
      {promptBet && <BetComponent lastBid={lastBid} submitBet={submitBet} />}
                
              </Container>
              </>

  );
}

export default GameLobby;
