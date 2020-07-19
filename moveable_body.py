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