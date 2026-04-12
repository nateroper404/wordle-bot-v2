from utils import evaluate_pattern

class WordleGame:
    def __init__(self, solution: str, allowed_words: list[str], max_attempts: int = 6):
        self.solution = solution.lower()
        self.allowed_words = set(word.lower() for word in allowed_words)
        self.max_attempts = max_attempts
        self.guesses = []
        self.letter_status = {}

    """
    def evaluate_guess(self, guess: str) -> str:
        solution = self.solution
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
    """

    def make_guess(self, guess: str):
        guess = guess.lower()
        #pattern = self.evaluate_guess(guess)
        pattern = evaluate_pattern(self.solution, guess)
        self.guesses.append((guess, pattern))

        # Update keyboard state
        for letter, color in zip(guess, pattern):
            current = self.letter_status.get(letter)

            if current == "G":
                continue  # never downgrade green

            if color == "G":
                self.letter_status[letter] = "G"
            elif color == "Y" and current != "G":
                self.letter_status[letter] = "Y"
            elif color == "B" and current not in ("G", "Y"):
                self.letter_status[letter] = "B"

        return pattern

    def is_solved(self):
        if not self.guesses:
            return False
        last_guess = self.guesses[-1][0]
        return last_guess == self.solution
    
    def attempts_remaining(self):
        return self.max_attempts - len(self.guesses)
    
    def is_valid_guess(self, guess: str) -> bool:
        return guess in self.allowed_words
    
    def format_guess(self, guess: str, pattern: str) -> str:
        """
        Returns a colored string representation of guess + pattern.
        """
        color_map = {
            "G": "\033[48;5;34m",   # rich green
            "Y": "\033[48;5;220m",  # gold
            "B": "\033[48;5;240m",  # dark gray
        }

        reset = "\033[0m"

        formatted = ""
        for letter, color in zip(guess.upper(), pattern):
            formatted += f"{color_map[color]} {letter} {reset} "

        return formatted
    
    def format_keyboard(self) -> str:

        rows = [
            "QWERTYUIOP",
            "ASDFGHJKL",
            "ZXCVBNM"
        ]

        color_map = {
            "G": "\033[48;5;34m",
            "Y": "\033[48;5;220m",
            "B": "\033[48;5;240m",
            None: "\033[48;5;236m"
        }

        reset = "\033[0m"

        output = "\nKeyboard:\n\n"

        for row in rows:
            for letter in row:
                status = self.letter_status.get(letter.lower())
                output += f"{color_map[status]} {letter} {reset} "
            output += "\n"

        return output
    
    def format_keyboard_html(self) -> str:
        rows = [
            "QWERTYUIOP",
            "ASDFGHJKL",
            "ZXCVBNM"
        ]

        color_map = {
            "G": "#538d4e",
            "Y": "#b59f3b",
            "B": "#3a3a3c",
            None: "#818384"
        }

        rows_html = ""
        for row in rows:
            tiles = ""
            for letter in row:
                status = self.letter_status.get(letter.lower())
                bg = color_map[status]
                tiles += f"""
                <div style="
                    width:32px;
                    height:32px;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    font-weight:bold;
                    font-size:13px;
                    color:white;
                    background-color:{bg};
                    border-radius:4px;
                ">
                    {letter}
                </div>
                """
            rows_html += f"""
            <div style="display:flex;flex-direction:row;justify-content:center;gap:4px;margin-bottom:6px;">
                {tiles}
            </div>
            """

        return f"""
        <div style="margin-top:12px;width:100%;max-width:340px;margin-left:auto;margin-right:auto;">
            {rows_html}
        </div>
        """

    def format_guess_html(self, guess: str, pattern: str) -> str:
        color_map = {
            "G": "#538d4e",
            "Y": "#b59f3b",
            "B": "#787c7e"
        }

        tiles = ""

        for letter, color in zip(guess.upper(), pattern):
            bg = color_map[color]

            tiles += f"""
            <div style="
                width:45px;
                height:45px;
                display:flex;
                align-items:center;
                justify-content:center;
                font-weight:bold;
                color:white;
                background-color:{bg};
                border-radius:4px;
            ">
                {letter}
            </div>
            """

        return f"""
        <div style="
            display:flex;
            flex-direction:row;
            gap:4px;
            margin-bottom:4px;
        ">
            {tiles}
        </div>
        """

