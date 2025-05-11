# Memory-Match-Game
AI Project
# 🧠 Memory Matching Challenge

**Submitted By:**  
22k-4215 Zain Rizwan  
22k-4420 Saad Qamar  
**Course:** AI  
**Instructor:** Miss Alishba  
**Submission Date:** May 11, 2025  

---

## 📄 1. Executive Summary

### 🎯 Project Overview

The **Memory Matching Challenge** is a card-based puzzle game that tests a player's memory and pattern recognition skills. The game includes two modes: **Player vs Player** and **Player vs AI**, where the AI intelligently remembers previously seen cards to play strategically and challenge the player.

---

## 🧠 2. Introduction

### 📚 Background

Memory games are classic logic challenges. This digital adaptation modernizes the experience using Python and AI, making it engaging for both solo and competitive play.

### 🎯 Objectives

- Create a card-flipping memory game using **Pygame**
- Implement **PvP** and **PvAI** modes
- Develop an AI agent with card memory and logic
- Add a responsive UI and game over interface
- Maintain real-time smooth gameplay

---

## 🕹️ 3. Game Description

### 📜 Original Rules

Players flip two cards per turn and try to find matches. The player with the most matched pairs wins.

### 🔧 Enhancements

- **Graphical UI** with Pygame
- **Two Modes:**
  - **PvP** – Two players take turns
  - **PvAI** – AI competes using memory
- AI remembers revealed unmatched cards
- Game over screen displays final scores
- Real-time feedback with animations and sounds

---

## 🤖 4. AI Approach and Methodology

### 🧠 AI Techniques

- **Rule-Based Memory AI**:
  - Stores known card positions
  - Searches for matches before choosing at random

### 🧩 Heuristic Design

- Maintains a dictionary of revealed card positions
- Prioritizes known matches
- Randomly guesses when no matches are known, avoiding duplicates

### ⚙️ Performance

- Fast decision-making (< 50ms per turn)
- Emulates human memory
- Improves performance as more cards are revealed

---

## 📏 5. Game Mechanics and Rules

### 🎮 Game Rules

- **4x4 grid** of 8 pairs
- Players flip 2 cards each turn
- A match earns a point and another turn
- Non-matches flip back after delay

### 🔁 Turn Flow

1. Player flips two cards  
2. If matched → point + extra turn  
3. Else → cards flip back, turn changes  
4. AI executes turn in PvAI mode

### 🏆 Win Conditions

- Game ends when all pairs are matched
- Player with most matches wins

---

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

