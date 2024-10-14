import React, { useState } from "react";

function BetComponent({ lastBid, submitBet }) {
  const [bet, setBet] = useState("");

  return (
    <div>
      <h2>Make Your Bet:</h2>
      <div onChange={(e) => setBet(e.target.value)}>
        <label>
          <input type="radio" value="0" name="bet" checked={bet === "0"} />
          Pass
        </label>

        {/* Dynamically create buttons from last_bid + 1 to 3 */}
        {[...Array(3 - lastBid)].map((_, index) => {
          const bidValue = lastBid + index + 1; // starts at last_bid + 1
          return (
            <label key={bidValue}>
              <input
                type="radio"
                value={bidValue}
                name="bet"
                checked={bet === String(bidValue)}
              />
              {bidValue}
            </label>
          );
        })}
      </div>
      <button onClick={() => submitBet(bet)}>Submit Bet</button>
    </div>
  );
}

export default BetComponent;
