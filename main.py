import tkinter as tk
import tkinter.font as tkFont
import simpleaudio as sa
import settings
import utils
from objects import Food, Snake

pop = sa.WaveObject.from_wave_file("sound/pop.wav")
uhhhh = sa.WaveObject.from_wave_file("sound/uhhhh.wav")
direction = "down"

def start_game(event=None):
    global snake, food, canvas, instructions, title_label
    title_label.place_forget()
    instructions.place_forget()
    canvas.config(bg=settings.BACKGROUND)
    canvas.delete("all")
    snake = Snake(canvas)
    food = Food(canvas)
    setup_game()
    next_turn(snake, food)

def setup_game():
    global canvas, score, direction, score_label, window
    score = 0
    direction = 'down'
    score_label = tk.Label(window, text=f"Points: {score}", font=('consolas', 20), bg='white')
    score_label.place(x=0, y=0, width=settings.WIDTH)
    canvas.pack(fill='both', expand=True)
    load_high_score()
    update_score_label()

def game_over(): 
    global high_score, high_speed, score
    settings.game_over_flag = True
    if score > high_score:
        high_score = score
        high_speed = settings.SPEED
        save_high_score()

    canvas.delete(tk.ALL)
    display_game_over_screen()

def display_game_over_screen():
    
    
    rect_color = "black" if settings.BACKGROUND == "red" else "red"
    text_color = "white"
    rect_x1 = settings.WIDTH // 8  
    rect_y1 = settings.HEIGHT // 3  
    rect_x2 = 7 * settings.WIDTH // 8  
    rect_y2 = 2 * settings.HEIGHT // 3  

    canvas.create_rectangle(rect_x1, rect_y1, rect_x2, rect_y2, fill=rect_color, outline="black")
    canvas.create_text(settings.WIDTH // 2, settings.HEIGHT // 2 - 20, text="You died! Press 'r' to retry.", fill=text_color, font=('Helvetica', 20, 'bold'))
    highscore_text = f"Highscore: {high_score} with speed: {high_speed}"
    canvas.create_text(settings.WIDTH // 2, settings.HEIGHT // 2 + 20, text=highscore_text, fill=text_color, font=('Helvetica', 16))

def restart_game(event):
    global snake, food, score, direction, canvas
    if settings.game_over_flag:
        canvas.delete(tk.ALL)
        score = 0
        direction = 'down'
        settings.game_over_flag = False
        update_score_label()
        snake = Snake(canvas)
        food = Food(canvas)
        next_turn(snake, food)

def update_score_label():
    global score, score_label
    score_label.config(text=f"Points: {score}")

def save_high_score():
  with open('highscore.txt', 'w') as file:
    file.write(f"{high_score},{high_speed}")

def load_high_score():
    global high_score, high_speed
    try:
       with open('highscore.txt', 'r') as file:
          high_score, high_speed = map(int, file.read().split(','))
    ##no highscore file yet, make one w initial highscore,speed = 0
    except FileNotFoundError:
        high_score, high_speed = 0, 0
        with open('highscore.txt', 'w') as file:
            file.write(f"{high_score},{high_speed}")
    #file exists, cant be read, overwrite it with initial vals
    except ValueError:
        high_score, high_speed = 0, 0
        with open('highscore.txt', 'w') as file:
            file.write(f"{high_score},{high_speed}")

def create_play_button(canvas, x, y, text, command):
    button = canvas.create_text(x, y, text=text, font=("Helvetica", 80), fill="green", activefill="light green", tags = "play_button")
    canvas.tag_bind(button, "<Button-1>", command)

# Function to check the next move of snake 
def next_turn(snake, food): 
  
  global direction, canvas

  x, y = snake.coordinates[0] 

  if direction == "up": 
    y -= settings.SPACE_SIZE 
  elif direction == "down": 
    y += settings.SPACE_SIZE 
  elif direction == "left": 
    x -= settings.SPACE_SIZE 
  elif direction == "right": 
    x += settings.SPACE_SIZE 

  snake.coordinates.insert(0, (x, y)) 

  square = canvas.create_rectangle( 
    x, y, x + settings.SPACE_SIZE, 
        y + settings.SPACE_SIZE, fill=settings.SNAKE, outline = settings.SNAKE) 

  snake.squares.insert(0, square) 

  if x == food.coordinates[0] and y == food.coordinates[1]: 
    global score 
    score += 1
    pop.play()
    update_score_label()
    canvas.delete("food") 
    food = Food(canvas) 
  #creates movement effect
  else: 
    del snake.coordinates[-1] 
    canvas.delete(snake.squares[-1]) 
    del snake.squares[-1] 

  if check_collisions(snake): 
    game_over() 
    uhhhh.play()

  else: 
    window.after(settings.SPEED, next_turn, snake, food) 


# Function to control direction of snake 
def change_direction(new_direction): 
  
  global direction 

  if new_direction == 'left': 
    if direction != 'right': 
      direction = new_direction 
  elif new_direction == 'right': 
    if direction != 'left': 
      direction = new_direction 
  elif new_direction == 'up': 
    if direction != 'down': 
      direction = new_direction 
  elif new_direction == 'down': 
    if direction != 'up': 
      direction = new_direction 

# function to check snake's collision and position 
def check_collisions(snake): 
  x, y = snake.coordinates[0] 

  if x < 0 or x >= settings.WIDTH: 
    return True
  elif y < 0 or y >= settings.HEIGHT: 
    return True

  for body_part in snake.coordinates[1:]: 
    if x == body_part[0] and y == body_part[1]: 
      return True

  return False

def main():
    global canvas, window, direction, title_label, instructions

    window_size = utils.get_window_size_input()
    settings.WIDTH = window_size
    settings.HEIGHT = window_size
    settings.SPEED = utils.get_speed_input()
    settings.SNAKE, settings.FOOD, settings.BACKGROUND = utils.get_all_colors()

    window = tk.Tk()
    window.title("Snake Game")
    
    canvas = tk.Canvas(window, height=settings.HEIGHT, width=settings.WIDTH, bg='black')
    canvas.pack()

    # Create the title label and instructions directly in the window
    pixel_style_font = tkFont.Font(family="Helvetica", size=36, weight="bold")
    title_label = tk.Label(window, text="SNAKE", fg="green", bg="black", font=pixel_style_font)
    title_label.pack()
    instructions = tk.Label(window, text="Click play or press the arrow to begin:", fg="white", bg="black", font=('Helvetica', 10))
    instructions.pack()

    # Place title_label and instructions in the window
    title_label.place(x=settings.WIDTH // 2, y=settings.HEIGHT // 4, anchor="center")
    instructions.place(x=settings.WIDTH // 2, y=settings.HEIGHT - 30, anchor="center")

    # Create play button and bind keys
    create_play_button(canvas, settings.WIDTH // 2, settings.HEIGHT // 2, u"\u25B6", start_game)

    window.bind('<Left>', lambda event: change_direction('left'))
    window.bind('<Right>', lambda event: change_direction('right'))
    window.bind('<Up>', lambda event: change_direction('up'))
    window.bind('<Down>', lambda event: change_direction('down'))
    window.bind('r', restart_game)

    window_size_padding = 40
    window.geometry(f"{settings.WIDTH}x{settings.HEIGHT + window_size_padding}")
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (settings.WIDTH // 2)
    y = (screen_height // 2) - ((settings.HEIGHT + window_size_padding) // 2)
    window.geometry(f"+{x}+{y}")

    window.mainloop()

if __name__ == "__main__":
    main()
