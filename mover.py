import curses
import time
import random 
import math
from IPython import embed

class Vector:
    def __init__(self, x = 0, y = 0):
        self.x = x 
        self.y = y

    def add(self, vector):
        self.x += vector.x
        self.y += vector.y
    
    def sub(self, vector):
        self.x -= vector.x 
        self.y -= vector.y

    def mult(self, n):
        self.x *= n
        self.y *= n

    def div(self, n):
        self.x /= n 
        self.y /= n 

    def mag(self):
        return math.sqrt(self.x * self.y)

    def normalize(self):
        mag = self.mag()
        self.div(mag)
    
    def limit(self, limit):
        if self.mag() > limit:
            self.normalize()
            self.mult(limit)


class MovableBody:
    
    def __init__(self, x = 1, y = 1):
        self.location     = Vector(x, y)
        self.velocity     = Vector(1, 1)
        self.acceleration = Vector(1, 1)

    def update(self):
        self.velocity.add(self.acceleration)
        self.velocity.limit(1)
        self.location.add(self.velocity)

    def intersect(self, body, x_off = 0, y_off = 0):
        return body.location.x >= self.location.x - x_off and body.location.x <= self.location.x + x_off and body.location.y >= self.location.y - y_off and body.location.y <= self.location.y + y_off

    def check_edges(self, max_width, max_height):
        if self.location.x <= 0 or self.location.x >= max_width - 1: 
            self.velocity.x *= -1
        
        if self.location.y <= 0 or self.location.y >= max_height - 1:
            self.velocity.y *= -1

    def display(self):
        return '0'


def main(window):
    m = MovableBody()

    window.nodelay(True)
    curses.curs_set(0)


    while True: 
        window.clear()

        key = window.getch()
        max_yx = window.getmaxyx()
        m.check_edges(max_yx[1], max_yx[0])
        m.update()

        mover_xy = f"Mover xy: {str((m.location.x, m.location.y))}"
        window.addstr(2,2, mover_xy)
        window.addstr(m.location.x, m.location.y, m.display())
        
        window.refresh()
        time.sleep(.09)

    
        
       

curses.wrapper(main)


