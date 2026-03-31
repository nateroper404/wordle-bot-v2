from wordle_words import load_words
from solver import find_best_guess
from utils import evaluate_pattern


def test_solver():

    all_guesses, solution_words = load_words(
        r"C:/Users/nater/Desktop/wordle_bot/Wordle Bot Starting Words v3.csv",
        r"C:/Users/nater/Desktop/wordle_bot/Most Common 5 Letter Words.txt",
        r"C:/Users/nater/Desktop/wordle_bot/Wordle Solution Words.txt"
    )

    #all_guesses = all_guesses[:500]
    all_guesses = all_guesses

    # Start with full solution space
    remaining_words = solution_words.copy()

    """
    # Simulate first guess
    guess = "stare"
    solution = "slick"

    pattern = evaluate_pattern(solution, guess)

    print("Guess:", guess)
    print("Pattern:", pattern)

    # Filter remaining words
    remaining_words = [
        w for w in remaining_words
        if evaluate_pattern(w, guess) == pattern
    ]

    print("Remaining words:", len(remaining_words))
    """


    # Run solver
    scores = find_best_guess(all_guesses, remaining_words)

    print("\nTop 10 guesses:")
    print(scores.head(50))


if __name__ == "__main__":
    test_solver()

