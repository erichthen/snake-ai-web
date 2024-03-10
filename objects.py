import random
import settings


class Snake: 
    def __init__(self, canvas): 
        self.body_size = settings.BODY_SIZE 
        self.coordinates = [] 
        self.squares = [] 

        for i in range(0, settings.BODY_SIZE): 
            self.coordinates.append([0, 0]) 

        for x, y in self.coordinates: 
            square = canvas.create_rectangle(x, y, x+settings.SPACE_SIZE, y+settings.SPACE_SIZE, fill=settings.SNAKE, outline=settings.SNAKE, tag="snake") 
            self.squares.append(square)

class Food: 
    def __init__(self, canvas): 
        x = random.randint(0, (settings.WIDTH // settings.SPACE_SIZE) - 1) * settings.SPACE_SIZE
        y = random.randint(0, (settings.HEIGHT // settings.SPACE_SIZE) - 1) * settings.SPACE_SIZE 

        self.coordinates = [x, y] 

        canvas.create_rectangle(x, y, x + settings.SPACE_SIZE, y + settings.SPACE_SIZE, fill=settings.FOOD, tag="food") 