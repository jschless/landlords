import React from "react";

function OpponentHand({ username, exposedCards, nCards }) {
  return (
    <div style={{ textAlign: "center", margin: "10px" }}>
      <h3>{username}</h3>
      <div style={{ display: "flex", justifyContent: "center" }}>
        {exposedCards.map((card, index) => (
          <img
            key={index}
            src={`${process.env.PUBLIC_URL}/cards/${card}.png`}
            alt={`Card ${card}`}
            style={{ width: "50px", height: "75px", margin: "5px" }}
          />
        ))}
        <img
          src={`${process.env.PUBLIC_URL}/cards/back-black.png`} // Placeholder for card count image
          alt="Number of cards"
          style={{ width: "50px", height: "75px", margin: "5px" }}
        />
        <span>{nCards}</span>
      </div>
    </div>
  );
}

export default OpponentHand;
