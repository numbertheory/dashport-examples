#! /usr/bin/env python3

from dashport.dash import Dashport
from dashport.run import wrap
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--cheat', action='store_true', help='Show answer when program starts. For debugging. ;)')
args = parser.parse_args()

if not args.cheat:
    cheat_mode = False
else:
    cheat_mode = True

def show_guess_grid(app):
    guesses = ["first", "second", "third", "fourth", "fifth", "sixth"]
    grid_row = 5
    for guess in guesses:
        for i in range(0, 5):
            app.panels[f"{guess}_guess_{str(i)}"] = app.panel(height=5, width=9, y=grid_row, x=20+(i*9), border=True)
            app.print(" ", x=1, y=1, panel="first_guess_0.0")
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





def exit_program(app):
    exit(0)

def pick_word():
    with open('wordlist.txt', 'r') as f:
        data = f.readlines()
    return random.choice(data)

def dashport(stdscr):
    app = Dashport(stdscr)
    app.layout("single_panel", border=False)
    app.add_control("q", exit_program, case_sensitive=False)
    app.picked_word = pick_word()
    app.letter_list = list(app.picked_word.strip())
    show_guess_grid(app)
    show_keyboard(app)
    while True:
        app.refresh()


if __name__ == '__main__':
    wrap(dashport)
