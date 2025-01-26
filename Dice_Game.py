import random
from collections import Counter
from itertools import product

def validate_dice(dice):
    if not isinstance(dice, list) or len(dice) < 1:
        raise ValueError("Dice must be a list with at least one die.")
    for die in dice:
        if not isinstance(die, list) or len(die) != 6 or not all(isinstance(x, int) for x in die):
            raise ValueError("Each die must be a list of 6 integers.")

def roll_dice(dice):
    return [random.choice(die) for die in dice]

def calculate_probabilities(dice):
    outcomes, total_rolls = Counter(), 0
    for roll in product(*dice):
        outcomes[sum(roll)] += 1
        total_rolls += 1
    return {s: round(count / total_rolls, 4) for s, count in outcomes.items()}

def display_probabilities(probabilities):
    print("\nHelp Table - Probabilities for 3 Dice (Sum -> Probability):")
    for s, prob in sorted(probabilities.items()):
        print(f"  {s} -> {prob}")

def initialize_game(dice):
    try:
        validate_dice(dice)
        return True
    except ValueError as e:
        print(f"Error: {e}")
        return False

def play_game(dice, rounds):
    print(f"\n--- Starting the Dice Game ---\nDice configuration: {dice}")
    if not initialize_game(dice):
        return
    probabilities = calculate_probabilities(dice[:3])
    display_probabilities(probabilities)
    total_user_score, total_computer_score = 0, 0
    for round_num in range(1, rounds + 1):
        print(f"\n--- Round {round_num} ---")
        computer_roll, user_roll = roll_dice(dice), roll_dice(dice)
        computer_sum, user_sum = sum(computer_roll), sum(user_roll)
        print(f"Computer rolled: {computer_roll} (Sum: {computer_sum})")
        print(f"User rolled: {user_roll} (Sum: {user_sum})")
        if computer_sum > user_sum:
            print("Computer wins this round!")
            total_computer_score += 1
        elif user_sum > computer_sum:
            print("User wins this round!")
            total_user_score += 1
        else:
            print("It's a tie!")
    print(f"\nFinal Scores: User - {total_user_score}, Computer - {total_computer_score}")
    if total_user_score > total_computer_score:
        print("User wins the game!")
    elif total_computer_score > total_user_score:
        print("Computer wins the game!")
    else:
        print("The game ends in a tie!")

if __name__ == "__main__":
    print("Welcome to the Dice Game!")
    standard_dice = [[1, 2, 3, 4, 5, 6]] * 4
    custom_dice = [[2, 2, 4, 4, 9, 9], [1, 1, 6, 6, 8, 8], [3, 3, 5, 5, 7, 7]]

    while True:
        print("\nChoose your dice configuration:")
        print("1. Play with 4 standard dice (1-6)")
        print("2. Play with 3 custom dice")
        print("3. Quit")
        choice = input("Enter your choice (1, 2, or 3): ").strip()
        
        if choice == "1":
            dice = standard_dice
        elif choice == "2":
            dice = custom_dice
        elif choice == "3":
            print("Thanks for playing!")
            break
        else:
            print("Invalid input. Please choose 1, 2, or 3.")
            continue
        
        try:
            rounds = int(input("How many rounds would you like to play? ").strip())
            if rounds < 1:
                print("Please enter a positive number of rounds.")
                continue
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        play_game(dice, rounds)
        
        replay = input("\nDo you want to play again? (yes or no): ").strip().lower()
        if replay not in ["yes", "y"]:
            print("Goodbye!")
            break
