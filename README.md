# Adivinhador de Regras

A Python game developed as part of **MC102 — Algorithms and Computer Programming**, during the first semester of the Computer Science undergraduate program at the **University of Campinas (UNICAMP), Brazil**.

The project was developed collaboratively by two Computer Science students as part of the course's programming assignments.

## About the Project

Adivinhador de Regras is a game built with Python and Pygame in which the player interacts with numbers and mathematical rules. The project was designed to practice programming fundamentals through a practical implementation.

The game includes different types of rules, such as:

- **Modulo (`mod`)** — operations involving the remainder of a division.
- **Power (`pot`)** — operations involving exponentiation.
- **Integer (`int`)** — operations involving integer values.

## Technologies

- **Python** — game logic and implementation.
- **Pygame** — graphics and user interaction.
- **Git and GitHub** — version control and project collaboration.

## Getting Started

### Prerequisites

- Python 3
- pip

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/nicolaspavanetti/adivinhador-de-regras
   cd adivinhador-de-regras
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install the dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

## How to Play

Start the game in manual mode:

```bash
python game.py
```

The game generates a secret rule involving integers from 1 to 100,000. Your goal is to discover the rule using number guesses and, ultimately, submit the correct rule.

### Available Commands

| Command | Description |
|---|---|
| `42` | Guess the number 42 |
| `num 42` | Same as above |
| `mod 5 2` | Guess the rule `n % 5 == 2` |
| `pot 3` | Guess the perfect-power order 3 |
| `int 10 50` | Guess the interval from 10 to 50, inclusive |

Press **Enter** to submit a guess, **R** to start a new match, and **Esc** to close the game.

### Automatic Mode

Run the automatic player:

```bash
python game.py --auto
```

Specify the interval between automatic guesses in milliseconds:

```bash
python game.py --auto 500
```

The default interval is 800 milliseconds. Press **Space** to pause or resume automatic gameplay.

## Project Structure

```text
adivinhador-de-regras/
├── game.py
├── player.py
├── requirements.txt
├── .gitignore
└── README.md
```

- **`game.py`** — game logic, rule generation, input handling, feedback, and graphical interface.
- **`player.py`** — automatic player's guessing strategy.
- **`requirements.txt`** — Python dependencies.
- **`.gitignore`** — files and directories excluded from Git tracking.
- **`README.md`** — project documentation.

## Academic Context

This project was developed for **MC102 — Algorithms and Computer Programming**, a course taken during the first semester of the Computer Science program at UNICAMP.

The assignment provided an opportunity to apply programming concepts to a complete project, including problem-solving, algorithm implementation, and the organization of code across multiple files.

## Authors

- **Nicolas Pavanetti** — [GitHub](https://github.com/nicolaspavanetti)
- **Daniel Dorigan Campos** — [GitHub](https://github.com/danieldorigancc)

## Learning Objectives

Through this project, we practiced:

- Algorithm design and problem-solving.
- Fundamental programming concepts.
- Organizing code into separate modules.
- Developing a game with Python and Pygame.
- Collaborative software development.

---

*Developed as an academic project for MC102 at the University of Campinas (UNICAMP).*
