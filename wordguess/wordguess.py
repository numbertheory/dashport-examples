#! /usr/bin/env python3

from dashport.dash import Dashport
from dashport.run import wrap

def dashport(stdscr):
    app = Dashport(stdscr)
    app.add_control("q", quit, case_sensitive=False)
    while True:
        app.refresh()


if __name__ == '__main__':
    wrap(dashport)
