import pygame  # Importing the pygame library
import random  # Importing the random module for generating random numbers
import time  # Importing the time module for time-related functions
import sys  # Importing the sys module for system-specific parameters and functions

# Constants defining the screen properties and colors
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
GRID_SIZE = 3
COLOR1 = 'goldenrod'  # Setting color constant for later use
COLOR2 = (209, 17, 33)  # Defining RGB color for later use (red)
COLOR3 = (18, 18, 18)  # Defining RGB color for later use (dark gray)
PYTHON_IMAGE_PATH = 'python1.png'  # Path to the python image
LOSE_IMAGE_PATH = 'python2.png'  # Path to the lose image
MAIN_MUSIC_PATH = "main_music.mp3"  # Path to the main music file
SMACK_SOUND_PATH = 'SMACK Sound Effect.mp3'  # Path to the smack sound effect file
WINNER_MUSIC_PATH = "Winner_Music.mp3"  # Path to the winner music file
LOSER_MUSIC_PATH = "Loser_Music.mp3"  # Path to the loser music file

# Initialize pygame modules
pygame.init()  # Initializing the pygame module
pygame.mixer.init()  # Initializing the mixer module for sound handling

# Load game resources
python_image = pygame.transform.scale(pygame.image.load(PYTHON_IMAGE_PATH), (int(5.5 * 400 / 12), int(5.5 * 400 / 12)))  # Loading and scaling the python image
lose_image = pygame.transform.scale(pygame.image.load(LOSE_IMAGE_PATH), (int(1.2 * 305), int(1.2 * 361)))  # Loading and scaling the lose image
pygame.mixer.music.load(MAIN_MUSIC_PATH)  # Loading the main music file
smack_sound = pygame.mixer.Sound(SMACK_SOUND_PATH)  # Loading the smack sound effect

# Start playing the main music in an indefinite loop
pygame.mixer.music.play(-1)

# Set up the game window with defined screen width and height
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Creating the game window
clock = pygame.time.Clock()  # Creating an object to help track time in the game


class Python:
    """
    Represents a python object in the 'Whack-A-Python' game

    Attributes:
        image (pygame.Surface): The image of the python displayed on the screen
        position (tuple): X and Y coordinates of the python on the screen
        visible (bool): Status of python's visibility on the screen
    """
    def __init__(self, image, position):
        """
        Initializes the Python object with an image and a starting position

        Args:
            image (pygame.Surface): The image of the python
            position (tuple): Starting X and Y coordinates for the python
        """
        self.image = image # Image of the python
        self.position = position # Starting position of the python
        self.visible = False  # Initially, the python is not visible

    def appear(self):
        # Makes the python visible
        self.visible = True

    def hide(self):
        # Makes the python invisible
        self.visible = False

    def draw(self, screen):
        # Draws the python on the screen if it is visible
        if self.visible:
            screen.blit(self.image, self.position)


class Grid:
    """
    Represents the grid layout for the python objects in the game

    Attributes:
        positions (list of tuples): List of X, Y coordinate tuples for python positions
    """
    def __init__(self, size):
        # A list of positions for the pythons. These positions are like spots in a 3x3 grid.
        self.positions = [(x, y) for x in range(110, 550, 199) for y in range(150, 550, 199)]


class Player:
    """
    Represents the player in the game, tracking score and misses

    Attributes:
        score (int): The player's current score
        missed (int): The number of pythons missed by the player
    """
    def __init__(self):
        # Initializes the Player object with a score and missed count
        self.score = 0  # Initializes the score as 0
        self.missed = 0  # Tracks missed pythons

    def hit_python(self):
        # Increments the score when a python is hit
        self.score += 1

    def miss_python(self):
        # Increments the missed count when a python is missed
        self.missed += 1
    

class Scoreboard:
    """
    Manages the display of the player's score and missed count in the game

    Attributes:
        font (pygame.font.Font): Font used for displaying the score and misses
        current_color (tuple): Current color of the score text
    """
    def __init__(self):
        # Initializes the Scoreboard object with a specific font and color
        self.font = pygame.font.SysFont('niagarasolid', 65)  # Initializes the font for the scoreboard
        self.current_color = COLOR1  # Sets the default color for the scoreboard

    def display_score(self, score, screen):
        # Displays the current score
        if score % 10 == 0 and score != 0 and score != 40:
            self.current_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            # Changes the color randomly if the score is a multiple of 10 but not 0 or 40
        else:
            self.current_color = COLOR1  # Resets the color to default if conditions aren't met
        score_text = self.font.render(f'Score: {score}', True, self.current_color)
        # Renders the score text with the current color
        screen.blit(score_text, (45, 25))  # Displays the score text on the screen at a specific position

    def display_missed_count(self, missed, screen):
        # Displays the missed count
        missed_text = self.font.render(f'Missed: {missed}', True, COLOR2)
        # Renders the missed count text with a specific color
        screen.blit(missed_text, (610, 25))  # Displays the missed count text on the screen at a specific position


def button(screen, msg, x, y, w, h, inactive_color, active_color, action=None):
    # Function to create a button on the screen and handle its behavior
    mouse = pygame.mouse.get_pos()  # Get the current mouse position
    click = pygame.mouse.get_pressed()  # Get mouse click status
    if x + w > mouse[0] > x and y + h > mouse[1] > y:  # Check if the mouse is hovering over the button
        pygame.draw.rect(screen, active_color, (x, y, w, h))  # Draw the button in active color
        if click[0] == 1 and action is not None:  # Check if the button is clicked
            action()  # Perform the specified action (e.g., function call)
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, w, h))  # Draw the button in inactive color

    small_font = pygame.font.SysFont("niagarasolid", 40)  # Define a smaller font for the button text
    text_surf = small_font.render(msg, True, COLOR3)  # Render the button text surface
    text_rect = text_surf.get_rect(center=(x + w / 2, y + h / 2))  # Set the button text position
    screen.blit(text_surf, text_rect)  # Display the button text on the screen

def show_main_menu(screen):
    running = True

    def stop_running():
        nonlocal running
        running = False

    while running:
        screen.fill((4, 56, 43))  # Fill the screen with a specific color

        # Displaying the text "WHACK-A-PYTHON" on the screen
        whack_text = pygame.font.SysFont('niagarasolid', 70).render('WHACK-A-PYTHON', True, COLOR1)
        screen.blit(whack_text, (SCREEN_WIDTH // 2 - whack_text.get_width() // 2, 220))

        # Create 'Play' and 'Exit' buttons on the screen
        button(screen, 'Play', 350, 350, 100, 50, COLOR1, COLOR2, stop_running)
        button(screen, 'Exit', 350, 450, 100, 50, COLOR1, COLOR2, pygame.quit)
        
        pygame.display.flip()  # Update the display
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Quit the game if the window is closed
                return False
        clock.tick(30)  # Control frame rate

    return True  # Return True if the loop exits

def show_game_over_menu(screen, win):
    running = True

    def stop_running():
        nonlocal running
        running = False

    font_large = pygame.font.SysFont('niagarasolid', 120)  # Define a large font for game over message
    font_medium = pygame.font.SysFont('niagarasolid', 50)  # Define a medium font for missed count

    while running:
        screen.fill((4, 56, 43))  # Fill the screen with a specific color

        # Display 'YOU WIN !!!' or 'GAME OVER' based on the win condition
        message_text = font_large.render('YOU WIN !!!' if win else 'GAME OVER', True, 'red' if not win else COLOR1)
        screen.blit(message_text, (SCREEN_WIDTH // 2 - message_text.get_width() // 2, SCREEN_HEIGHT // 4))

        # Display the missed count if the game is lost
        if not win:
            missed_count_text = font_medium.render(f'Score: {game.player.score}', True, COLOR2)

            screen.blit(missed_count_text, (350,125))

        # Create 'Again' and 'Exit' buttons on the screen
        button(screen, 'Again', 350, 350, 100, 50, COLOR1, COLOR2, stop_running)
        button(screen, 'Exit', 350, 450, 100, 50, COLOR1, COLOR2, pygame.quit)

        pygame.display.flip()  # Update the display

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Quit the game if the window is closed
                return False
        clock.tick(30)  # Control frame rate

    return True  # Return True if the loop exits


class Game:
    """
    Main class that controls the game's overall logic and state

    Attributes:
        grid (Grid): The grid layout of the game
        player (Player): The player playing the game
        scoreboard (Scoreboard): The scoreboard displaying score and misses
        pythons (list of Python): List of python objects in the game
        python_interval (float): Time interval for python appearanc
        last_python_time (float): The time when the last python appeared
        game_over (bool): Flag to indicate if the game is over
        win (bool): Flag to indicate if the player has won
    """
    def __init__(self):
        # Initializes the Game object with a grid, player, scoreboard, and python objects
        self.grid = Grid(GRID_SIZE)  # Initialize the grid
        self.player = Player()  # Initialize the player
        self.scoreboard = Scoreboard()  # Initialize the scoreboard
        self.pythons = [Python(python_image, pos) for pos in self.grid.positions]  # Create Python objects
        self.python_interval = 1.3  # Set interval for python appearance
        self.last_python_time = 0  # Initialize time tracker for last python appearance
        self.game_over = False  # Game over state
        self.win = False  # Win state
        self.running = True  # Game running state
        self.WINNER_MUSIC_PATH = "Winner_Music.mp3"  # Path to the winner music file
        self.LOSER_MUSIC_PATH = "Loser_Music.mp3"  # Path to the loser music file

    def reset_game(self):
        # Resets player, scoreboard, pythons, and other state variables
        self.player = Player()  # Reset player
        self.scoreboard = Scoreboard()  # Reset scoreboard
        # ... reset other state variables as needed ...
        self.game_over = False  # Reset game over state
        self.win = False  # Reset win state
        self.running = True  # Reset game running state
        self.last_python_time = 0  # Reset time tracker for last python appearance

    def handle_click(self, pos):
        # Handles clicking on python objects
        for python in self.pythons:
            if python.visible and python.position[0] < pos[0] < python.position[0] + python.image.get_width() \
                    and python.position[1] < pos[1] < python.position[1] + python.image.get_height():
                python.hide()
                self.player.hit_python()
                # Play smack sound for python
                pygame.mixer.Sound('SMACK Sound Effect.mp3').play()

    def show_next_python(self):
        # Hides all pythons and checks if the current python was missed
        for python in self.pythons:
            if python.visible:
                self.player.miss_python()  # Increment missed count if the python was visible
            python.hide()

        self.current_python_index = random.randint(0, len(self.pythons) - 1)
        self.pythons[self.current_python_index].appear()

    def start(self):
        # Display main menu and start the game loop

        if not show_main_menu(screen):  # Show main menu and exit if 'Exit' is selected
            return

        pygame.mixer.music.load(MAIN_MUSIC_PATH)  # Load main music
        pygame.mixer.music.play(-1)  # Start playing the main music

        last_python_time = 0  # Initialize last python appearance time

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False  # Exit the game if the window is closed
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(pygame.mouse.get_pos())  # Handle mouse click for hitting python

            # Makes a random python appear based on the interval
            current_time = time.time()
            if current_time - last_python_time > self.python_interval:
                self.show_next_python()
                last_python_time = current_time

            # Logic to adjust python appearance speed based on the player's score
            if self.player.score <= 10:
                self.python_interval = 1.0
            elif self.player.score <= 20:
                self.python_interval = 0.6
            elif self.player.score <= 30:
                self.python_interval = 0.5
            
            # Win condition: Score reaches 35
            if self.player.score >= 35:
                pygame.mixer.music.load(self.WINNER_MUSIC_PATH)  # Load winner music
                pygame.mixer.music.play()  # Play winner music
                self.game_over = True  # Set game over
                self.win = True  # Set win state
                self.running = False  # Stop the game loop
            
            # Losing condition: Missed count reaches 10
            if self.player.missed >= 10:
                pygame.mixer.music.load(self.LOSER_MUSIC_PATH)  # Load loser music
                pygame.mixer.music.play()  # Play loser music
                self.game_over = True  # Set game over
                self.win = False  # Set lose state
                self.running = False  # Stop the game loop
                
            screen.fill((4, 56, 43))  # Fill the screen with a color
            
            # designs 3x3 grid
            horizontal_spacing = SCREEN_WIDTH // (GRID_SIZE + 1.01)
            vertical_spacing = SCREEN_HEIGHT // (GRID_SIZE + 1.01)
            horizontal_offset = 0
            vertical_offset = 35

            for x in range(GRID_SIZE):   # draws the outer grid circles
                for y in range(GRID_SIZE):
                    circle_x = (x + 1) * horizontal_spacing + horizontal_offset
                    circle_y = (y + 1.0005) * vertical_spacing + vertical_offset
                    pygame.draw.circle(screen, COLOR1, (circle_x, circle_y), 85)

            for x in range(GRID_SIZE):
                for y in range(GRID_SIZE):   # draws the inner grid circles
                    circle_x = (x + 1) * horizontal_spacing + horizontal_offset
                    circle_y = (y + 1.0005) * vertical_spacing + vertical_offset
                    pygame.draw.circle(screen, COLOR3, (circle_x, circle_y), 80)
    
            # draws each python
            for python in self.pythons:
                python.draw(screen)

            # displays the score
            self.scoreboard.display_score(self.player.score, screen)
            self.scoreboard.display_missed_count(self.player.missed, screen)
                    
            # updates the display
            pygame.display.flip()
            clock.tick(120)
        
            if self.game_over:
                self.running = False  # Set this to False to end the game loop

        if self.game_over:
            retry = show_game_over_menu(screen, self.win)  # Display game over menu and handle user choice
            if retry:
                self.reset_game()  # Reset game state
                self.start()  # Restart the game if 'Try Again' is selected
            else:
                self.running = False  # End the game if 'Exit' is selected

# Starting the game
game = Game()  # Create an instance of the Game class
if show_main_menu(screen):  # Show the main menu
    game.start()  # Start the game
pygame.quit()  # Quit pygame when the game ends
