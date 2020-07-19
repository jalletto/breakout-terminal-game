import curses

def main(window):
    while True: 
        win = curses.newwin(20, 20, 3, 50)
        win.border()


curses.wrapper(main)