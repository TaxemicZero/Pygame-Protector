import math
import random


import pygame
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum
# from pygame import mixer




class GameState(Enum):
    QUIT = -1
    TITLE = 0
    LEVEL_SWITCH = 1
    RUNNING = 2
    OVER = 3

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
        if self.xCoord <= 225:
            self.xCoord = 225
        if keys[pygame.K_RIGHT]:
            self.xCoord += self.velocity
        if self.xCoord >= 475:
            self.xCoord = 475


class Enemy(Entity):
    maxStrafeRight = 1
    maxStrafeLeft = 1
    direction = 1
    fireRate = 1
    fireTimer = 0
    def __init__(self, x, y, img, vel, size, fireRate):
        self.xCoord = x
        self.yCoord = y
        self.img = pygame.transform.scale(pygame.image.load(img),(size[0],size[1]))
        self.velocity = vel
        maxStrafe = random.randint(30, 130)
        self.maxStrafeRight = x + maxStrafe
        if self.maxStrafeRight > 475:
            self.maxStrafeRight = 475
        self.maxStrafeLeft = x - maxStrafe
        if self.maxStrafeLeft < 225:
            self.maxStrafeLeft = 225
        self.fireRate = fireRate

    def shoot(self):
        self.fireTimer += 1
        if self.fireTimer > self.fireRate:            
            bullet = Bullet(self.xCoord + 25, self.yCoord + 25, 'bullet.png', 0.4, [10,20])
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
        distance = math.sqrt(math.pow(entity.xCoord + 25 - self.xCoord, 2) + (math.pow(entity.yCoord + 25 - self.yCoord, 2)))
        if distance < 40:
            return True
        else:
            return False

def levelStart():
    global level
    global player
    level += 1
    player = Player(370, 440, 'player.png', 1, [50,50])
    enemies_on_screen.clear()
    bullets_on_screen.clear()
    #difficulty scaling
    firerate = 180 + 20 * level
    velocity = 0.2 + 0.1 * level
    for x in range(level // 3 + 1):
        enemy = Enemy(350, 40, 'enemy.png', velocity, [50,50], random.randint( int(firerate * 0.8),int(firerate * 1.2)))
        enemies_on_screen.append(enemy)
        print('added enemy')
    
def gameOver():
    bullets_on_screen.clear()
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
background = pygame.image.load('background3.png')


enemies_on_screen = []
bullets_on_screen = []
# Sound
#mixer.music.load("background.wav") 
#mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Protector")
pygame.display.set_icon(pygame.image.load('player.png'))

#variables
levelTransition = True
running = True
score = 0
gameState = GameState.TITLE
player = Player(370, 440, 'player.png', 0.5, [50,50])
FPS = 480
clock = pygame.time.Clock()
time_passed = 0
level_swap_time = 0
level = 0

while running:

    #refresh the clock
    dt = clock.tick(FPS) / 1000

    


    if gameState == GameState.TITLE:
        level = 0
        score = 0
        screen.fill((8, 96, 168))
        title_text = pygame.font.Font('freesansbold.ttf', 64).render("Protector", True, (255, 255, 255))
        screen.blit(title_text, (150, 100))
        blit_text(screen,'Protect the civilians! \nUse your shield to block shots \nPress arrow keys to move \nPress Enter to start\n\nGood luck!',(150, 200),pygame.font.Font('freesansbold.ttf', 32))        

    if gameState == GameState.RUNNING:

        time_passed += dt
        time_left = 60 - time_passed

        screen.blit(background, (0, 0))
        screen.blit(pygame.transform.scale(pygame.image.load("crowd2.png"), (300,50) ), (225, 550))
        blit_text(screen, "Level " + str(level) + " \nTime left: " + str(int(time_left)) + "s", (570,20), pygame.font.Font('freesansbold.ttf', 32), pygame.Color('black'))

        #pygame.draw.line(screen, (0,0,0), [225, 0], [225, 600])
        #pygame.draw.line(screen, (0,0,0), [525, 0], [525, 600])
        
        if time_left <= 0:
            gameState = GameState.LEVEL_SWITCH
            time_passed = 0

        for bullet in bullets_on_screen:
            bullet.fly()
            if bullet.yCoord > 470:
                time_passed = 0
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
        extra_text = 'You saved ' + str(score) + ' people\nHowever, there are many more to save\n Press r to restart'
        blit_text(screen, extra_text,(150, 310),pygame.font.Font('freesansbold.ttf', 32))

    if gameState == GameState.LEVEL_SWITCH:
        screen.fill((8, 96, 168))
        trans_text = pygame.font.Font('freesansbold.ttf', 64).render("Level " + str(level + 1), True, (255, 255, 255))
        screen.blit(trans_text, (300, 200))
        level_swap_time += dt
        if level_swap_time > 2:
            gameState = GameState.RUNNING
            level_swap_time = 0
            levelStart()
        

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mouse_up = True
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_RETURN) & (gameState == GameState.TITLE):
                gameState = GameState.LEVEL_SWITCH
            if (event.key == pygame.K_r) & (gameState == GameState.OVER):
                gameState = GameState.TITLE
            
    

    pygame.display.update()