import curses
import time
from IPython import embed

class MovableBody:
    
    def __init__(self, x = 1, y = 1, x_speed = 1, y_speed = 1):
        self.x = x
        self.y = y
        self.x_speed = x_speed
        self.y_speed = y_speed

    def update(self):
        self.x += self.x_speed
        self.y += self.y_speed

    def intersect(self, body, x_off = 0, y_off = 0):
        return body.x >= self.x - x_off and body.x <= self.x + x_off and body.y >= self.y - y_off and body.y <= self.y + y_off


class Ball(MovableBody): 

    def __init__(self):
        super().__init__()
    
    def display(self):
        return "\u25CF"

    def check_edges(self, max_width, max_height):
        if self.x <= 0 or self.x >= max_width - 1: 
            self.x_speed *= -1
        
        if self.y <= 0 or self.y >= max_height - 1:
            self.y_speed *= -1
    

class Paddle(MovableBody):

    def __init__(self):
        super().__init__(20, 20, 3, 3)

    def handle_key_press(self, key):
        if key == curses.KEY_LEFT:
            self.x -= self.x_speed
        elif key == curses.KEY_RIGHT:
            self.x += self.x_speed
    
    def display(self):
        return "\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550"


# class Window(curses):
#     def __init__(self):
#         pass 


class Game:
    def __init__(self):
        self.paddle = Paddle()
        self.ball = Ball()
    

    def play(self, window):
        window.nodelay(True)
        curses.curs_set(0)
        while True:
            # we don't actually want to see the cursor so hide it. 

            key = window.getch()
            window.clear()
            max_yx = window.getmaxyx()
            # embed()
            self.ball.check_edges(max_yx[1], max_yx[0])
            self.paddle.handle_key_press(key)
            self.ball.update()    

            if self.ball.intersect(self.paddle, 6):
                self.ball.y_speed *= -1

            # display
            window.addstr(self.ball.y, self.ball.x, self.ball.display())
            window.addstr(self.paddle.y, self.paddle.x, self.paddle.display())

        
            window.refresh()
            time.sleep(.09)


def main(window):
    Game().play(window)

    
        
       

curses.wrapper(main)