# use pygame library
import pygame
import random
import math
from pygame import mixer

# initialize the pygame
pygame.init()

# create a screen
window = pygame.display.set_mode((800, 600))

# Add background image
background = pygame.image.load("background.png")
pygame.display.set_icon(background)

# Add the soundtrack
mixer.music.load("background.wav")
mixer.music.play(-1)

# Add a title icon
pygame.display.set_caption("Space Invaders!")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# origin is the top-left
playerIMG = pygame.image.load("001-space-invaders.png")
playerX = 370
playerY = 480

# create a variable that specifies how much movement occurred
playerX_change = 0

# Create the enemy
# for loop to create multiple enemies
enemyIMG = []
enemyX = []
enemyY = []
numEnemies = 6

# Need to be in lists so that each enemy has their own change. apparently...
enemyX_change = []
enemyY_change = []

for i in range(numEnemies):
    enemyIMG.append(pygame.image.load("002-alien.png"))
    # Make it so that the enemy spans randomly within a range
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Create the Bullet
bulletIMG = pygame.image.load("bullet.png")
bulletX = 0  # Because we will change it later
bulletY = 480  # Because our spaceship is at 480, and we want to shoot from our ship
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"  # 2 states: ready you can see the bullet; fire bullet is moving

# Keep track of score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 28)
textX = 10
textY = 10

# Game over text
game_over_font = pygame.font.Font("freesansbold.ttf", 64)


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    window.blit(score, (textX, textY))


def game_over_text():
    game_over = game_over_font.render("GAME OVER", True, (255, 255, 255))
    window.blit(game_over, (200, 255))


def player(x, y):
    window.blit(playerIMG, (x, y))


def enemy(x, y, i):
    window.blit(enemyIMG[i], (x, y))


# when we press space, we want to call this function
def firebullet(x, y):
    global bullet_state  # so we can use this variable in the function
    bullet_state = "fire"
    window.blit(bulletIMG, (x + 16, y + 10))  # so that the bullet is at the centre of our ship


# Finding the collion by calculating the distance between bullet and enemy
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow((enemyX - bulletX), 2) + math.pow((enemyY - bulletY), 2))
    if distance < 27:
        return True
    else:
        return False


# now we need events to interact within this game window. Without an exit button, it will close automatically.
# All events that will run will go within this loop. When it finishes, the game terminates. Thus, by pressing exit, we
# switch running to False.
running = True
while running:
    # The base layer
    window.fill((10, 10, 10))

    # Background
    window.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":  # Before we could shoot a bullet anytime and the bullet would just follow the x co-ord of the ship, so we have to explicitly state here.
                    shoot_sound = mixer.Sound("laser.wav")
                    shoot_sound.play()
                    bulletX = playerX
                    firebullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:  # This so that player eventually stops after a movement
                playerX_change = 0

    # Place anything persistent here

    playerX += playerX_change
    # prevent player from going outside boundary; it essentially deletes the icon and replaces a valid one.
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:  # 736 because the size of the icon is 64
        playerX = 736

    for i in range(numEnemies):
        if enemyY[i] > 440:
            for j in range(numEnemies):
                enemyY[j] = 2000
            game_over_text()
            break

        # Move the Enemy automatically within boundaries
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 6
            enemyY[i] += enemyY_change[i]  # decrease by constant amount
        elif enemyX[i] >= 736:
            enemyX_change[i] = -6
            enemyY[i] += enemyY_change[i]

        # insert collision check here
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0,
                                       736)  # spawn = random x y value. Hence, we overwrite enemy's location as if it's re-spawning
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Return the bullet after going off the screen
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    # Bullet Movement: so that the bullet persists at all frames
    if bullet_state == "fire":
        firebullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)  # increase values and re-frame the image.
    show_score(textX, textY)
    pygame.display.update()  # Always update variables

# 1. Initialize pygame
# 2. Create a window and an event loop
# 3. Customize the window
# 4. Add in the player: first upload photo and starting co-ords
# 5. Call the player method within the loop so that it always appears. After fill so that it is layer over screen
# 6. Give the player function parameters so you can increase or decrease its value
# 7. To move objects with keys, create an event. Put it in the event loop so that it checks for input on every frame.
# 7.5 You need to first specify if key is pressed, then check the type. Then check once it is released. Create a change variable the re-iterates positions
# 8. Create an enemy char. Use bounded random integers for respawning.
# 9. Add enemy movement. since in while loop already, whenever the enemy is within bounds, the co-ords change.
# 10. After adding background, while loop is slower, so the objects move small increments every so often. Increase speed
# 11. Create framework for fire function
# 12. Within events, make a condition for when space is pressed. Then pass in the coords of the spaceship.
# 13. However, this just makes the bullet appear; it doesn't propagate through the frame. Since we changed the state, we can make a conditional within the loop that checks a
#     bullet state and keeps calling the function (problem because it uses the new playerX value every call, and the state never changes back to ready, so we can't call fire again.

# How to respawn? Just overwrite enemy X enemyY again.
# decrease enemy spawn location because if it spans at 800, it is past the border and will float down automatically

# Creating multiple enemies. We will make a list of enemy elements of a preset size. We will fill that list. Thus, whenever we want to check on the state of the enemies, we need to go iterate through the list.
