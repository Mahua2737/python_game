import pygame
import sys
import random

pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bombing Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.Font(None, 36)

# Load images
jet_image = pygame.image.load("plane1.jpeg")
bomb_image = pygame.image.load("bomb1jpeg.jpeg")
house_image = pygame.image.load("home.jpeg")
explosion_image = pygame.image.load("ex1jpeg.jpeg")

# Load sounds
explosion_sound = pygame.mixer.Sound("music.wav")

# Set up game variables
jet_x, jet_y = -200, 100
bomb_x, bomb_y = -200, 100
MAX_BOMBS = 4
bomb_falling = False
house_speed = 5
house_x = WIDTH // 2 - house_image.get_width() // 2
house_y = HEIGHT - house_image.get_height()
score = 0


# Function to drop bomb
def drop_bomb():
    global bomb_x, bomb_y, bomb_falling
    bomb_x = jet_x + 20  # Align bomb with the plane
    bomb_y = jet_y + 40  # Align bomb with the plane
    bomb_falling = True
    # Play explosion sound
    explosion_sound.play()


# Function to check collision between bomb and house
def check_collision():
    global bomb_falling, score
    if (
        house_x < bomb_x + bomb_image.get_width() < house_x + house_image.get_width()
        and house_y
        < bomb_y + bomb_image.get_height()
        < house_y + house_image.get_height()
    ):
        bomb_falling = False
        # Play explosion sound
        explosion_sound.play()
        # Increment score
        score += 1


# Set up timer event for bomb drops
DROP_BOMB_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(
    DROP_BOMB_EVENT, 2000
)  # Trigger every 2000 milliseconds (2 seconds)

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == DROP_BOMB_EVENT:
            if not bomb_falling:
                drop_bomb()

    # Move the jet
    jet_x += 4
    if jet_x > WIDTH:
        jet_x = -200

    # Move the bomb
    if bomb_falling:
        bomb_y += 5
        if bomb_y > HEIGHT:
            bomb_falling = False

        # Check collision with house
        check_collision()

    # Draw jet plane
    screen.blit(jet_image, (jet_x, jet_y))

    # Draw bomb
    if bomb_falling:
        screen.blit(bomb_image, (bomb_x, bomb_y))

    # Handle house movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and house_x > 0:
        house_x -= house_speed
    if keys[pygame.K_RIGHT] and house_x < WIDTH - house_image.get_width():
        house_x += house_speed

    # Draw house at the bottom middle
    screen.blit(house_image, (house_x, house_y))

    # Draw score
    score_text = FONT.render("Score: " + str(score), True, BLACK)
    screen.blit(score_text, (10, 10))

    # Display explosion if bomb touches house
    if not bomb_falling:
        screen.blit(
            explosion_image,
            (
                bomb_x - explosion_image.get_width() // 2,
                bomb_y - explosion_image.get_height() // 2,
            ),
        )

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
