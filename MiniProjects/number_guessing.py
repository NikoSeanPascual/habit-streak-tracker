import random
number = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
name = input("What is your name? ").title().strip()
attempts = 5
num_picked = random.choice(number)

while attempts > 0:
    guess = int(input(f"Guess the number {name} (0-10): "))

    if num_picked > guess:
        attempts -= 1
        print(f"Your guess is too high, you have {attempts} attempts left, guess wisely {name}.")
    elif num_picked < guess:
        attempts -= 1
        print(f"Your guess is too low, you have {attempts} attempts left, guess wisely {name}.")
    elif num_picked == guess:
        print(f"YOU GUESSED THE CORRECT NUMBER! GOOD FOR YOU {name.upper()}")
        again = input("do you wanna play again (yes/no)? ").strip().lower()
        if again == "yes":
            num_picked = random.choice(number)
            guess = int(input(f"Guess the number {name} (0-10): "))
        elif again == "no":
            print(f"Goodbye {name.title()}")
            break

print(f"YOU LOSE THE NUMBER WAS {num_picked}, TO BE HONEST IT'S SKILL ISSUES AT THIS POINT.")