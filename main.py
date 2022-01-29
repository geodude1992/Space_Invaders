import math
import pygame
import random
from pygame import mixer

# Initialize pygame
pygame.init()

# Create Screen: w=800px, h=600px expands from top left corner
screen = pygame.display.set_mode((800, 600))

# Background Img same px as screen
background = pygame.image.load('space.png')

# Background sound: -1 to loop sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title
pygame.display.set_caption("Celestial Invasion")

# Icon from Flaticon.com 32px
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player: img from Flaticon.com 64px
playerImg = pygame.image.load('space-invaders.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemies
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    # Enemy: img from Flaticon.com 64px
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(64, 150))
    enemyX_change.append(0.2)
    enemyY_change.append(random.randint(15, 35))

# Bullet1: img from Flaticon.com 32px
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1
# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving
bullet_state = "ready"

# Initialize score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game Over text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 0, 255))
    screen.blit(score, (x, y))


def game_over_text():
    gO_text = over_font.render("GAME OVER", True, (128, 0, 128))
    screen.blit(gO_text, (200, 250))


def player(x, y):
    # Draw img on game surface
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    # Draw img on game surface
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    # Global variable can be accessed anywhere
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16, y+10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    # Distance formula d = sqrt((x-xi)^2 + (y-yi)^2)
    distance = math.sqrt((math.pow(enemyX-bulletX, 2)) + (math.pow(enemyY-bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    # RGB - Magenta (Screen) Background Color
    #screen.fill((255, 0, 255))

    # Background Img
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        # Check if user quits game
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check direction
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                playerX_change = -0.25
            if event.key == pygame.K_d:
                playerX_change = 0.25
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    # Play firing sound when shooting key is pressed
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    # Get the current x-cord of spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                playerX_change = 0

    # Update X position
    playerX += playerX_change

    # Set boundaries
    if playerX <= 0:
        playerX = 0
    # 800px - 64px
    elif playerX >= 736:
        playerX = 736

    # Enemy movement
    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]

        # Set boundaries and change direction when boundary reached
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.2
            enemyY[i] += enemyY_change[i]
        # 800px - 64px
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.2
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            # Play collision sound when collision occurs
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            # Reset bullet to ready
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            # Reset enemy when shot
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(64, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Draw player on top of screen - Calls Player function
    player(playerX, playerY)

    # Show score
    show_score(textX, textY)

    # Always update game display
    pygame.display.update()
