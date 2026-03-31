
from wordle_words import load_words
from solver import find_best_guess
import pandas as pd


def precompute_first_turn():

    all_guesses, solution_words = load_words(
        r"C:/Users/nater/Desktop/wordle_bot/Wordle Bot Starting Words v3.csv",
        r"C:/Users/nater/Desktop/wordle_bot/Most Common 5 Letter Words.txt",
        r"C:/Users/nater/Desktop/wordle_bot/Wordle Solution Words.txt"
    )

    print("Running first-turn optimization... (this may take a while)")

    scores = find_best_guess(all_guesses, solution_words)

    # Save results
    output_path = "first_turn_scores.csv"
    scores.to_csv(output_path, index=False)

    print(f"\nSaved results to {output_path}")
    print("\nTop 10 starting guesses:")
    print(scores.head(10))


if __name__ == "__main__":
    precompute_first_turn()

