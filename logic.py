import random

DIGITS = list("0123456789")


def generate_number(number_len :int ) -> str:

    first_num = str(random.choice(range(1, 10)))
    digit_pull = [num for num in DIGITS if num != first_num]
    remaining_num =  random.sample(digit_pull, number_len - 1)

    return first_num + "".join(remaining_num)

def check_answer(players_num : str, secret_num : str) -> tuple:

    # повністю вгадані
    bulls = 0
    # не вгадане місце положення
    cows = 0

    for index, num in enumerate(players_num):

        if num in secret_num:

            if index == secret_num.index(num):
                bulls += 1
            else:
                cows += 1

    return (bulls, cows)


def is_valid_guess(guess: str, number_len: int) -> bool:
    return guess.isdigit() and len(guess) == number_len