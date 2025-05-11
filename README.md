<h1 align="center">Memory Matching Game</h1>

[DEMO VIDEO](https://drive.google.com/file/d/1slfBUbUokhwk6EGT5x9ev-XgljCOci8C/view?usp=sharing)

# Project Report

**Submitted By:**  
22k-4215 Zain Rizwan  
22k-4420 Saad Qamar  
**Course:** AI  
**Instructor:** Miss Alishba  
**Submission Date:** May 11, 2025  

## 1. Executive Summary

### Project Overview

This project involved creating a card-matching memory game that has an unique feature: players are required to match three cards of the same value, rather than the usual two.  There are two modes available in the game: single-player (against AI) and two-player.  The AI was created to emulate memory and strategic decision-making through a tailored heuristic method.  Using the Pygame library, the project was created in Python, with an emphasis on interactive gameplay, intelligent AI behavior, and seamless game mechanics.

## 2. Introduction

### Background

Players of classic memory-based card games such as Concentration must recall the locations of cards in order to match pairs.  These games are commonly employed to assess and enhance short-term memory and pattern recognition.  This project builds upon the classic formula by necessitating players to match three cards of the same type, thereby increasing difficulty and strategic depth and complicating memory retention and AI logic.

### Objectives

- Create a card-flipping memory game using **Pygame**
- Implement **PvP** and **PvAI** modes
- Modify the standard card-matching game to require matching triplets.
- Implement an AI player that remembers previously seen cards and selects optimal moves.
- Add a responsive UI and game over interface
- Maintain real-time smooth gameplay


##  3. Game Description

###  Original Rules

In a traditional card-matching game, cards are placed face-down.  With the goal of uncovering a matching pair, players turn over two cards each turn.  Unmatched cards are turned back over, while matched cards are taken away.  The game proceeds with players taking turns until every pair is matched.

### Innovations and Modifications

- Changed matching requirement from pairs to triplets.
- Developed AI memory logic to track multiple card positions of the same type.
- Enhanced user interface with turn indicators, animations, and score displays.
- Added game-over and restart functionality.
- Adjusted scoring and turn logic to support the new match-3 rule.


## 4. AI Approach and Methodology

### AI Techniques Used
The AI employs decision-making based on memory.  It keeps a dictionary of observed card values and their locations.  It picks cards according to known placements that create a triple.  It continues the exploration if there are less than three known cards for a value.


### Algorithm and Heuristic Design
- Memory Storage: AI stores revealed card values and their board positions.
- Prioritizes known matches
- Randomly guesses when no matches are known, avoiding duplicates

### Performance

- Fast decision-making (< 50ms per turn)
- Emulates human memory
- Improves performance as more cards are revealed



## 5. Game Mechanics and Rules

### Game Rules

- Each turn, a player selects three cards to flip.
- A match is successful only if all three cards are of the same value.
- Matched cards are removed; unmatched ones are flipped back.
- Player gets another turn upon a successful match.

### Turn-based mwchanics

- Turn alternates unless a player makes a successful match.
- Each player has a score counter.
- The game board updates dynamically after every selection.

### Win Conditions

- The game ends when all possible triplets are matched.
- Player with most matches wins
-  A draw is declared in case of equal scores.

## 🛠️ 6. Implementation and Development

### 🔨 Process

- Built grid and UI in **Pygame**
- Created matching and flipping logic
- Developed **PvP** and **PvAI** loops
- Programmed AI with memory logic
- Added scoring, game end screen, and animations

### 💻 Tools & Libraries

- **Language:** Python
- **Libraries:**
  - `pygame` – UI and game control
  - `random`, `time` – Card shuffle and delays

### ⚠️ Challenges

- Syncing animations and input
- Designing reactive and fair AI
- Handling turn transitions smoothly
- Preventing rapid/invalid card clicks
- Balancing game flow and difficulty

---

## 👥 7. Team Contributions

- **Zain Rizwan:** Game loop, scoring, card mechanics  
- **Saad Qamar:** AI logic, memory system, UI feedback

---

## 📊 8. Results and Discussion

### 🤖 AI Behavior

- Consistently uses memory to find matches
- Recognizes patterns quickly as game progresses
- Provides fair yet competitive gameplay

### 🎮 Player Feedback

- Clean, intuitive controls
- Replayable with randomized layouts
- PvAI mode feels intelligent and reactive
- PvP mode supports quick fun matches

---

> ✅ *For best experience, run the game in a desktop environment with Python and Pygame installed.*

