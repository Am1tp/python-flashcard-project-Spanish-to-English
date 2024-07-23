from tkinter import *
from os.path import exists
import pandas as pd

FLIP_TIME = 3000 # adjust time before new card
BACKGROUND_COLOR = "#B1DDC6"

# create dataframe from file
if exists("data/Words_to_learn.csv"): # check if programme has been previously run
    data = pd.read_csv("data/Words_to_learn.csv")
    df = pd.DataFrame(data)
else:
    data = pd.read_csv("data/500 Spanish English.csv")  # otherwise load data from default file
    df = pd.DataFrame(data)

flip_timer = None
# global variable to keep track of schedules card flips. allows management of the timing for card flips independently
# of button presses, loop created to continuously display new cards and flip, if user choses to interact or not


def new_word():
    """Uses Words_to_learn data to select a random word, accesses the Spanish and English words to display the
    Spanish word on the 'front' and the English translation on the 'back'. After FLIP_TIME the card_front changes
     to card_back by calling flip_card() """
    global random_word, english_word, flip_timer

    if flip_timer is not None:
        window.after_cancel(flip_timer)

    random_word = df.sample()
    index = random_word.index
    spanish_word = random_word.Spanish  # obtain Spanish word from row
    english_word = random_word.English  # obtain English word from row

    canvas.itemconfig(canvas_img, image=card_front)
    canvas.itemconfig(title, text="Spanish", font=("ariel", 40, "italic"), fill="black")
    canvas.itemconfig(word, text=f"{spanish_word.to_string(index=False)}", font=("ariel", 60, "bold"), fill="black")

    flip_timer = window.after(FLIP_TIME, flip_card)


def flip_card():
    """Flips the card from Spanish side to English side"""
    canvas.itemconfig(canvas_img, image=card_back)
    canvas.itemconfig(title, text="English", font=("ariel", 40, "italic"), fill="white")
    canvas.itemconfig(word, text=f"{english_word.to_string(index=FALSE)}", font=("ariel", 60, "bold"), fill="white")

    flip_timer = window.after(FLIP_TIME, new_word)


def word_learnt():
    """Once user presses the 'tick' button, the word is deemed as learnt and is removed from the data file"""
    index = random_word.index[0]
    if exists("data/Words_to_learn.csv"):
        wtl_data = pd.read_csv("data/Words_to_learn.csv")
        df = pd.DataFrame(wtl_data)
        df = df.drop(index)
        df.to_csv("data/Words_to_learn.csv", index=False)
    else:
        wtl_data = pd.read_csv("data/500 Spanish English.csv")
        df = pd.DataFrame(wtl_data)
        df = df.drop(index)
        df.to_csv("data/Words_to_learn.csv", index=False)

    new_word()


# window settings
window = Tk()

window.title("Flashy")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

# canvas settings
canvas = Canvas(height=526, width=800, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
canvas_img = canvas.create_image(400, 263, image=card_front)
title = canvas.create_text(400, 150, text="Title", font=("ariel", 40, "italic"))
word = canvas.create_text(400, 263, text="word", font=("ariel", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

# buttons
right_button_img = PhotoImage(file="images/right.png")
wrong_button_img = PhotoImage(file="images/wrong.png")
right_button = Button(image=right_button_img, highlightthickness=0, command=word_learnt) # 'tick' button
right_button.grid(column=1, row=1)
wrong_button = Button(image=wrong_button_img, highlightthickness=0, command=new_word) # 'cross' button
wrong_button.grid(column=0, row=1)

new_word()

window.mainloop()
