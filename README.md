# Othello Game

**COEN 244 Class Project**  
**Date:** 11/10/2023

This repository contains an enhanced implementation of the classic Othello (Reversi) game.

## Project Overview

This project was developed for the **COEN 244** class. 

*   **Language Switch**: The game logic was originally designed in **C++**, but has been ported to **Python** for greater convenience and portability.
*   **UI Upgrade**: The user interface has been completely overhauled. It now features a fully graphical interface (GUI) built with Python's Turtle library, replacing the standard console output with an interactive window.

## Gameplay Screenshots

| Main Menu | Mode Selection |
|:---:|:---:|
| ![Main Menu](screenshots/Screenshot%202025-12-18%20175121.png) | ![Mode Select](screenshots/Screenshot%202025-12-18%20175222.png) |

| Color Selection | Gameplay |
|:---:|:---:|
| ![Color Select](screenshots/Screenshot%202025-12-18%20175234.png) | ![Gameplay](screenshots/Screenshot%202025-12-18%20175242.png) |

## Game Rules

The game is played on an 8x8 board with disc-like pieces that have a black side and a white side.

1.  **Setup**: The game begins with four discs placed in a square in the middle of the grid, two facing white side up, two pieces with the dark side up, with same-colored discs on a diagonal with each other.
2.  **Objective**: The goal is to have the majority of discs on the board showing your color when the game ends.
3.  **Turns**: Black always moves first. Players take turns placing a disc of their color on the board.
4.  **Valid Moves**:
    *   You must place your disc in a position that "outflanks" one or more of your opponent's discs.
    *   This means there must be a continuous straight line (horizontal, vertical, or diagonal) of the opponent's discs between the new disc you placed and another disc of your own color already on the board.
5.  **Capturing**: When a valid move is made, all the opponent's discs lying on that straight line between the new disc and the anchoring disc are flipped to your color.
6.  **Passing**: If a player cannot make a valid move, they must pass their turn. If they can make a move, they must.
7.  **End Game**: The game ends when neither player can move (usually when the board is full). The player with the most discs of their color on the board wins.

## Features

*   **Interactive Menu System**: A retro-style main menu with options to Play, view Settings, or Quit.
*   **Multiple Game Modes**:
    *   **Vs Computer**: Challenge the AI. You can choose your color (Black goes first, White goes second).
    *   **Vs Player**: A local 2-player mode to play against a friend on the same machine.
*   **Visual Enhancements**:
    *   **Move Highlighting**: Possible legal moves are highlighted with blue dots to assist decision-making.
    *   **Live Status**: Real-time display of the current turn and score (piece count).
    *   **Themed Design**: Classic Othello board colors (Forest Green background with Black/White tiles).

## How to Run

Ensure you have Python 3 installed. Run the game using:

```bash
python game.py
```

## Tech Stack

*   **Language**: Python 3
*   **Graphics**: Turtle Graphics Module (Standard Python Library)
