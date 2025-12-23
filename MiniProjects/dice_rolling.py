import random

def roll_dice():
    dice = {
        1: [
            ".---------.",
            "|    1    |",
            "|    ○    |",
            "|         |",
            ".---------."
        ],
        2: [
            ".---------.",
            "|  ○      |",
            "|    2    |",
            "|      ○  |",
            ".---------."
        ],
        3: [
            ".---------.",
            "|  ○      |",
            "|    ○    |",
            "|      ○  |",
            ".---------."
        ],
        4: [
            ".---------.",
            "|  ○   ○  |",
            "|    4    |",
            "|  ○   ○  |",
            ".---------.",
        ],
        5: [
            ".---------.",
            "|  ○ 5 ○  |",
            "|    ○    |",
            "|  ○   ○  |",
            ".---------."
        ],
        6: [
            ".---------.",
            "|  ○   ○  |",
            "|  ○ 6 ○  |",
            "|  ○   ○  |",
            ".---------."
        ]
    }
    roll = input("Roll the dice ? (yes/no)").lower().strip()

    while roll == "yes":
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        print("\n".join(dice[1]))
        print("\n".join(dice[2]))

        print("Dice rolled: {} and {}".format(dice1, dice2))

        roll = input("Roll again? (yes/no").lower().strip()

roll_dice()