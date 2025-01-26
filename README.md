# Dice-Game

Description
This project implements a collaborative dice-rolling protocol ensuring fairness through the use of cryptographic HMACs. It supports multiple dice configurations, modular arithmetic for result calculation, and probability table generation for analysis.

How to Run:

Clone the repository:

(https://github.com/Rakib-RK/Dice-Game)

Install dependencies:

pip install -r requirements.txt

Run the program with desired configurations:

python dice_game.py

To display the help table or run tests with invalid parameters, follow features below.

Features:

1. Fairness Protocol: Uses HMAC to ensure unbiased random number generation.
   
2. Modular Arithmetic: Combines user and computer inputs for uniform result distribution.
   
3. Probability Table: Calculates and displays winning probabilities for different dice configurations.
   
4. Error Handling: Manages invalid inputs, including malformed dice configurations and missing parameters.
