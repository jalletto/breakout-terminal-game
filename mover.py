import curses
import time
import random 
from IPython import embed

class MovableBody:
    
    def __init__(self, x = 1, y = 1, x_speed = 0, y_speed = 0):
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
        super().__init__(1, 1 , 1, 1)
    
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

class Block(MovableBody):

    def __init__(self, x, y):
        super().__init__(x, y)

    def display(self):
        return "\u2580"


class Game:
    def __init__(self):
        self.paddle = Paddle()
        self.ball = Ball()
        self.blocks = self.create_blocks()

    def create_blocks(self):
        blocks = []
        for i in range(125):
            for j in range(10):
                blocks.append(Block(i + 25, j))
        return blocks
        

    def play(self, window):
        window.nodelay(True)
        # we don't actually want to see the cursor so hide it. 
        curses.curs_set(0)
        while True:

            key = window.getch()
            window.clear()
            max_yx = window.getmaxyx()

            self.ball.check_edges(max_yx[1], max_yx[0])
            self.paddle.handle_key_press(key)
            self.ball.update()    

            if self.ball.intersect(self.paddle, 6):
                prob = random.random()
                self.ball.y_speed *= -1

            # display blocks 
            for i, block in enumerate(self.blocks):
                if self.ball.intersect(block):
                    del self.blocks[i]
                window.addstr(block.y, block.x, block.display())
            
            window.addstr(self.ball.y, self.ball.x, self.ball.display())
            window.addstr(self.paddle.y, self.paddle.x, self.paddle.display())

        
            window.refresh()
            time.sleep(.09)


def main(window):
    Game().play(window)

    
        
       

curses.wrapper(main)