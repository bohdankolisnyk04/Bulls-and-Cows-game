import tkinter as tk
from PIL import Image, ImageTk
from logic import generate_number, check_answer, is_valid_guess


def create_background(frame, image_path="main_screen.jpg"):
    """Додає фон у frame з картинкою, яка масштабована на весь розмір."""
    image = Image.open(image_path)
    image = image.resize((800, 600))
    bg_image = ImageTk.PhotoImage(image)
    bg_label = tk.Label(frame, image=bg_image)
    bg_label.image = bg_image  # щоб не зникла
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)


def create_welcome_frame(root, on_start_callback):
    frame = tk.Frame(root)

    create_background(frame)

    start_button = tk.Button(
        frame,
        text="Старт",
        font=("Helvetica", 20, "bold"),
        fg="white",
        bg="#4CAF50",
        activebackground="#45a049",
        activeforeground="white",
        relief="raised",
        bd=5,
        cursor="hand2",
        command=on_start_callback,
        width=10,
        pady=10,
    )
    start_button.place(relx=0.5, rely=0.8, anchor="center")

    # Прив'язка Enter до кнопки
    frame.bind_all("<Return>", lambda event: on_start_callback())

    return frame


def create_digit_select_frame(root, on_start_game):
    frame = tk.Frame(root)
    create_background(frame)

    label = tk.Label(frame, text="Введи кількість цифр (3-6):", font=("Arial", 18), bg="#f0f0f0")
    label.pack(pady=20)

    entry_var = tk.StringVar()
    entry = tk.Entry(frame, textvariable=entry_var, font=("Arial", 16), justify="center",
                     bd=4, relief="groove", width=5)
    entry.pack()

    error_label = tk.Label(frame, text="", fg="red", font=("Arial", 12), bg="#f0f0f0")
    error_label.pack(pady=10)

    def on_click():
        val = entry_var.get()

        if not val.isdigit():
            error_label.config(text="Введи ціле число")
            return

        number_len = int(val)

        if not (3 <= number_len <= 6):
            error_label.config(text="Число має бути від 3 до 6")
            return

        error_label.config(text="")
        secret = generate_number(number_len)
        on_start_game(number_len, secret)

    start_button = tk.Button(frame, text="Почати гру", font=("Arial", 16), command=on_click,
                             bg="#4CAF50", fg="white", activebackground="#45a049",
                             activeforeground="white", relief="raised", bd=4, cursor="hand2", width=15, pady=6)
    start_button.pack(pady=20)

    # Прив'язка Enter до кнопки
    frame.bind_all("<Return>", lambda event: on_click())

    return frame


def create_game_frame(root, number_len, secret_number, on_game_end):
    frame = tk.Frame(root)
    create_background(frame)

    label = tk.Label(frame, text=f"Введи число з {number_len} цифр:", font=("Arial", 18), bg="#f0f0f0")
    label.pack(pady=10)

    guess_var = tk.StringVar()
    guess_entry = tk.Entry(frame, textvariable=guess_var, font=("Arial", 16), justify="center",
                           bd=4, relief="groove", width=10)
    guess_entry.pack()

    message_label = tk.Label(frame, text="", fg="red", font=("Arial", 12), bg="#f0f0f0")
    message_label.pack(pady=10)

    # Frame для текстового поля з історією + скролбаром
    history_frame = tk.Frame(frame, bg="#f0f0f0")
    history_frame.pack(pady=10)

    history_text = tk.Text(history_frame, height=10, width=45, state="disabled",
                          font=("Courier", 14), bg="#4CAF50", fg="white", bd=4, relief="raised")
    history_text.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(history_frame, command=history_text.yview)
    scrollbar.pack(side="right", fill="y")
    history_text.config(yscrollcommand=scrollbar.set)

    history = []

    def add_history(guess, bulls, cows):
        history.append({"guess": guess, "bulls": bulls, "cows": cows})
        history_text.config(state="normal")
        history_text.delete("1.0", tk.END)
        for h in history:
            line = f"{h['guess']}  |  {h['bulls']} бик, {h['cows']} корова\n"
            history_text.insert(tk.END, line)
        history_text.config(state="disabled")
        history_text.see(tk.END)

    def on_check_click():
        guess = guess_var.get()

        if not is_valid_guess(guess, number_len):
            message_label.config(text=f"Введи правильне число з {number_len} унікальних цифр")
            return

        message_label.config(text="")

        bulls, cows = check_answer(guess, secret_number)
        add_history(guess, bulls, cows)

        if bulls == number_len:
            on_game_end(secret_number, len(history))
        else:
            guess_var.set("")

    check_button = tk.Button(frame, text="Перевірити", font=("Arial", 16), command=on_check_click,
                             bg="#4CAF50", fg="white", activebackground="#45a049",
                             activeforeground="white", relief="raised", bd=4, cursor="hand2", width=15, pady=6)
    check_button.pack(pady=10)

    # Прив'язка Enter до кнопки
    frame.bind_all("<Return>", lambda event: on_check_click())

    return frame



def create_end_frame(root, secret_number, attempts, on_restart, on_exit):
    frame = tk.Frame(root)
    create_background(frame)

    congrats_label = tk.Label(frame, text="Вітаємо! Ви вгадали число!", font=("Arial", 20), bg="#f0f0f0")
    congrats_label.pack(pady=20)

    secret_label = tk.Label(frame, text=f"Секретне число було: {secret_number}", font=("Arial", 16), bg="#f0f0f0")
    secret_label.pack(pady=10)

    attempts_label = tk.Label(frame, text=f"Кількість спроб: {attempts}", font=("Arial", 16), bg="#f0f0f0")
    attempts_label.pack(pady=10)

    btn_frame = tk.Frame(frame, bg="#f0f0f0")
    btn_frame.pack(pady=20)

    restart_btn = tk.Button(btn_frame, text="Грати знову", font=("Arial", 16), command=on_restart,
                            bg="#4CAF50", fg="white", activebackground="#45a049",
                            activeforeground="white", relief="raised", bd=4, cursor="hand2", width=12, pady=6)
    restart_btn.pack(side="left", padx=15)

    exit_btn = tk.Button(btn_frame, text="Вийти", font=("Arial", 16), command=on_exit,
                         bg="#f44336", fg="white", activebackground="#e53935",
                         activeforeground="white", relief="raised", bd=4, cursor="hand2", width=12, pady=6)
    exit_btn.pack(side="left", padx=15)

    # Прив'язка Enter на кнопки (Enter активує "Грати знову")
    frame.bind_all("<Return>", lambda event: on_restart())

    return frame


def run():
    root = tk.Tk()
    root.title("Bulls and Cows")
    root.geometry("800x600")
    root.resizable(False, False)

    current_frame = None

    def show_frame(frame):
        nonlocal current_frame
        if current_frame is not None:
            current_frame.pack_forget()
        current_frame = frame
        current_frame.pack(fill="both", expand=True)

    def on_welcome_start():
        show_frame(digit_select_frame)

    def on_digit_start(number_len, secret_number):
        nonlocal game_frame
        game_frame = create_game_frame(root, number_len, secret_number, on_game_end)
        show_frame(game_frame)

    def on_game_end(secret_number, attempts):
        nonlocal end_frame
        end_frame = create_end_frame(root, secret_number, attempts, on_restart, on_exit)
        show_frame(end_frame)

    def on_restart():
        show_frame(welcome_frame)

    def on_exit():
        root.destroy()

    welcome_frame = create_welcome_frame(root, on_welcome_start)
    digit_select_frame = create_digit_select_frame(root, on_digit_start)
    game_frame = None
    end_frame = None

    show_frame(welcome_frame)

    root.mainloop()
