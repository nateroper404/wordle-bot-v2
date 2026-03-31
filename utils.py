
def evaluate_pattern(solution: str, guess: str) -> str:
    solution = solution.lower()
    guess = guess.lower()

    result = [""] * 5
    unmatched = list(solution)

    # First pass: greens
    for i in range(5):
        if guess[i] == solution[i]:
            result[i] = "G"
            unmatched[i] = None
        else:
            result[i] = None

    # Second pass: yellows and grays
    for i in range(5):
        if result[i] is None:
            if guess[i] in unmatched:
                result[i] = "Y"
                unmatched[unmatched.index(guess[i])] = None
            else:
                result[i] = "B"

    return "".join(result)
