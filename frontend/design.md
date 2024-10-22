# General Design

## Views

1. Homepage:
   - Allows people to create a game
   - Allows people to create a username?
2. Game Lobby:
   - Initially is a loading screen
   - Once game loads, shows cards

## View from player's perspective:

| Scoreboard Game Name Chat |
| |
| |
| |
| P1 view Current hand P2 view |
| [list grows down] |
| |
| |
| |
| |
| |
| |
| |
| Your cards |

---

## Gameflow

Gameflow is controlled by websockets sent from server.
Each message contains an "action":

- `update`: updates the game view
- `alert`: sends player a message, mostly for mistakes
- `make_a_bid`: solicits a bid from a player
- `make_a_bet`: allows a player to submit a bet

Basically, users can only send a message to the server when they have received a solicitation for a move or a bet
