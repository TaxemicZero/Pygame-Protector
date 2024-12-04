import math
import random

import uicode

import pygame
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum
# from pygame import mixer




class GameState(Enum):
    QUIT = -1
    TITLE = 0
    RUNNING = 1
    OVER = 2

class Entity:
    img = ''
    xCoord = 370
    yCoord = 480
    velocity = 5
    def __init__(self, x, y, img, vel, size):
        self.xCoord = x
        self.yCoord = y
        self.img = pygame.transform.scale(pygame.image.load(img),(size[0],size[1]))
        self.velocity = vel
    def draw(self):
        screen.blit(self.img, (self.xCoord, self.yCoord))

class Player(Entity):
    
    #do shield code
    #def __init__ (self):

    def movePlayer(self,keys):
        if keys[pygame.K_LEFT]:
            self.xCoord -= self.velocity
        if self.xCoord <= 150:
            self.xCoord = 150
        if keys[pygame.K_RIGHT]:
            self.xCoord += self.velocity
        if self.xCoord >= 600:
            self.xCoord = 600


class Enemy(Entity):
    maxStrafeRight = 1
    maxStrafeLeft = 1
    direction = 1
    fireRate = 300
    fireTimer = 0
    def __init__(self, x, y, img, vel, size, fireRate):
        self.xCoord = x
        self.yCoord = y
        self.img = pygame.transform.scale(pygame.image.load(img),(size[0],size[1]))
        self.velocity = vel
        maxStrafe = random.randint(50, 270)
        self.maxStrafeRight = x + maxStrafe
        if self.maxStrafeRight > 550:
            self.maxStrafeRight = 550
        self.maxStrafeLeft = x - maxStrafe
        if self.maxStrafeRight < 200:
            self.maxStrafeRight = 200
        self.fireRate = fireRate

    def shoot(self):
        self.fireTimer += 1
        if self.fireTimer > self.fireRate:            
            bullet = Bullet(self.xCoord + 25, self.yCoord + 25, 'bullet.png', 0.1, [10,20])
            bullets_on_screen.append(bullet)
            self.fireTimer = 0
            #print("shot on " + str(self.xCoord))
    def strafe(self):
        self.xCoord += self.velocity * self.direction
        if self.xCoord > self.maxStrafeRight:
            self.xCoord = self.maxStrafeRight
            self.direction = -1
        if self.xCoord < self.maxStrafeLeft:
            self.xCoord = self.maxStrafeLeft
            self.direction = 1



class Bullet(Entity):
    def fly(self):
        self.yCoord += self.velocity
    def isCollision(self, entity):
        distance = math.sqrt(math.pow(entity.xCoord - self.xCoord, 2) + (math.pow(entity.yCoord - self.yCoord, 2)))
        if distance < 40:
            return True
        else:
            return False

#UI CODE

def levelStart():
    enemy = Enemy(370, 40, 'enemy.png', 0.2, [50,50], 1000)
    enemies_on_screen.append(enemy)
    
def gameOver():
    over_text = pygame.font.Font('freesansbold.ttf', 64).render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def blit_text(surface, text, pos, font, color=pygame.Color('white')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.

# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background2.png')


enemies_on_screen = []
bullets_on_screen = []
# Sound
#mixer.music.load("background.wav")
#mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Test Game")
pygame.display.set_icon(pygame.image.load('icon.png'))
level = 1
levelTransition = True
running = True
score = 0
gameState = GameState.TITLE
uielement = uicode.UIElement(
    center_position=(400, 400),
    font_size=30,
    bg_rgb=(106, 159, 181),
    text_rgb=(255, 255, 255),
    text="Hello World",
    action=GameState.QUIT
)

FPS = 480
clock = pygame.time.Clock()

while running:

    #dt = clock.tick(FPS) / 1000
    if gameState == GameState.TITLE:
        screen.fill((8, 96, 168))
        title_text = pygame.font.Font('freesansbold.ttf', 64).render("Protector", True, (255, 255, 255))
        screen.blit(title_text, (150, 100))
        blit_text(screen,'Protect the civilians! \nUse your shield to block shots \nPress arrow keys to move \nPress Enter to start\n\nGood luck!',(150, 200),pygame.font.Font('freesansbold.ttf', 32))        

    if gameState == GameState.RUNNING:
        screen.blit(background, (0, 0))
        screen.blit(pygame.transform.scale(pygame.image.load("crowd2.png"), (300,50) ), (200, 550))
        for bullet in bullets_on_screen:
            bullet.fly()
            if bullet.yCoord > 470:
                gameState = GameState.OVER
                break
            collision = bullet.isCollision(player)
            if collision:
                #explosionSound = mixer.Sound("explosion.wav")
                #explosionSound.play()
                score += 1
                print(score)
                bullets_on_screen.remove(bullet)
                del bullet
            else:
                bullet.draw()

        for enemy in enemies_on_screen:
            enemy.shoot()
            enemy.strafe()
            enemy.draw()

        player.draw()

        player.movePlayer(pygame.key.get_pressed())

    if gameState == GameState.OVER:
        screen.fill((8, 96, 168))
        over_text = pygame.font.Font('freesansbold.ttf', 64).render("GAME OVER", True, (255, 255, 255))
        screen.blit(over_text, (200, 200))
        extra_text = 'You saved ' + str(score) + ' people\nHowever, there are many more to save'
        blit_text(screen, extra_text,(150, 310),pygame.font.Font('freesansbold.ttf', 32))

    if levelTransition:
        levelTransition = False
        player = Player(370, 440, 'player.png', 0.5, [50,50])
        levelStart()
        

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mouse_up = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                gameState = GameState.RUNNING
            if (event.key == pygame.K_r) & (GameState == GameState.OVER):
                gameState = GameState.RUNNING
    


    #ui_action = uielement.update(pygame.mouse.get_pos(), mouse_up)
    #uielement.draw(screen)
    pygame.display.update()