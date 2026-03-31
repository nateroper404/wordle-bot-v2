import pandas as pd

"""
Load Wordle word banks.

Returns:
    all_guesses (list[str])
    solution_words (list[str])
"""


def load_words(
    guess_csv_path,
    common_words_path,        # ← kept for compatibility (can remove later)
    solution_words_path
):

    # ---------------------------
    # Load all possible guesses
    # ---------------------------
    guesses_df = pd.read_csv(guess_csv_path)

    all_guesses = (
        guesses_df["GUESS_WORD"]
        .str.lower()
        .str.strip()
    )

    # Ensure only valid 5-letter words
    all_guesses = [
        word for word in all_guesses
        if isinstance(word, str) and len(word) == 5
    ]

    # Remove duplicates + stabilize order
    all_guesses = sorted(set(all_guesses))


    # ---------------------------
    # Load official solution list ONLY
    # ---------------------------
    solution_words = pd.read_csv(
        solution_words_path,
        header=None
    )[0]

    solution_words = (
        solution_words
        .str.lower()
        .str.strip()
    )

    solution_words = [
        word for word in solution_words
        if isinstance(word, str) and len(word) == 5
    ]

    # Remove duplicates + stabilize order
    solution_words = sorted(set(solution_words))


    return all_guesses, solution_words

"""
def load_words(
    guess_csv_path,
    common_words_path,
    solution_words_path
):


    # ---------------------------
    # Load all possible guesses
    # ---------------------------
    guesses_df = pd.read_csv(guess_csv_path)

    all_guesses = (
        guesses_df["GUESS_WORD"]
        .str.lower()
        .str.strip()
    )

    # Ensure only valid 5-letter words
    all_guesses = [
        word for word in all_guesses
        if isinstance(word, str) and len(word) == 5
    ]


    # ---------------------------
    # Load solution sources
    # ---------------------------
    common_words = pd.read_csv(
        common_words_path,
        header=None
    )[0]

    solution_words = pd.read_csv(
        solution_words_path,
        header=None
    )[0]

    # Combine and clean
    solution_words = pd.concat(
        [common_words, solution_words],
        ignore_index=True
    )

    solution_words = (
        solution_words
        .str.lower()
        .str.strip()
    )

    solution_words = [
        word for word in solution_words
        if isinstance(word, str) and len(word) == 5
    ]

    # Remove duplicates
    solution_words = sorted(set(solution_words))


    return all_guesses, solution_words
"""