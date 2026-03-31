# Wordle Bot Project

This project is a full-featured Wordle engine built in Python, including:

* Interactive gameplay (terminal + Streamlit UI)
* Solver using expected value optimization
* Hint system
* Auto-solver
* Post-game analysis
* Precomputation for performance

---

# 📁 Project Structure

## 1. `wordle_game.py`

**Purpose:** Core game engine

### Responsibilities:

* Manages game state (solution, guesses, attempts)
* Evaluates guesses against the solution
* Tracks keyboard state
* Formats board output (terminal + HTML)

### Key Logic:

* `make_guess()`
  → Evaluates guess and updates game state

* `is_solved()`
  → Checks if last guess matches solution

* `attempts_remaining()`
  → Tracks remaining turns

* `format_guess()`
  → ANSI formatting for terminal

* `format_guess_html()`
  → HTML/CSS rendering for Streamlit UI

---

## 2. `wordle_words.py`

**Purpose:** Load and prepare word lists

### Responsibilities:

* Load all valid guess words
* Load official solution words (source of truth)
* Clean and standardize word lists

### Key Logic:

* `load_words()`
  → Returns:

  * `all_guesses` (full dictionary)
  * `solution_words` (curated solutions)

---

## 3. `wordle_main.py`

**Purpose:** Terminal-based gameplay

### Responsibilities:

* Runs main game loop
* Handles user input (guess, hint, solve, solution)
* Displays board and keyboard
* Tracks remaining possible solutions
* Stores analysis history

### Key Logic:

* Game loop with input validation
* Filtering `remaining_words` after each guess
* Replay logic (play again / solve / exit)

---

## 4. `precompute_first_turn.py`

**Purpose:** Precompute optimal first guesses

### Responsibilities:

* Runs solver on full solution space
* Saves results to file for reuse

### Key Logic:

* `find_best_guess(all_guesses, solution_words)`
* Saves output to:

  * `first_turn_scores.csv` or `.pkl`

### Why It Matters:

* First move is deterministic → compute once
* Avoids expensive recomputation during gameplay

---

## 5. `utils.py`

**Purpose:** Shared utility functions

### Responsibilities:

* Core logic reused across modules

### Key Logic:

* `evaluate_pattern(solution, guess)`
  → Returns Wordle color pattern (G/Y/B)

### Importance:

* Centralized logic used by:

  * game engine
  * solver
  * filtering
  * analysis

---

## 6. `solver.py`

**Purpose:** Optimization engine

### Responsibilities:

* Evaluate all guesses against remaining solutions
* Rank guesses by expected remaining words
* Provide hint suggestions
* Post-game analysis

### Key Logic:

#### `generate_outcomes()`

* Creates guess × solution combinations
* Computes patterns

#### `score_guesses()`

* Groups by (guess, pattern)
* Computes:

  * words remaining
  * probability
  * expected value

#### `find_best_guess()`

* Returns ranked guesses

#### `analyze_game()`

* Evaluates user guesses:

  * rank
  * expected words remaining
  * top alternatives

#### `build_display_guesses()`

* Ensures:

  * top N guesses shown
  * minimum number of solution words included

---

## 7. `test_auto_solver.py`

**Purpose:** Validate auto-solve logic

### Responsibilities:

* Runs solver against a known solution
* Prints step-by-step results

### Key Logic:

* Calls `auto_solve()`
* Verifies:

  * correct progression
  * solution reached

---

## 8. `test_solver.py`

**Purpose:** Validate solver accuracy

### Responsibilities:

* Tests scoring and ranking logic
* Confirms parity with R implementation

### Key Logic:

* Simulates:

  * guess
  * pattern
  * filtering
* Runs solver on reduced solution space

---

## 9. `wordle_app.py`

**Purpose:** Streamlit web app

### Responsibilities:

* Provides browser-based UI
* Replaces terminal interaction with buttons
* Maintains game state using `st.session_state`

### Features:

* Interactive board (HTML-rendered tiles)
* Buttons:

  * Submit Guess
  * Hint
  * Solve
  * Reveal Solution
  * Play Again

### Key Logic:

* Uses:

  * `WordleGame` for state
  * `evaluate_pattern` for filtering
  * `find_best_guess` for hints
* Uses `@st.cache_data` for performance

---

# 🧠 Core Concepts

## 1. Remaining Words Filtering

After each guess:

```
remaining_words = [
    w for w in remaining_words
    if evaluate_pattern(w, guess) == pattern
]
```

→ This represents the current solution space.

---

## 2. Expected Value Optimization

Each guess is evaluated by:

```
E[remaining_words] = Σ (probability × words_remaining)
```

Goal:
→ Minimize expected remaining possibilities

---

## 3. Solver Strategy

* Early game → explore (information gain)
* Late game → exploit (choose actual solutions)

---

## 4. First Turn Optimization

* First move is constant
* Precomputed and reused
* Improves performance significantly

---

## 5. Analysis System

For each guess:

* Rank among all possible guesses
* Expected remaining words
* Compare to top alternatives

---

# 🚀 Future Improvements

* Add luck metric (expected vs actual)
* Cache mid-game solver states
* Improve UI (keyboard, animations)
* Optimize solver performance
* Evaluate all starting words

---

# 🎯 Summary

This project combines:

* Game engine
* Optimization model
* UI layer
* Analytical tooling

Result:
→ A complete Wordle AI + coaching system
