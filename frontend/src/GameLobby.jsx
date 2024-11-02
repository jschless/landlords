import React, { useEffect, useState, useRef } from "react";
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
import CountdownTimer from "./CountdownTimer";
import SpecialHandAnimation from "./SpecialHandAnimation";
import { Heading, Container, Flex, Stack } from "@chakra-ui/react";
import { completeGameTestData } from "./test_sets.js";
const testMode = process.env.REACT_APP_DEVELOPMENT;
const TIMER_LENGTH = 15;

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
  const [alertMessages, setAlertMessages] = useState([]);
  const [uniqueId, setUniqueId] = useState("");
  const [possibleMoves, setPossibleMoves] = useState(null);
  const [moveTimer, setMoveTimer] = useState(TIMER_LENGTH);
  const [specialHand, setSpecialHand] = useState(null);
  const [lastHand, setLastHand] = useState(null);

  const timerRef = useRef(null); // Use ref to hold timer ID

  const apiUrl = process.env.REACT_APP_DEVELOPMENT
    ? "http://localhost:8000/backend"
    : "https://doughdizhu.com/backend";

  const wsUrl = process.env.REACT_APP_DEVELOPMENT
    ? "ws://localhost:8000/backend"
    : "wss://doughdizhu.com/backend";

  const sendMove = (cards, kickers) => {
    if (socket && promptMove) {
      const message = {
        action: "move",
        cards: cards,
        kickers: kickers,
      };
      console.log("Sending selected cards:", message);
      socket.send(JSON.stringify(message));
      setPromptMove(false);
      clearInterval(timerRef.current);
    }
  };

  useEffect(() => {
    const fetchGameData = async () => {
      try {
        const response = await fetch(`${apiUrl}/game/${id}`);

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

    if (testMode) {
      setGameData(completeGameTestData);
      setLoading(false);
      setPromptMove(false);
      setPromptBet(false);
      // setSpecialHand("bomb");
      // setAlertMessages([
      //   { id: 1, message: "test 1" },
      //   { id: 2, message: "test 2" },
      // ]);
      setPossibleMoves([
        {
          base: 3,
          chain_length: 1,
          low: 7,
          kicker_base: 1,
          kicker_len: 1,
          hand_cards: [7, 7, 7],
          kicker_cards: [3],
          string_repr: "triple-1-chain with 1 single discards",
        },
        {
          base: 3,
          chain_length: 1,
          low: 7,
          kicker_base: 1,
          kicker_len: 1,
          hand_cards: [7, 7, 7],
          kicker_cards: [3],
          string_repr: "triple-1-chain with 1 single discards",
        },
        {
          base: 3,
          chain_length: 1,
          low: 7,
          kicker_base: 1,
          kicker_len: 1,
          hand_cards: [7, 7, 7],
          kicker_cards: [3],
          string_repr: "triple-1-chain with 1 single discards",
        },
      ]);

      setPromptMove(true);
      console.log("Alert Messages", alertMessages);
    } else {
      fetchGameData();
    }

    let uniqueIdCook = getCookie("uniqueId");
    if (!uniqueIdCook) {
      uniqueIdCook = "user_" + Math.random().toString(36).substr(2, 9);
      setCookie("uniqueId", uniqueIdCook, 7); // Set cookie for 7 days
    }
    setUniqueId(uniqueIdCook); // Save the uniqueId in the state

    const ws = new WebSocket(`${wsUrl}/ws/game/${id}?id=${uniqueIdCook}`);

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
        const newAlert = { id: alertMessages.length, message: message.message };
        setAlertMessages((prevMessages) => [...prevMessages, newAlert]);

        setTimeout(() => {
          setAlertMessages((prevMessages) =>
            prevMessages.filter((alert) => alert.id !== newAlert.id),
          );
        }, 4000);
      } else if (message.action === "make_a_move") {
        // Prompt player for move
        console.log("REQUEST FOR MOVE", message);
        setPossibleMoves(message.possible_moves);
        setPromptMove(true);
        // Set timer
        console.log("Initiating timer");
        setMoveTimer(TIMER_LENGTH);
        if (timerRef.current) clearInterval(timerRef.current);
        timerRef.current = setInterval(() => {
          setMoveTimer((prev) => {
            return prev - 1;
          });
        }, 1000);
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
      clearInterval(timerRef.current);
    };
    // eslint-disable-next-line
  }, []);

  // Timer countdown0
  useEffect(() => {
    if (promptMove && moveTimer <= 1) {
      console.log("Auto submitting move");
      clearInterval(timerRef.current);
      const message = {
        action: "move",
        cards: [],
        kickers: [],
      };
      console.log("Sending selected cards:", message);
      socket.send(JSON.stringify(message));
      setPromptMove(false);
      clearInterval(timerRef.current);
    }
  }, [promptMove, moveTimer, timerRef, socket]);

  useEffect(() => {
    // Ensure this runs whenever gameData changes
    if (gameData) {
      const currentCurRound = gameData.cur_round || [];

      const lastRoundEntry = currentCurRound[currentCurRound.length - 1];

      const tempLastHand = lastRoundEntry?.[1];

      if (lastHand !== tempLastHand) {
        console.log("Updating last hand to", tempLastHand);
        setLastHand(tempLastHand);
        if (tempLastHand?.string_repr.includes("bomb")) {
          setSpecialHand("bomb");
        } else if (
          tempLastHand?.string_repr.includes("triple") &&
          tempLastHand?.string_repr.includes("chain")
        ) {
          setSpecialHand("airplane");
        } else {
          setSpecialHand(null);
        }
      }
    }
    // eslint-disable-next-line
  }, [gameData]);

  const submitMove = (selectedCards, selectedKickers) => {
    if (socket && promptMove) {
      sendMove(
        selectedCards.map((c) => c.card),
        selectedKickers.map((c) => c.card),
      );
    }
  };

  const handleMove = (move) => {
    if (socket && promptMove) {
      sendMove(move.hand_cards, move.kicker_cards);
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
  if (!gameData.started) {
    return <WaitingPage gameData={gameData} />;
  }

  return (
    <>
      <Container maxW="container.xl" p={4}>
        {/* Header Section */}
        <Flex justify="space-between" p={4} bg="gray.100">
          <Scoreboard scoreboard={gameData.scoreboard} />

          <Stack spacing={2} align="center">
            <Heading size="lg">Dough Dizhu Lobby</Heading>
            <Heading size="sm">Game ID: {gameData.game_id}</Heading>
            <RoundInfo gameData={gameData} />
          </Stack>

          <RoundHistory roundHistory={gameData.round_history} />
        </Flex>

        {alertMessages.length > 0 && <AlertMessage messages={alertMessages} />}

        <TurnBanner gameDataUid={gameData.current_player_uid} uid={uniqueId} />

        {/* Opponent Hands and Round Display */}
        <Flex justify="space-between" p={4} gap={4}>
          {specialHand && <SpecialHandAnimation type={specialHand} />}

          {/* Left Opponent */}
          {gameData.started &&
            gameData.players &&
            gameData.players.length > 0 && (
              <OpponentHand
                username={gameData.players[0].username}
                exposedCards={gameData.players[0].exposed_cards}
                nCards={gameData.players[0].n_cards}
                landlord_username={gameData.landlord_username}
                current_player_username={gameData.current_player_username}
              />
            )}

          {/* Display of Going Hand */}
          {gameData.started && (
            <Round hands={gameData.cur_round} bidValue={gameData.bid} />
          )}

          {/* Right Opponent */}
          {gameData.started &&
            gameData.players &&
            gameData.players.length > 1 && (
              <OpponentHand
                username={gameData.players[1].username}
                exposedCards={gameData.players[1].exposed_cards}
                nCards={gameData.players[1].n_cards}
                landlord_username={gameData.landlord_username}
                current_player_username={gameData.current_player_username}
              />
            )}
        </Flex>

        <Flex direction="column" justify="space-between" gap="4">
          {/* Hand Component */}
          <Hand
            myCards={gameData.my_cards}
            promptMove={promptMove}
            onSubmit={submitMove}
            isLandlord={gameData.username === gameData.landlord_username}
            username={gameData.username}
            current_player_username={gameData.current_player_username}
          />

          {possibleMoves && possibleMoves.length > 0 && promptMove && (
            <CardMoveButtons
              possibleMoves={possibleMoves}
              handleMove={handleMove}
            />
          )}

          <CountdownTimer promptMove={promptMove} moveTimer={moveTimer} m={4} />

          {/* Bet Component */}
          {promptBet && (
            <BetComponent lastBid={lastBid} submitBet={submitBet} />
          )}
        </Flex>
      </Container>
    </>
  );
}

export default GameLobby;
