import React, { useState } from "react";

function Hand({ myCards, onSubmit, promptMove }) {
  const [selectedCards, setSelectedCards] = useState([]);
  const [selectedKickers, setSelectedKickers] = useState([]);

  const handleCardClick = (e, card, index) => {
    if (e.button === 0) {
      // Left-click
      if (e.shiftKey) {
        // If shift key is pressed
        // Add or remove from selectedKickers list
        if (selectedKickers.some((c) => c.index === index)) {
          setSelectedKickers(selectedKickers.filter((c) => c.index !== index)); // Remove if already selected
        } else {
          setSelectedKickers([...selectedKickers, { card, index }]); // Add new kicker
        }
      } else {
        // Add or remove from selectedCards list
        if (selectedCards.some((c) => c.index === index)) {
          setSelectedCards(selectedCards.filter((c) => c.index !== index)); // Remove if already selected
        } else {
          setSelectedCards([...selectedCards, { card, index }]); // Add new card
        }
      }
    }
  };

  const handleSubmit = () => {
    if (selectedCards.length > 0) {
      console.log("submit happened", selectedCards, selectedKickers);
      onSubmit(selectedCards, selectedKickers);
      setSelectedCards([]);
      setSelectedKickers([]);
    }
  };

  return (
    <div>
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          padding: "20px",
          position: "absolute",
          bottom: 0,
          width: "100%",
        }}
      >
        {myCards.map((card, index) => (
          <img
            key={index}
            src={`${process.env.PUBLIC_URL}/cards/${card}.png`}
            alt={`Card ${card}`}
            style={{
              width: "50px",
              height: "75px",
              margin: "5px",
              border: selectedCards.some((c) => c.index === index)
                ? "3px solid blue"
                : selectedKickers.some((c) => c.index === index)
                  ? "3px solid orange"
                  : "none",
              cursor: "pointer",
            }}
            onClick={(e) => handleCardClick(e, card, index)}
          />
        ))}
      </div>
      {promptMove && (
        <button
          onClick={handleSubmit}
          style={{ margin: "10px", padding: "10px" }}
        >
          Submit Selected Cards
        </button>
      )}
    </div>
  );
}

export default Hand;
