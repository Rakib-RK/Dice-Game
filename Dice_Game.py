import secrets
import hashlib
from dataclasses import dataclass
from typing import List, Tuple
from itertools import product
from collections import Counter

try:
  from tabulate import tabulate
except ModuleNotFoundError:
  print("The 'tabulate' library is not installed. Please install it using:")
  print("  pip install tabulate")
  print("Once installed, re-run your program.")
  exit()

class Die:
    def __init__(self, sides: List[int]):
        self.sides = sides

    def roll(self, key: bytes) -> int:
        random_value = secrets.randbelow(len(self.sides))
        hmac_value = hashlib.sha256(key + str(random_value).encode()).hexdigest()
        print(f"I selected a random value in the range 0..{len(self.sides) - 1} (HMAC={hmac_value}).")

        user_input = int(input("Add your number modulo " + str(len(self.sides)) + ": "))
        result = (random_value + user_input) % len(self.sides)
        
        print(f"My number is {random_value} (KEY={key.hex()}).")
        print(f"The result is {random_value} + {user_input} = {result} (mod {len(self.sides)}).")
        return self.sides[result]


class DiceConfigParser:
    @staticmethod
    def parse(dice_config_str: str) -> List[Die]:
        dice_configs = []
        for die_str in dice_config_str.split():
            sides = [int(side) for side in die_str.split(",")]
            dice_configs.append(Die(sides))
        return dice_configs


class ProbabilityCalculator:
    @staticmethod
    def calculate_win_probabilities(dice1: Die, dice2: Die) -> dict:
        outcomes = Counter()
        for roll1 in dice1.sides:
            for roll2 in dice2.sides:
                outcomes[roll1 > roll2] += 1
        total_outcomes = sum(outcomes.values())
        return {
            "Dice 1 Wins": outcomes[True] / total_outcomes,
            "Dice 2 Wins": outcomes[False] / total_outcomes,
            "Tie": outcomes[roll1 == roll2] / total_outcomes,
        }


class HelpTableGenerator:
    @staticmethod
    def generate_help_table(dice_configs: List[Die]) -> None:
        print("\nHelp Table: Win Probabilities for each dice pair.")
        headers = [" "] + [f"Dice {i+1}" for i in range(len(dice_configs))]
        table_data = []
        for i, die1 in enumerate(dice_configs):
            row = [f"Dice {i+1}"]
            for j, die2 in enumerate(dice_configs):
                if i == j:
                    row.append("-")
                else:
                    probs = ProbabilityCalculator.calculate_win_probabilities(die1, die2)
                    row.append(f"{probs['Dice 1 Wins']:.2f}")
            table_data.append(row)
        print(tabulate(table_data, headers=headers, tablefmt="grid"))


class DiceGame:
    def __init__(self, dice_configs: List[Die]) -> None:
        self.dice_configs = dice_configs
        self.user_score = 0
        self.computer_score = 0

    def play(self) -> None:
        while True:
            print("\nAvailable dice:")
            for i, die in enumerate(self.dice_configs):
                print(f"{i} - {die.sides}")

            user_choice = input("Choose your dice (or X to exit, ? for help): ")
            if user_choice == "X":
                break
            elif user_choice == "?":
                HelpTableGenerator.generate_help_table(self.dice_configs)
                continue
            try:
                user_choice = int(user_choice)
            except ValueError:
                print("Invalid selection. Please enter a number or 'X' or '?'.")
                continue 

            if user_choice not in range(len(self.dice_configs)):
                print("Invalid selection. Try again.")
                continue

            computer_choice = self.determine_first_move()
            user_die = self.dice_configs[user_choice]
            computer_die = self.dice_configs[computer_choice]

            print(f"\nYou chose dice {user_die.sides}. I chose dice {computer_die.sides}.")
            user_throw = user_die.roll(secrets.token_bytes(32))
            computer_throw = computer_die.roll(secrets.token_bytes(32))

            if user_throw > computer_throw:
                self.user_score += 1
                print("You win!")
            elif computer_throw > user_throw:
                self.computer_score += 1
                print("I win!")
            else:
                print("It's a tie!")

            print(f"\nCurrent score: You - {self.user_score}, Computer - {self.computer_score}")

    def determine_first_move(self) -> int:
        computer_choice = secrets.randbelow(2)
        key = secrets.token_bytes(32)
        hmac_value = hashlib.sha256(key + str(computer_choice).encode()).hexdigest()
        print(f"Let's determine who makes the first move.")
        print(f"I selected a random value in the range 0..1 (HMAC={hmac_value}).")
        while True:
            user_guess = input("Try to guess my selection (0, 1, X to exit): ")
            if user_guess == "X":
                exit()
            elif user_guess in ("0", "1"):
                user_guess = int(user_guess)
                break
            else:
                print("Invalid input. Please enter 0, 1, or X.")

        print(f"My selection: {computer_choice} (KEY={key.hex()}).")
        return computer_choice if computer_choice != user_guess else (computer_choice + 1) % 2


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python dice_game.py <dice_config1> <dice_config2> ...")
        print("Example: python dice_game.py 2,2,4,4,9,9 6,8,1,1,8,6 7,5,3,7,5,3")
        sys.exit(1)

    dice_configs = DiceConfigParser.parse(" ".join(sys.argv[1:]))
    game = DiceGame(dice_configs)
    game.play()
