import settings

def get_window_size_input():
    size_map = {
        "small": 500,
        "medium": 650,
        "large": 800
    }

    while True:
        size_input = input("Enter window size (small, medium, large):\n").lower()
        if size_input in size_map:
            return size_map[size_input]
        else:
            print("Please enter 'small', 'medium', or 'large'.")


def get_speed_input():
   
    while True:
        
        user_input = input("\nSelect speed (25-200), lower is faster\nDefault (no input) is 100.\n\nSpeed: \n")
        
        if user_input.strip() == "":
            print("speed set to 100\n")
            return 100  #default
        
        try:
            speed = int(user_input)
            #hard
            if speed > 0 and speed <=50:
               print("good luck lol")
            #redundant
            elif speed == 100:
               print("couldve just entered but ok")
               print("speed set to 100\n")
            
            if 25 <= speed <= 200:
                return speed
            
            else:
               raise ValueError
            
        #not valid
        except ValueError:
            print("\n**Ivalid input**\n")

def get_unique_color_input(prompt):
    while True:
        color = input(prompt).lower()
        if color in settings.color_map:  
            return color
        else:
            print("Color is not mapped, please try another color: ")

def get_all_colors():
    
    while True:
        
        snake_color = get_unique_color_input("Set snake color: ")
        food_color = get_unique_color_input("Set food color: ")
        background_color = get_unique_color_input("Set background color: ")

        if snake_color != food_color and snake_color != background_color and food_color != background_color:
            return snake_color, food_color, background_color
        else:
            print("You cannot use the same color for more than one element. Please choose different colors.")