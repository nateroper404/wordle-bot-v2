
import streamlit as st
import random
import io
import contextlib
import pandas as pd
from pathlib import Path

from wordle_words import load_words
from solver import auto_solve, find_best_guess, analyze_game
from wordle_game import WordleGame
from utils import evaluate_pattern

DATA_DIR = Path(__file__).parent


@st.cache_data
def load_word_lists():
    return load_words(
        str(DATA_DIR / "Wordle Bot Starting Words v3.csv"),
        str(DATA_DIR / "Most Common 5 Letter Words.txt"),
        str(DATA_DIR / "Wordle Solution Words.txt")
    )


@st.cache_data
def load_first_turn_scores():
    return pd.read_csv(DATA_DIR / "first_turn_scores.csv")


all_guesses, solution_words = load_word_lists()
first_turn_scores = load_first_turn_scores()
solution_words_set = set(solution_words)


def init_game(solution):
    st.session_state.game = WordleGame(solution, all_guesses)
    st.session_state.solution = solution
    st.session_state.remaining_words = solution_words.copy()
    st.session_state.input_key = 0
    st.session_state.game_history = []
    st.session_state.show_bot_solution = False
    st.session_state.setdefault("show_keyboard", True)


# --- Mode selection screen ---
st.markdown("<h2 style='text-align:center;margin-bottom:0;'>Wordle+</h2>", unsafe_allow_html=True)

if "game" not in st.session_state:
    if st.session_state.get("setup_mode") == "choose":
        st.subheader("Enter a word to solve")
        word_input = st.text_input("Word (5 letters)", key="word_choice_input", autocomplete="off").strip().lower()

        if st.button("Start Game"):
            if len(word_input) != 5:
                st.warning("Must be exactly 5 letters.")
            elif word_input not in solution_words_set:
                st.warning(f"**{word_input.upper()}** is not a valid solution word. Try another.")
            else:
                init_game(word_input)
                del st.session_state.setup_mode
                st.rerun()

        if st.button("← Back"):
            del st.session_state.setup_mode
            st.rerun()

    else:
        st.subheader("How would you like to play?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎲 Random Word", use_container_width=True):
                init_game(random.choice(solution_words))
                st.rerun()
        with col2:
            if st.button("✏️ Choose a Word", use_container_width=True):
                st.session_state.setup_mode = "choose"
                st.rerun()

    st.stop()


game = st.session_state.game


# --- End-of-game dialogs ---
@st.dialog("You won! 🎉")
def win_dialog():
    st.write(f"You solved **{st.session_state.solution.upper()}** in {len(game.guesses)} guess{'es' if len(game.guesses) != 1 else ''}!")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Play Again", use_container_width=True):
            st.session_state.clear()
            st.rerun()
    with col2:
        if st.button("See Bot Solution", use_container_width=True):
            st.session_state.show_bot_solution = True
            st.rerun()


@st.dialog("Game Over")
def loss_dialog():
    st.write(f"The word was **{st.session_state.solution.upper()}**.")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Play Again", use_container_width=True):
            st.session_state.clear()
            st.rerun()
    with col2:
        if st.button("See Bot Solution", use_container_width=True):
            st.session_state.show_bot_solution = True
            st.rerun()


# --- Board ---
empty_row = """
<div style="display:flex;flex-direction:row;gap:4px;margin-bottom:4px;">
    <span style="display:inline-block;width:45px;height:45px;border:2px solid #3a3a3c;"></span>
    <span style="display:inline-block;width:45px;height:45px;border:2px solid #3a3a3c;"></span>
    <span style="display:inline-block;width:45px;height:45px;border:2px solid #3a3a3c;"></span>
    <span style="display:inline-block;width:45px;height:45px;border:2px solid #3a3a3c;"></span>
    <span style="display:inline-block;width:45px;height:45px;border:2px solid #3a3a3c;"></span>
</div>
"""

board_html = "".join(game.format_guess_html(g, p) for g, p in game.guesses)
board_html += empty_row * game.attempts_remaining()
st.html(f'<div style="display:flex;flex-direction:column;gap:0;width:fit-content;margin:0 auto;">{board_html}</div>')

kb_label = "Hide Keyboard" if st.session_state.get("show_keyboard", True) else "Show Keyboard"
with st.container(key="kb_toggle_container"):
    st.markdown("""
    <style>
    div[data-testid="kb_toggle_container"] button {
        padding-top: 2px;
        padding-bottom: 2px;
        font-size: 12px;
        line-height: 1;
    }
    </style>
    """, unsafe_allow_html=True)
    if st.button(kb_label, key="kb_toggle"):
        st.session_state.show_keyboard = not st.session_state.get("show_keyboard", True)
        st.rerun()

if st.session_state.get("show_keyboard", True):
    st.html(game.format_keyboard_html())

# --- Input (only while game is active) ---
game_over = game.is_solved() or game.attempts_remaining() == 0

if not game_over:
    guess = st.text_input("Enter your guess", key=f"guess_{st.session_state.input_key}", autocomplete="off")

    if st.button("Submit Guess"):
        guess = guess.strip().lower()
        if len(guess) != 5:
            st.warning("Guess must be 5 letters")
        elif not game.is_valid_guess(guess):
            st.warning("Not in word list")
        else:
            pattern = game.make_guess(guess)
            st.session_state.game_history.append({
                "guess": guess,
                "pattern": pattern,
                "remaining_words_before": st.session_state.remaining_words.copy()
            })
            st.session_state.remaining_words = [
                w for w in st.session_state.remaining_words
                if evaluate_pattern(w, guess) == pattern
            ]
            st.session_state.input_key += 1
            st.rerun()

    if st.button("💡 Hint"):
        with st.spinner("Calculating best guess..."):
            scores = find_best_guess(all_guesses, st.session_state.remaining_words)
        st.write(scores.head(5))

    if st.button("🔍 Show Solution"):
        st.write(f"Solution: {st.session_state.solution.upper()}")

# --- End-of-game popup (only if bot solution not yet requested) ---
if game.is_solved() and not st.session_state.show_bot_solution:
    win_dialog()
elif game.attempts_remaining() == 0 and not game.is_solved() and not st.session_state.show_bot_solution:
    loss_dialog()

# --- Bot solution + analysis ---
if st.session_state.show_bot_solution:
    st.divider()
    st.subheader("🤖 Bot Solution")

    with st.spinner("Solving..."):
        bot_guesses = auto_solve(
            st.session_state.solution,
            all_guesses,
            solution_words,
            first_turn_scores=first_turn_scores,
            verbose=False
        )

    bot_board_html = "".join(game.format_guess_html(g, p) for g, p, *_ in bot_guesses)
    bot_board_html += empty_row * (game.max_attempts - len(bot_guesses))
    st.html(f'<div style="display:flex;flex-direction:column;gap:0;">{bot_board_html}</div>')

    st.write(f"Bot solved in **{len(bot_guesses)}** guesses.")

    bot_df = pd.DataFrame(
        [(g.upper(), round(est, 1) if est is not None else "—", act)
         for g, p, est, act in bot_guesses],
        columns=["Guess", "Estimated Remaining", "Actual Remaining"]
    )
    st.dataframe(bot_df, hide_index=True, use_container_width=False)

    if st.session_state.game_history:
        st.subheader("📊 Your Game Analysis")
        with st.spinner("Analyzing your guesses..."):
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                analyze_game(st.session_state.game_history, all_guesses, first_turn_scores)
        st.code(buf.getvalue(), language=None)

    if st.button("🔁 Play Again"):
        st.session_state.clear()
        st.rerun()
