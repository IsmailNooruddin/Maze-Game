import tkinter as tk
from tkinter import messagebox
import turtle
import random


delay = 0.1

wn = turtle.Screen()
wn.bgcolor("silver")
wn.title("APS project")
wn.setup(605, 705)  # Increased vertical space for scoreboard
wn.tracer(0)
current_level = 1

# Score tracking
player_stats = {
    "score": 0,
    "lives": 3,
    "gold": 0
}
level_in_transition = False
def increase_difficulty():
    global current_level, treasures, enemies, delay, level_in_transition

    if level_in_transition:
        return  # Prevent triggering level transition if it's already in progress

    level_in_transition = True  # Set the flag to indicate level transition

    # Increase the level
    current_level += 1
    print(f"Level {current_level} begins!")

    # Pause the game and wait for player input
    wn.update()
    messagebox.showinfo("Level Up!", f"Get ready for Level {current_level}!")  # Show level-up prompt

    # Clear existing treasures and enemies
    for treasure in treasures:
        treasure.destroy()
    treasures = []

    for enemy in enemies:
        enemy.destroy()
    enemies = []

    # Adjust difficulty: increase enemy speed
    new_enemy_count = min(current_level + 1, 10)  # Increment enemies up to 10 max
    for _ in range(new_enemy_count):
        valid_positions = [(x, y) for x in range(-288, 288, 24) for y in range(288, -288, -24) if (x, y) not in walls]
        if valid_positions:
            enemy_pos = random.choice(valid_positions)
            enemy = Enemy(*enemy_pos)
            enemies.append(enemy)

    # Reset player position
    reset_player()

    # Update enemy movement speed
    for enemy in enemies:
        wn.ontimer(enemy.move, t=max(100, 250 - current_level * 20))  # Decrease time interval for movement

    # Reset delay and treasures for the new level
    for _ in range(current_level):  # Number of treasures based on the current level
        while True:
            x = random.randint(-12, 12) * 24
            y = random.randint(-12, 12) * 24
            if (x, y) not in walls:  # Ensure the position is not inside a wall
                treasures.append(Treasure(x, y))
                break

    delay = max(0.05, delay - 0.01)  # Cap minimum delay to prevent absurd speed

    # Update score display
    update_score()

    # Resume the game loop
    game_loop()

    # Reset level_in_transition flag after the delay, allowing the game to continue
    wn.ontimer(reset_level_transition_flag, 1000)
def reset_level_transition_flag():
    global level_in_transition
    level_in_transition = False  # Reset the flag after the delay



def next_level():
    global treasures, enemies, delay, current_level

    # Increment level
    current_level += 1
    print(f"Starting Level {current_level}!")

    # Show level transition message
    messagebox.showinfo("Level Up!", f"Congratulations! Proceeding to Level {current_level}")

    # Reset treasures and enemies
    for treasure in treasures:
        treasure.destroy()
    treasures = []

    for enemy in enemies:
        enemy.destroy()
    enemies = []

    # Adjust enemy speed and delay for new level
    new_enemy_speed = max(100, 250 - current_level * 20)  # Faster enemies
    delay = max(0.05, delay - 0.01)  # Reduce delay for faster game pace

    # Generate new treasures
    for _ in range(current_level):
        while True:
            x = random.randint(-12, 12) * 24
            y = random.randint(-12, 12) * 24
            if (x, y) not in walls:
                treasures.append(Treasure(x, y))
                break

    # Generate new enemies
    for _ in range(min(current_level + 1, 10)):  # Max 10 enemies
        while True:
            x = random.randint(-12, 12) * 24
            y = random.randint(-12, 12) * 24
            if (x, y) not in walls:
                enemy = Enemy(x, y)
                enemies.append(enemy)
                wn.ontimer(enemy.move, t=new_enemy_speed)
                break

    # Reset player position
    reset_player()

    # Update score display
    update_score()

    # Resume game loop
    game_loop()



# Score display
score_pen = turtle.Turtle()
score_pen.hideturtle()
score_pen.penup()
score_pen.color("black")
score_pen.goto(0, 320)  # Positioned in the empty space at the top
score_pen.write("Score: 0  Lives: 3", align="center", font=("Courier", 18, "bold"))

class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("blue")
        self.penup()
        self.speed()
        self.goto(0, 0)
        self.direction = "stop"
        self.gold = 0

    def is_collision(self, other):
        distance = self.distance(other)
        if distance < 5:  
            return True
        return False
    
def find_path(start, goal, visited=None):
    if visited is None:
        visited = {}
    
    visited[start] = True  # Mark the current pos as visitedd

    # Base case: if the start is the goal
    if start == goal:
        return [start]

    x, y = start
    neighbors = [
        (x + 24, y), (x - 24, y),  # Right, Left
        (x, y + 24), (x, y - 24)   # Up, Down
    ]

    for neighbor in neighbors:
        if neighbor not in walls and neighbor not in visited:
            path = find_path(neighbor, goal, visited)
            if path:  # If a valid path is found
                # Draw a line to the neighbor
                pen.goto(neighbor)
                pen.pendown()
                pen.goto(start)
                pen.penup()
                return [start] + path

    return None  # No path found





def go_up():
    move_to_x = player.xcor()
    move_to_y = player.ycor() + 24

    if (move_to_x, move_to_y) not in walls:
        player.goto(move_to_x, move_to_y)

def go_down():
    move_to_x = player.xcor()
    move_to_y = player.ycor() - 24

    if (move_to_x, move_to_y) not in walls:
        player.goto(move_to_x, move_to_y)

def go_left():
    move_to_x = player.xcor() - 24
    move_to_y = player.ycor()

    if (move_to_x, move_to_y) not in walls:
        player.goto(move_to_x, move_to_y)

def go_right():
    move_to_x = player.xcor() + 24
    move_to_y = player.ycor()

    if (move_to_x, move_to_y) not in walls:
        player.goto(move_to_x, move_to_y)

# marker
pen = turtle.Turtle()
pen.color("black")
pen.pensize(5)
pen.shape("square")
pen.penup()
pen.speed(0)

pen.setpos(-288, 288)
pen.setheading(0)

class Treasure(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("circle")
        self.color("gold")
        self.penup()
        self.speed(0)
        self.gold = 100
        self.goto(x, y)

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()

class Enemy(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("red")
        self.penup()
        self.speed(0)
        self.gold = 25
        self.goto(x, y)
        self.direction = random.choice(["up", "down", "left", "right"])
    
    def move(self):
        if self.direction == "up":
            dx = 0
            dy = 24
        elif self.direction == "down":
            dx = 0
            dy = -24
        elif self.direction == "left":
            dx = -24
            dy = 0
        elif self.direction == "right":
            dx = 24
            dy = 0
        else:
            dx = 0
            dy = 0

        # Calculate the movement spot of enemy
        move_to_x = self.xcor() + dx
        move_to_y = self.ycor() + dy
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)
        else:
            self.direction = random.choice(["up", "down", "left", "right"])

        wn.ontimer(self.move, t=random.randint(100, 300))
    
    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()

# Reset player position when hit by enemy
def reset_player():
    valid_positions = [(x, y) for x in range(-288, 288, 24) for y in range(288, -288, -24) if (x, y) not in walls]
    if valid_positions:
        respawn_position = random.choice(valid_positions)
        player.goto(respawn_position)



treasures = []

def load_maze_from_file(filename):
    with open(filename, 'r') as file:
        maze = [line.strip() for line in file.readlines()]
    return maze

# Load the maze from the file
level_1 = load_maze_from_file("maze_data.txt")

# Continue with the existing setup_maze function and game loop code...


walls = []
enemies = []
def setup_maze(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            character = level[y][x]
            screen_x = -288 + (x * 24)
            screen_y = 288 - (y * 24)
            if character == 'X':
                pen.goto(screen_x, screen_y)
                pen.stamp()
                walls.append((screen_x, screen_y))

            if character == 'P':
                player.goto(screen_x, screen_y)

            if character == 'T':
                treasures.append(Treasure(screen_x, screen_y))
            
            # Check if it is E representing enemies
            if character == "E":
                enemies.append(Enemy(screen_x, screen_y))

# After defining the Player class, treasures, and setup_maze
def help_player():
    player_pos = (player.xcor(), player.ycor())
    closest_treasure = None
    min_distance = float('inf')

    for treasure in treasures:
        treasure_pos = (treasure.xcor(), treasure.ycor())
        distance = abs(player_pos[0] - treasure_pos[0]) + abs(player_pos[1] - treasure_pos[1])
        if distance < min_distance:
            min_distance = distance
            closest_treasure = treasure_pos

    if closest_treasure:
        # Set up the pen for drawing
        pen.color("green")
        pen.pensize(2)
        pen.penup()
        pen.goto(player_pos)

        path = find_path(player_pos, closest_treasure)
        if path:
            print(f"Path to treasure: {path}")
        else:
            print("No path found!")

        # Reset the pen after drawing
        pen.penup()
        pen.color("black")
        pen.pensize(5)
        pen.goto(-288, 288)
    else:
        print("No treasures left!")



def update_score():
    score_pen.clear()
    score_pen.write(f"Score: {player_stats['score']}  Lives: {player_stats['lives']}  Level: {current_level}", 
                    align="center", font=("Courier", 18, "bold"))




def check_collisions():
    global treasures
    for treasure in treasures:
        if player.is_collision(treasure):
            player_stats["gold"] += treasure.gold
            player_stats["score"] += 100
            update_score()
            print(f"Player Gold: {player_stats['gold']}")
            treasure.destroy()
            treasures.remove(treasure)

    # Check if all treasures have been collected
    if not treasures:
        print(f"Level {current_level} complete!")
        # Trigger level advancement after all actions for this level are done
        wn.ontimer(increase_difficulty, t=500)  # Delay to ensure level changes smoothly

    # Check collision with enemies
    for enemy in enemies:
        if player.is_collision(enemy):
            player_stats["lives"] -= 1
            update_score()
            print(f"Player hit an enemy! Lives remaining: {player_stats['lives']}")
            if player_stats["lives"] <= 0:
                print("Game Over!")
                messagebox.showinfo("Game Over", f"Your Score: {player_stats['score']}")
                wn.bye()
            else:
                reset_player()



player = Player()
setup_maze(level_1)

# Keybindings
wn.listen()
wn.onkeypress(go_up, "w")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")
wn.onkeypress(go_down, "s")
wn.onkeypress(help_player, "h")  # Bind 'h' to help_player function

for enemy in enemies:
    wn.ontimer(enemy.move, t=250)

def game_loop():
    check_collisions()
    wn.update()  # Updates the screen
    wn.ontimer(game_loop, int(delay * 1000))  # Continue the loop after delay

# Start the game loop
game_loop()

# Starts the main event loop
wn.mainloop()