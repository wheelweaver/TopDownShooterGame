import pygame
vect = pygame.math.Vector2

# define colors
WHITE = (255,255,255)
BLACK = (0,0,0)
LIGHTGREY = (100,100,100)
DARKGREY = (40, 40, 40)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
TRON = (12,49,51)
TRON2 = (2,27,32)
LIGHTBLUE = (58,147,161)
MEDIUMBLUE = (15,104,104)
COLORSS = [RED, GREEN, BLUE, WHITE]
COLORS = [RED, TRON, LIGHTBLUE, MEDIUMBLUE]

#game options
WIDTH  = 1024
HEIGHT = 768
FPS = 60

TILESIZE = 32
GRID_WIDTH = WIDTH / TILESIZE
GRID_HEIGHT = HEIGHT / TILESIZE

PEOPLE = ['p1.png', 'p2.png', 'p3.png', 'p4.png', 'p5.png']

#WALL_MAPS = ['wallMap3.txt', 'wallMap2.txt', 'wallMap.txt']
RANDOM_GAME_TIME = [100, 40, 30, 20, 10, 45]

# Player Info
PLAYER_SPEED = 300
PLAYER_IMAGE = 'mainChar.png'
PLAYER_ROATION_SPEED = 250
PLAYER_RECTANGE = pygame.Rect(0,0,22,22)
PLAYER_HEALTH = 500
# Enemy Info
ENEMY_IMAGE = 'enemy.png'
#ENEMY_SPEED = 150
ENEMY_SPEED = [150, 100, 75, 125, 300, 500]

ENEMY_RECTANGLE = pygame.Rect(0,0,30,30)
ENEMY_ROATION_SPEED = 250
ENEMY_RADIUS = 50 #Avoid each other
Enemy_DETECTION_RADIUS = 300
ENEMY_DAMAGE = 10

# Princess
PRINCESS_IMAGE = 'princess.png'
PRINCESS_ROATION_SPEED = 250
PRINCESS_ROATION_SPEED = 250
PRINCESS_RECTANGE = pygame.Rect(0,0,35,35)

#Bullet Info
BULLET_IMAGE = 'bullet3.png'
BULLET_SPEED = 500
BULLET_LAST = 800
BULLET_RATE = 150
BULLET_SHOT_CHANGE = vect(30, 10)
ENEMY_BULLET_LAST = 300

ENEMY_BULLET_IMAGE = 'bullet2.png'
#ENEMY_BULLET_IMAGE = 'bullet4.png'


#Music
BACKGROUND_M = 'background.ogg'
WEAPON_SOUNDS = ['laser.ogg']
START_M = 'start.mp3'
#Laser_M = 'laser.ogg'
