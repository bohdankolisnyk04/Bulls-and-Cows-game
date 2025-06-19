from logic import generate_number, check_answer, is_valid_guess


def start_game():

    print(" Вітаю в грі \"Бики та Корови\", введіть кількість цифр в числі, яке хочете відгадувати")
    number_length = int(input())

    code_number = generate_number(number_length)

    while True:

        print(" Введіть ваше число")
        user_input = str(input())

        while is_valid_guess(user_input, number_length) is False:
            print("Введіть будь ласка число з заданою довжиною")
            user_input = str(input())



        bulls , cows = check_answer(user_input, code_number)

        print(f"В числі {bulls} бика та {cows} корів")

        if (bulls == number_length):
            print(f"Ви перемогли! Вітаю")
            break
        else:
            print("Спробуйте далі! ")

    print(f"Хочеш спробувати ще?")
    if str(input()) == "так":
        start_game()
    else:
        print("До зустрічі")