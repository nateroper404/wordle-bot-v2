from wordle_game import WordleGame
from wordle_words import load_words
from utils import evaluate_pattern
from solver import find_best_guess
from solver import auto_solve
from solver import analyze_game
import random
import os
import pandas as pd

first_turn_scores = pd.read_csv("C:\\Users\\nater\\Desktop\\wordle_bot\\first_turn_scores.csv")

def main():
    
    all_guesses, solution_words = load_words(
        r"C:/Users/nater/Desktop/wordle_bot/Wordle Bot Starting Words v3.csv",
        r"C:/Users/nater/Desktop/wordle_bot/Most Common 5 Letter Words.txt",
        r"C:/Users/nater/Desktop/wordle_bot/Wordle Solution Words.txt"
    )
    
    while True: 

        #solution = random.choice(solution_words)
        #game = WordleGame(solution, all_guesses)

        #solution = input("Enter solution word (for testing): ").strip().lower()
        #random.seed(6969)
        solution = random.choice(solution_words)
        #solution = 'ivory'
        game = WordleGame(solution, all_guesses)

        remaining_words = solution_words.copy()  
        analysis_history = []


        if solution not in solution_words:
            print("Warning: solution not in official solution list.")

        game = WordleGame(solution, all_guesses)

        os.system("cls")
        
        print("\nWordle\n")
        print("\nGame started! Type 'hint' for suggestions or 'solution' to reveal the answer.\n")

        for _ in range(game.attempts_remaining()):
            print("_ _ _ _ _")

        won = False
        
        while game.attempts_remaining() > 0:

            guess = input("Enter your guess: ").strip().lower()

            # 🔎 Reveal solution and exit
            if guess == "solution":
                print(f"\n🔎 The solution is: {solution.upper()}")
                return
            
            # 💡 Hint logic
            if guess == "hint":

                print("\nCalculating best guesses...\n")

                # Optional: limit guesses for speed (can remove later)
                #candidate_guesses = all_guesses[:1000]
                candidate_guesses = all_guesses

                scores = find_best_guess(candidate_guesses, remaining_words)

                print("Top 5 suggested guesses:\n")
                top5 = scores.head(5)

                for i, row in top5.iterrows():
                    word = row["guess"].upper()
                    is_solution = row["possible_solution"]

                    tag = "(possible solution)" if is_solution == 1 else ""

                    print(f"{word:10} {tag}")

                input("\nPress Enter to continue...")

                continue

            if len(guess) != 5:
                print("Guess must be 5 letters.\n")
                continue

            if not game.is_valid_guess(guess):
                print("Not in word list.\n")
                continue

            pattern = game.make_guess(guess)

            analysis_history.append({
                "guess": guess,
                "pattern": pattern,
                "remaining_words_before": remaining_words.copy()
            })

            # 🔥 update remaining solutions
            
            remaining_words = [
                w for w in remaining_words
                if evaluate_pattern(w, guess) == pattern
            ]
            

            print("\nCurrent Board:\n")

            for g, p in game.guesses:
                print(game.format_guess(g, p))

            print()

            for _ in range(game.attempts_remaining()):
                print("_ _ _ _ _")

            print()
            print(game.format_keyboard())
            print(f"\nRemaining solutions: {len(remaining_words)}")
            #print(pattern)

            if game.is_solved():
                print("\n🎉 You solved it!")
                won = True
                break

            print(f"Attempts remaining: {game.attempts_remaining()}\n")

        # If user ran out of attempts
        if not won:
            print(f"\n❌ Game over. The word was: {solution.upper()}")

        # 🔁 Replay prompt
        while True:
            choice = input("\nPlay again? (yes / bot solve / exit): ").strip().lower()

            if choice == "yes":
                break

            elif choice == "bot solve":

                print("\n🤖 Solving...\n")

                guesses = auto_solve(solution, all_guesses, solution_words, verbose=False)

                print(f"\nSolution: {solution.upper()}\n")
                print("Auto-solve result:\n")

                # Create a temp game instance just for formatting
                display_game = WordleGame(solution, all_guesses)

                print(f"\nSolution: {solution.upper()}\n")
                print("Auto-solve result:\n")

                # Print board
                for g, p in guesses:
                    print(display_game.format_guess(g, p))

                # Fill remaining rows (optional, for full board look)
                remaining_rows = display_game.max_attempts - len(guesses)
                for _ in range(remaining_rows):
                    print("_ _ _ _ _")

                print(f"\nThe bot solved in {len(guesses)} guesses!")

                analyze_game(analysis_history, all_guesses, first_turn_scores)

                input("\nPress Enter to continue...")
                continue  # stay in replay menu

            elif choice == "exit":
                print("\nThanks for playing!")
                return

            else:
                print("Please type 'yes', 'solve', or 'exit'.")

if __name__ == "__main__":
    main()