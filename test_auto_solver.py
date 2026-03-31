
from wordle_words import load_words
from solver import auto_solve
from wordle_game import WordleGame


def test_auto_solver():

    all_guesses, solution_words = load_words(
        r"C:/Users/nater/Desktop/wordle_bot/Wordle Bot Starting Words v3.csv",
        r"C:/Users/nater/Desktop/wordle_bot/Most Common 5 Letter Words.txt",
        r"C:/Users/nater/Desktop/wordle_bot/Wordle Solution Words.txt"
    )

    solution = "wiser"  # test case

    print(f"\nSolving for: {solution.upper()}\n")

    guesses = auto_solve(solution, all_guesses, solution_words)

    print("\nFinal result:\n")

    display_game = WordleGame(solution, all_guesses)

    # Print board
    for g, p in guesses:
        print(display_game.format_guess(g, p))

    # Fill remaining rows (optional, for full board look)
    remaining_rows = display_game.max_attempts - len(guesses)
    for _ in range(remaining_rows):
        print("_ _ _ _ _")

    print(f"\nSolved in {len(guesses)} guesses!")

    """
    for i, (g, p) in enumerate(guesses, 1):
        print(f"{i}. {g.upper()} -> {p}")

    print(f"\nSolved in {len(guesses)} guesses!")
    """


if __name__ == "__main__":
    test_auto_solver()

