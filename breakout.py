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
        super().__init__(4, 4 , 1, 1)
    
    def display(self):
        return "\u25CF"

    def check_edges(self, max_width, max_height):
        if self.x <= 0 or self.x >= max_width - 2: 
            self.x_speed *= -1
        
        if self.y <= 0 or self.y >= max_height - 2:
            self.y_speed *= -1

    

class Paddle(MovableBody):

    def __init__(self):
        super().__init__(20, 20, 6, 6)

    def handle_key_press(self, key):
        if key == curses.KEY_LEFT:
            if self.x > 2:
                self.x -= self.x_speed
        elif key == curses.KEY_RIGHT:
            self.x += self.x_speed
    
    
    def display(self):
        return "\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550"


class Block(MovableBody):

    def __init__(self, x, y):
        super().__init__(x, y)

    def display(self):
        return "\u2580\u2580\u2580"


class Game:
    def __init__(self, window):
        self.window = window
        self.paddle = Paddle()
        self.ball = Ball()
        self.create_blocks()

    def create_blocks(self):
        blocks = []
        for i in range(50):
            for j in range(4,10):
                if i % 2 == 0:
                    blocks.append(Block(i * 2 + 20, j))
        self.blocks = blocks

    def ball_intersects_paddle(self):
        if self.ball.intersect(self.paddle, 6):
            prob = random.random()
            self.ball.y_speed *= -1

            if prob > .8:
                self.ball.x_speed *= -1

    def check_block_hit(self):
        for i, block in enumerate(self.blocks):
            if self.ball.intersect(block, 1):
                del self.blocks[i]
                self.ball.y_speed *= -1
    
    def display_blocks(self):
        for i, block in enumerate(self.blocks):
            self.window.addstr(block.y, block.x, block.display())
        


        

    def play(self):
        self.window.nodelay(True)
        # we don't actually want to see the cursor so hide it. 
        refresh = 0
        curses.curs_set(0)
        while True:
            refresh += 1
            key = self.window.getch()
            self.window.clear()
            max_yx = self.window.getmaxyx()
            
            self.ball.check_edges(max_yx[1], max_yx[0])
            self.paddle.handle_key_press(key)

            self.ball_intersects_paddle()

            self.ball.update()    
            self.check_block_hit()
            self.display_blocks()
            
            self.window.addstr(self.ball.y, self.ball.x, self.ball.display())
            self.window.addstr(self.paddle.y, self.paddle.x, self.paddle.display())
            # ball_xy = f"ball xy: {str((self.ball.x, self.ball.y))}"
            # self.window.addstr(2,2, ball_xy)
            # self.window.addstr(5,2, f'refreshes: {refresh}')

        
            self.window.refresh()
            time.sleep(.09)


def main(window):
    Game(window).play()

    
        
       

curses.wrapper(main)