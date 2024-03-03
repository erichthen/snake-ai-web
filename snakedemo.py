# Program in Python to create a Snake Game 

from tkinter import *
import random 

# Initialising Dimensions of Game 
WIDTH = 500
HEIGHT = 500
SPEED = 200
SPACE_SIZE = 20
BODY_SIZE = 2
SNAKE = "#00FF00"
FOOD = "#FFFFFF"
BACKGROUND = "#000000"

# Class to design the snake 
class Snake: 

  def __init__(self): 
    self.body_size = BODY_SIZE 
    self.coordinates = [] 
    self.squares = [] 

    for i in range(0, BODY_SIZE): 
      self.coordinates.append([0, 0]) 

    for x, y in self.coordinates: 
      square = canvas.create_rectangle( x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE, tag="snake") 
      self.squares.append(square) 

# Class to design the food 
class Food: 

  def __init__(self): 

    x = random.randint(0, 
        (WIDTH / SPACE_SIZE)-1) * SPACE_SIZE 
    y = random.randint(0, 
        (HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE 

    self.coordinates = [x, y] 

    canvas.create_oval(x, y, x + SPACE_SIZE, y +
            SPACE_SIZE, fill=FOOD, tag="food") 

# Function to check the next move of snake 
def next_turn(snake, food): 

  x, y = snake.coordinates[0] 

  if direction == "up": 
    y -= SPACE_SIZE 
  elif direction == "down": 
    y += SPACE_SIZE 
  elif direction == "left": 
    x -= SPACE_SIZE 
  elif direction == "right": 
    x += SPACE_SIZE 



window = Tk()
score = 0
window.title("Snake Game")
direction = 'down'

label = Label(window, text = "Points:{}".format(score), font = ('consolas', 20))
canvas = Canvas(window, bg = BACKGROUND, height = HEIGHT, width = WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
