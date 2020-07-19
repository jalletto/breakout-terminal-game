from moveable_body import MovableBody

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