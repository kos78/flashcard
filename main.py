from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"

df = pd.DataFrame
try:
    words = pd.read_csv("data/words to learn.csv")
    to_learn = df.to_dict(words, orient='records')
except FileNotFoundError:
    original_data = pd.read_csv("data/Japanese words - Sheet1.csv")
    to_learn = df.to_dict(original_data, orient='records')



current_card = {}
first_word = random.choice(to_learn)


def next_card():
    global current_card, flip_timer
    """Chooses a japanese word at random to display on the card"""
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="Japanese", fill="black")
    canvas.itemconfig(card_word, text=current_card["Japanese"], fill="black")
    canvas.itemconfig(card_background, image=front_card)
    flip_timer = window.after(ms=3000, func=flip_cards)


def flip_cards():
    canvas.itemconfig(card_background, image=back_card)
    canvas.itemconfig(card_title, fill="white", text="English")
    canvas.itemconfig(card_word, fill="white", text=current_card["English"])


def save_progress():
    """to save progress by removing cards seen from the csv and creating a csv of words that haven't been learned"""
    to_learn.remove(current_card)
    next_card()
    print(len(to_learn))
    data = pd.DataFrame(to_learn)
    data.to_csv("data/words to learn.csv",index=False)


# -------------- UI SETUP -------------------#

window = Tk()
window.title("Flashcards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(ms=3000, func=flip_cards)

canvas = Canvas(width=800, height=526)

front_card = PhotoImage(file="images/card_front.png")
right = PhotoImage(file="images/right.png")
wrong = PhotoImage(file="images/wrong.png")
back_card = PhotoImage(file="images/card_back.png")

card_background = canvas.create_image(400, 263, image=front_card)
card_title = canvas.create_text(400, 150, text="Japanese", font=("Arial", 25, "bold"))
card_word = canvas.create_text(400, 263, text="word", font=("Arial", 25, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)

right_button = Button(image=right, highlightthickness=0, command=save_progress)
right_button.grid(column=1, row=1)
wrong_button = Button(image=wrong, highlightthickness=0, command=next_card)
wrong_button.grid(column=0, row=1)

right_button.bind("Save", save_progress)

window.mainloop()
