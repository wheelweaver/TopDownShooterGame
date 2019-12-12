import pygame
import random
from random import choice

from os import path
from gameInfo import *
from sprites import *


class Game():
    def __init__(self):
        # initalize pygame and create window
        print("STS")
        self.counter = 0
        pygame.init()
        #pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("FINAL PROJECT")
        self.clock = pygame.time.Clock()
        self.start_ticks=pygame.time.get_ticks() #starter tick
        # Font to display Player Health
        self.font = pygame.font.Font(None, 54)
        self.font_color = pygame.Color('springgreen')

        ####################################TIME INFO NOT USED####################################################################
        #self.timer_started = False
        #self.totalTime = 10
        #self.passed_time = 0
        ############################################################################################################################
        pygame.key.set_repeat(500, 100)
        self.load_data()  # LOADS THE DATA USED
        #self.keepGoing = True
    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        """Function to draw elements onto the screen

        Parameters
        ----------
        text : type
            Description of parameter `What is displayed onto screen`.
        font_name : type
            Description of parameter `font_name`.
        size : type
            Description of parameter `size`.
        color : type
            Description of parameter `color`.
        x : type
            Description of parameter `Location`.
        y : type
            Description of parameter `Location`.
        align : type
            Description of parameter `align`.

        Returns
        -------
        type
            Blits information onto screen.
        """
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def load_data(self):
        """Loads all data.
        """
        game_folder = path.dirname(__file__) # Gets current directory
        self.map_data = []

        #Gets images of enemies before they become AGENTS and start attacking
        self.zero_img = pygame.image.load(path.join(game_folder, PEOPLE[0]))
        self.one_img = pygame.image.load(path.join(game_folder, PEOPLE[1]))
        self.two_img = pygame.image.load(path.join(game_folder, PEOPLE[2]))
        self.three_img = pygame.image.load(path.join(game_folder, PEOPLE[3]))
        self.four_img = pygame.image.load(path.join(game_folder, PEOPLE[4]))
        #List of total people so they can be randomly scatared around map
        self.totalPeople = [self.zero_img, self.one_img, self.two_img, self.three_img, self.four_img]

        #Images
        self.player_img = pygame.image.load(path.join(game_folder, PLAYER_IMAGE))
        self.enemy_img = pygame.image.load(path.join(game_folder, ENEMY_IMAGE))
        self.bullet_img = pygame.image.load(path.join(game_folder, BULLET_IMAGE))

        # ENEMY BULLETS
        self.enemyBullet_img = pygame.image.load(path.join(game_folder, ENEMY_BULLET_IMAGE))

        #self.princess_image = pygame.image.load(path.join(game_folder, PRINCESS_IMAGE))
        self.hud_font = path.join(game_folder, 'Impacted2.0.ttf')

        #Music
        pygame.mixer.music.load(path.join(game_folder, BACKGROUND_M)) #background music
        self.weapon_sounds = {}
        self.weapon_sounds['laser'] = []

        for sound in WEAPON_SOUNDS:
            self.weapon_sounds['laser'].append(pygame.mixer.Sound(path.join(game_folder, sound))) #laser shot music

#        with open(path.join(game_folder,choice(WALL_MAPS)), 'rt') as f:
        with open(path.join(game_folder,'wallMap.txt'), 'rt') as f:  # selects the text file of grid and appends to maps
            for line in f:
                self.map_data.append(line)

    def newGame(self):
        # starts a new game
        #self.totalTime = 10
        #self.counter = self.counter + 1

        self.all_sprites = pygame.sprite.Group()  # Sprite group for all sprites
        self.walls = pygame.sprite.Group()         # Sprite group for walls
        self.enemy = pygame.sprite.Group()          # Sprite group for enemy
        self.bullets = pygame.sprite.Group()        # Sprite group for bullets that player shoots
        self.bullets2 = pygame.sprite.Group()       # Sprite group for bullets that enemy shoots
        #self.princess = pygame.sprite.Group) # NOT USED

# Goes though the grid information to display elements onto screen
        #self.run()
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':                     # Creates a Wal
                    Wall(self, col, row)
                if tile == 'P':                     # Starting place of player
                    self.player = Player(self, col, row)
                if tile == 'E':                     # Puts the enemies
                    Enemy(self, col, row)

    def run(self):
        # Game loop
        self.keepGoing = True
        pygame.mixer.music.play(loops=-1) # Starts music
        while self.keepGoing:
            ######################## TIME DISPLAY INFO NOT USED##################################################################
            '''
            self.timer_started = not self.timer_started
            if self.timer_started:
                self.start_time = pygame.time.get_ticks()
            self.seconds = seconds=(pygame.time.get_ticks()-self.start_ticks)/1000 #calculate how many seconds
            #print(type(self.seconds))
            #print(self.seconds)
            if self.timer_started:
                self.passed_time = pygame.time.get_ticks() - self.start_time
                print(self.passed_time/1000)'''
            ###################################################################################################################
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pygame.quit()
        sys.exit()

    def update(self):
        # Game Loop update
        self.all_sprites.update()
        if len(self.enemy) == 0:
            self.keepGoing = False

        # Player get hit
        hits = pygame.sprite.spritecollide(self.player, self.bullets2, False, collide_rect2)
        for hit in hits:
            self.player.health -= ENEMY_DAMAGE
            hit.vel = vect(0, 0)
            if self.player.health <= 0:
                hit.kill()
                self.keepGoing = False

        # Bullet hits Enemy
        hits = pygame.sprite.groupcollide(self.enemy, self.bullets, False, True)
        for hit in hits:
            hit.kill()
        #print(self.counter)


    def events(self):
        # Game loop events
        for event in pygame.event.get():
            # closing window
            if event.type == pygame.QUIT:
                self.quit()


    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(self.screen,LIGHTGREY, (x,0), (x,HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(self.screen,LIGHTGREY, (0,y), (WIDTH,y))

    def draw(self):
        # Game Loop draw
        #self.screen.fill(choice(COLORSS))
        self.screen.fill(BLACK)

        self.draw_grid()
        self.all_sprites.draw(self.screen)
        self.draw_text('ENEMY: {}'.format(len(self.enemy)),self.hud_font, 30, GREEN, WIDTH - 10, 10, align="ne")
        text = self.font.render(str(self.player.health), True, self.font_color)
        self.draw_text("HEALTH", self.hud_font, 30, BLACK, 70, 20, align="center" )
        self.screen.blit(text, (50, 40))
        # *after* drwaing everything , flips the display (like a blackboard)
        pygame.display.flip()

    def start_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("Trust no one!  \t ANY OF THEM COULD BE AGENTS! \t KILL THEM ALL TO SURVIVE", self.hud_font, 32, RED, WIDTH / 2, HEIGHT / 5, align="center" )
        self.draw_text("USE ARROW KEYS TO MOVE AND SPACE To shoot. ", self.hud_font, 30, TRON, WIDTH / 2, HEIGHT / 3, align="center" )

        pygame.display.flip()
        pygame.event.wait()
        replay = True
        while replay:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    replay = False
                    self.quit()
                if event.type == pygame.KEYUP:
                    replay = False
                    self.totalTime = 10

    def game_over(self):
        #game over screen
        self.screen.fill(BLACK)
        if len(self.enemy) == 0:
            self.draw_text("YOU WON!", self.hud_font, 100, GREEN, WIDTH / 2, HEIGHT / 4, align="center" )
            self.draw_text("PRESS ANY KEY TO PLAY AGAIN", self.hud_font, 50, RED, WIDTH / 2, HEIGHT / 2, align="center" )
        elif(self.player.health <= 0):
            self.draw_text("GAME OVER. YOU DIED!", self.hud_font, 80, RED, WIDTH / 2, HEIGHT / 4, align="center" )
            self.draw_text("PRESS ANY KEY TO RESTART.", self.hud_font, 50, GREEN, WIDTH / 2, HEIGHT /2 , align="center" )
        pygame.display.flip()
        pygame.event.wait()
        replay = True
        while replay:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    replay = False
                    self.quit()
                if event.type == pygame.KEYUP:
                    #self.totalTime = choice(RANDOM_GAME_TIME)
                    replay = False
                    #WALL_MAPS = choice(WALL_MAPS)


g = Game()
g.start_screen()
while True:
    g.newGame()
    g.run()
    g.game_over()

pygame.quit()
