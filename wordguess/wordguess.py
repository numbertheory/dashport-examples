#! /usr/bin/env python3

from dashport.dash import Dashport
from dashport.run import wrap
import random
import argparse
from collections import Counter

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--cheat', action='store_true', help='Show answer when program starts. For debugging. ;)')
args = parser.parse_args()

if not args.cheat:
    cheat_mode = False
else:
    cheat_mode = True

def show_guess_grid(app, **kwargs):
    guesses = ["first", "second", "third", "fourth", "fifth", "sixth"]
    grid_row = 5
    for guess in guesses:
        for i in range(1, 6):
            panel = f"{guess}_guess_{str(i)}"
            app.panels[panel] = app.panel(height=5, width=9, y=grid_row, x=10+(i*9), border=True)
        grid_row += 5

def show_keyboard(app):
    letters = [['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
               ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
               ['Z', 'X', 'C', 'V', 'B', 'N', 'M']]
    pos_x = 22
    for top_row in letters[0]:
        app.widget("button", button_name=top_row, 
                   color="black_on_white",
                   text=top_row,
                   x=pos_x, y=36, height=3, width=3, h_align="center")
        pos_x += 4

    pos_x = 24
    for middle_row in letters[1]:
        app.widget("button", button_name=middle_row, 
                   color="black_on_white",
                   text=middle_row,
                   x=pos_x, y=40, height=3, width=3, h_align="center")
        pos_x += 4

    pos_x = 28
    for bottom_row in letters[2]:
        app.widget("button", button_name=bottom_row, 
                   color="black_on_white",
                   text=bottom_row,
                   x=pos_x, y=44, height=3, width=3, h_align="center")
        pos_x += 4

def color_in_grid(app, colors, guess_position, current_guess):
    row_name = {5: "first", 10: "second", 15: "third", 20: "fourth", 25: "fifth", 30: "sixth"}
    for i in range(1, 6):
        panel = f"{row_name[guess_position]}_guess_{str(i)}"
        app.panels[panel][0].border(" ", " ", " ", " ", " ", " ", " ", " ")
        app.widget("button", button_name=panel, 
                   color=f"black_on_{colors[i - 1]}",
                   text=current_guess[i - 1],
                   x=10+(i*9), y=guess_position, height=5, width=9, h_align="center")
        app.screen.refresh()



def evaluate_guess(app):
    picked_word = list(app.picked_word)
    evaluated_result = []
    for i in range(0, len(app.current_guess)):
        
        if app.current_guess[i] == picked_word[i]:
            evaluated_result.append("green")
        elif app.current_guess[i] in picked_word:
            right_spot = 0
            occurrences_in_word = Counter(picked_word)[app.current_guess[i]]
            for j in range(0, len(app.current_guess)):
                if app.current_guess[j] == picked_word[j]:
                    right_spot += 1
            if occurrences_in_word > right_spot:
                evaluated_result.append("olive")
            else:
                evaluated_result.append("grey")
        else:
            evaluated_result.append("grey")
    app.print(f"{evaluated_result}", x=4, y=3, panel="layout.0")
    color_in_grid(app, evaluated_result, app.guess_position, app.current_guess)
    app.current_guess = []
    app.guess_position += 1
    app.guess_complete = False



def handle_guess(app, letter_pressed, guess_position):
    row_names = ["first", "second", "third", "fourth", "fifth", "sixth"]
    guess_order = []
    for row_name in row_names:
        for cell in range(1, 6):
            guess_order.append(f"{row_name}_guess_{cell}")
    if not app.guess_complete and letter_pressed != "\n":
        app.print(letter_pressed, x=4, y=2, panel=f"{guess_order[guess_position - 1]}.0")
        app.current_guess.append(letter_pressed)
    elif app.guess_complete and letter_pressed == "\n":
        evaluate_guess(app)
    if letter_pressed != "\n":
        if (app.guess_position % 5) != 0:
            app.guess_position += 1
        else:
             app.print("Confirm your guess by pressing Enter", x=4, y=2, panel="layout.0")
             app.guess_complete = True

def handle_deletion(app, guess_position):
    row_names = ["first", "second", "third", "fourth", "fifth", "sixth"]
    guess_order = []
    for row_name in row_names:
        for cell in range(1, 6):
            guess_order.append(f"{row_name}_guess_{cell}")
    app.print(" ", x=4, y=2, panel=f"{guess_order[guess_position - 2]}.0")
    app.guess_complete = False
    app.current_guess = app.current_guess[:-1]
    if (guess_position - 1) not in [0, 5, 10, 15, 20, 25]:
        app.guess_position -= 1


def pick_word():
    with open('wordlist.txt', 'r') as f:
        data = f.readlines()
    return random.choice(data)

def dashport(stdscr):
    app = Dashport(stdscr, color_names=["default", "white", "black", "silver", "grey", "olive", "yellow", "green", "red"])
    app.layout("single_panel", border=False)
    app.picked_word = pick_word()
    app.letter_list = list(app.picked_word.strip())
    if cheat_mode:
        app.print(f"Cheat Mode: {app.picked_word.strip()} | Press F1 to quit", panel="layout.0")
    else:
        app.print(f"Press F1 to quit", panel="layout.0")
    show_guess_grid(app)
    show_keyboard(app)
    app.guess_position = 1
    app.guess = 0
    app.guess_complete = False
    app.current_guess = []
    while True:
        letters = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
                   'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L',
                   'Z', 'X', 'C', 'V', 'B', 'N', 'M', '\n']
        letter_pressed = None
        letter_pressed = app.screen.getkey()
        if letter_pressed.upper() in letters:
            handle_guess(app, letter_pressed.upper(), app.guess_position)
        elif letter_pressed in ('KEY_F(1)', 'KEY_F1'):
            exit(0)
        elif letter_pressed in ('KEY_BACKSPACE', '\b', '\x7f'):
            handle_deletion(app, app.guess_position)
        else:
            app.refresh()


if __name__ == '__main__':
    wrap(dashport)
