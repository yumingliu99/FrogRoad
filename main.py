
import pygame, sys, random
from frog import Frog
from street import Street
from river import River

# Initializes pygame internal variables
pygame.init()

# Only allow KEYDOWN (key press) and QUIT (exit) events
# Improves performance by not searching for all events including mouse events
pygame.event.set_allowed([pygame.KEYDOWN, pygame.QUIT])

# Define a tuple representing screen size in pixels
# Initialize a window with the screen size defined
SCREEN_DIM = WIDTH, HEIGHT = 600, 500
SCREEN = pygame.display.set_mode(SCREEN_DIM)
pygame.display.set_caption('Frog Road!')

# Define a Clock object to control the game's frame rate
CLOCK = pygame.time.Clock()
FPS = 60

# Define RGB colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (28, 128, 28)
YELLOW = (100, 85, 0)
BROWN = (118, 92, 72)
GRAY = (175, 175, 175)
BLUE = (0, 0, 175)

# Fonts
FONT = pygame.font.Font('resources/joystix monospace.ttf', 20)
MENU_BIG = pygame.font.Font('resources/joystix monospace.ttf', 60)
MENU_MED = pygame.font.Font('resources/joystix monospace.ttf', 25)
MENU_SMALL = pygame.font.Font('resources/joystix monospace.ttf', 15)

# Images
MENU_IMAGE = pygame.image.load('resources/menu_image.png')

# Menus
START_MENU = True
END_MENU = False

# Create Frog object
frog = Frog()

# Create Street objects
streets = []
number_of_buses = 3
street_height = 400
for _ in range(2):
    streets.append(Street(street_height, 'Left', random.randint(1, number_of_buses)))
    streets.append(Street(street_height - 40, 'Right', random.randint(1, number_of_buses)))
    street_height -= 80

# Create River objects
rivers = []
number_of_logs = 3
river_height = 200
for _ in range(2):
    rivers.append(River(river_height, 'Left', random.randint(1, number_of_logs)))
    rivers.append(River(river_height - 30, 'Right', random.randint(1, number_of_logs)))
    river_height -= 60

# Scoring Information
score = 0
high_score = 0
current_best = 0

# Game loop
while True:
    while START_MENU:
        # Tick forward at 15 frames per second
        CLOCK.tick(15)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    START_MENU = False

        # Show text on menu screen
        SCREEN.fill(GREEN)
        
        name = MENU_BIG.render('FROG ROAD', True, WHITE)
        instructions = MENU_SMALL.render('Press Space To Start', True, (255, 255, 255))
        SCREEN.blit(name, (75, 130))
        SCREEN.blit(instructions, (180, 210))
        SCREEN.blit(MENU_IMAGE, (145, 260))

        # pygame.display.flip() updates the screen
        pygame.display.update()

    while END_MENU:
        # Tick forward at 15 frames per second
        CLOCK.tick(15)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    END_MENU = False
                    # Reset all stats
                    current_best = 0
                    score = 0
                    frog.lives = 3

        # Show text on end screen
        SCREEN.fill(GREEN)
        
        thx = MENU_MED.render('Thanks for Playing!', True, WHITE)
        scores = MENU_MED.render('Your Final Score: %d' % (score + current_best), True, WHITE)
        instructions = MENU_SMALL.render('Press \'Space\' To Play Again', True, WHITE)
        SCREEN.blit(thx, (85, 120))
        SCREEN.blit(scores, (70, 180))
        SCREEN.blit(instructions, (130, 240))

        # pygame.display.flip() updates the screen
        pygame.display.update()

    # Tick forward at 60 frames per second
    CLOCK.tick(FPS)

    # Event listener: Listens for an input the player provides
    for event in pygame.event.get():
        # User closes the game window
        if event.type == pygame.QUIT:
            sys.exit()
        # User presses a key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w: # W
                frog.move_up()
            if event.key == pygame.K_a: # A
                frog.move_left()
            if event.key == pygame.K_s: # S
                frog.move_down()
            if event.key == pygame.K_d: # D
                frog.move_right()
        
    # Color the background
    SCREEN.fill(BLACK)

    # Act on streets and buses
    for street in streets:
        # Draw Street
        SCREEN.fill(GRAY, street.rect)

        # Bus
        for bus in street.buses:
            SCREEN.blit(bus.image, bus.rect)
            bus.move()
            if frog.rect.colliderect(bus.rect):
                frog.reset_position(True)

    # Act of rivers and logs
    frog_on_log = False
    for river in rivers:
        # Draw River
        SCREEN.fill(BLUE, river.rect)

        # Log
        for log in river.logs:
            SCREEN.blit(log.image, log.rect)
            log.move()
            if frog.rect.colliderect(log.rect):
                frog.move_on_log(log)
                frog_on_log = True
        
        # Collided with River and not a Log
        if not frog_on_log and frog.rect.colliderect(river.rect):
            frog.reset_position(True)

    # Draw frog
    SCREEN.blit(frog.image, frog.rect)

    # Frog reached end
    if frog.rect.top <= 60:
        frog.reset_position(False)
        score += 1000 + current_best
        current_best = 0


    # Update the score only if the score is increasing
    current_best = 475 - frog.rect.top if 475 - frog.rect.top > current_best else current_best

    # Update high score
    if score + current_best >= high_score:
        high_score = score + current_best

    # Display score, high score, and lives
    # NOTE: Escape characters do not work in pygame (\n, \t, etc)
    score_text = FONT.render('Score: %d' % (score + current_best), True, WHITE)
    high_score_text = FONT.render('High Score: %d' % (high_score), True, WHITE)
    lives_text = FONT.render('Lives: %d' % (frog.lives), True, WHITE)
    SCREEN.blit(score_text, (5, 0))
    SCREEN.blit(high_score_text, (5, 20))
    SCREEN.blit(lives_text, (5, 40))

    # End of game
    if frog.lives == 0:
        END_MENU = True

    # pygame.display.flip() updates the screen
    pygame.display.flip()