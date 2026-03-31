
import pandas as pd
from itertools import product
from wordle_game import WordleGame
from utils import evaluate_pattern

def generate_outcomes(possible_guesses, remaining_solutions):
    """
    Create dataframe of all (guess, solution, pattern)
    """

    data = []

    for guess, sol in product(possible_guesses, remaining_solutions):
        pattern = evaluate_pattern(sol, guess)
        data.append((guess, sol, pattern))

    df = pd.DataFrame(data, columns=["guess", "solution", "pattern"])

    return df


def score_guesses(outcomes_df, remaining_solutions):
    """
    Compute expected remaining words per guess
    """

    grouped = (
        outcomes_df
        .groupby(["guess", "pattern"])
        .agg(words_remaining=("solution", "nunique"))
        .reset_index()
    )

    total = len(remaining_solutions)

    grouped["prob"] = grouped["words_remaining"] / total
    grouped["expected"] = grouped["prob"] * grouped["words_remaining"]

    scores = (
        grouped
        .groupby("guess")
        .agg(expected_words=("expected", "sum"))
        .reset_index()
    )

    # 🔥 Add possible solution flag
    remaining_set = set(remaining_solutions)
    scores["possible_solution"] = scores["guess"].apply(
        lambda x: 1 if x in remaining_set else 0
    )

    # 🔥 Sort by expected_words, then possible_solution (descending)
    scores = scores.sort_values(
        ["expected_words", "possible_solution"],
        ascending=[True, False]
    )

    return scores


def find_best_guess(possible_guesses, remaining_solutions):
    """
    Main entry point
    """

    outcomes = generate_outcomes(possible_guesses, remaining_solutions)

    scores = score_guesses(outcomes, remaining_solutions)

    return scores

from utils import evaluate_pattern
from solver import find_best_guess


def auto_solve(solution, all_guesses, solution_words, verbose=True):

    remaining_words = solution_words.copy()
    guesses = []

    # --- First guess is fixed ---
    guess = "raise"

    while True:

        pattern = evaluate_pattern(solution, guess)
        guesses.append((guess, pattern))

        # Filter remaining words
        remaining_words = [
            w for w in remaining_words
            if evaluate_pattern(w, guess) == pattern
        ]

        if verbose:
            print(f"{guess.upper()} -> {pattern} | Remaining: {len(remaining_words)}")

        # Check solved
        if guess == solution:
            break

        # Choose next guess using solver
        # Optional: restrict when small
        if len(remaining_words) <= 3:
            candidate_guesses = remaining_words
        else:
            candidate_guesses = all_guesses

        scores = find_best_guess(candidate_guesses, remaining_words)

        guess = scores.iloc[0]["guess"]

    return guesses

def analyze_game(history, all_guesses, first_turn_scores):

    print("\n📊 Post-Game Analysis\n")

    for i, step in enumerate(history, 1):

        guess = step["guess"]
        remaining_words = step["remaining_words_before"]

        print(f"\nTurn {i}")
        print(f"Your guess: {guess.upper()}")

        # Run solver for that state
        if i == 1:
            scores = first_turn_scores.copy()
        else:
            scores = find_best_guess(all_guesses, remaining_words)

        scores = scores.reset_index(drop=True)
        scores["rank"] = scores.index + 1

        # Rank
        rank = scores.index[scores["guess"] == guess][0] + 1

        # Expected words
        user_expected = scores.loc[
            scores["guess"] == guess, "expected_words"
        ].values[0]

        print(f"Rank: {rank} / {len(scores)}")
        print(f"Estimated remaining: {round(user_expected, 2)}")

        # Top 5

        print("\nTop guesses:\n")

        top5 = scores.head(5).copy()

        solution_count = top5["possible_solution"].sum()

        if solution_count < 3:

            needed = 3 - solution_count

            additional_solutions = (
                scores[
                    (scores["possible_solution"] == 1) &
                    (~scores["guess"].isin(top5["guess"]))
                ]
                .head(needed)
            )

            display_df = pd.concat([top5, additional_solutions], ignore_index=True)

        else:
            display_df = top5

        for _, row in display_df.iterrows():

            rank = int(row["rank"])
            word = row["guess"].upper()
            expected = round(row["expected_words"], 2)

            label = "(solution)" if row["possible_solution"] == 1 else ""

            print(f"{rank:>4}. {word:10} → {expected:6} {label}")

        print("-" * 40)