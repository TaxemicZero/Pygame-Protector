import math
import random

import pygame
# from pygame import mixer

# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

# Sound
#mixer.music.load("background.wav")
#mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Test Game")
pygame.display.set_icon(pygame.image.load('icon.png'))

class Player:
    img = ''
    xCoord = 370
    yCoord = 480
    velocity = 5
    def __init__(self, x, y, img, vel):
        self.xCoord = x
        self.yCoord = y
        self.img = pygame.transform.scale(pygame.image.load(img),(50,50))
        self.velocity = vel
    def player(self):
        screen.blit(self.img, (self.xCoord, self.yCoord))

        

# Enemy
class Enemy():
    img = ''
    xCoord = 0
    yCoord = 0
    xVel = 0
    yJump = 0

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []


num_of_enemies = 20

for i in range(num_of_enemies):
    enemyImg.append(pygame.transform.scale(pygame.image.load('enemy.png'),(50,50)))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)
    

# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.transform.scale(pygame.image.load('bullet.png'),(20,20))
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))





def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 40:
        return True
    else:
        return False


# Game Loop
running = True
player = Player(370, 480, 'player.png', 5)
while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.xCoord -= player.velocity
        if player.xCoord <= 0:
            player.xCoord = 0
    if keys[pygame.K_RIGHT]:
        player.xCoord += player.velocity
        if player.xCoord >= 736:
            player.xCoord = 736
    if keys[pygame.K_SPACE]:
        if bullet_state is "ready":
            #bulletSound = mixer.Sound("laser.wav")
            #bulletSound.play()
            # Get the current x cordinate of the spaceship
            bulletX = player.xCoord
            fire_bullet(bulletX, bulletY)


    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            #explosionSound = mixer.Sound("explosion.wav")
            #explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player.player()
    show_score(textX, testY)
    pygame.display.update()