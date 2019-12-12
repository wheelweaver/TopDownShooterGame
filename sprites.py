import pygame
import sys
from random import choice
from gameInfo import *
from sprites import *
vect = pygame.math.Vector2

def collide_rect2(one, two):
    return one.collide_rect.colliderect(two.rect)

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.collide_rect = PLAYER_RECTANGE
        self.collide_rect.center = self.rect.center
        self.vel = vect(0, 0)
        self.pos = vect(x, y) * TILESIZE
        self.rotation = 0
        self.last_shot = 0
        self.health = PLAYER_HEALTH


    def getKeys(self):
        self.rotation_speed = 0
        self.vel = vect(0, 0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rotation_speed = PLAYER_ROATION_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rotation_speed = -PLAYER_ROATION_SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.vel = vect(PLAYER_SPEED, 0).rotate(-self.rotation)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.vel = vect(-PLAYER_SPEED / 2, 0).rotate(-self.rotation)
        if keys[pygame.K_SPACE]:
            toShoot = pygame.time.get_ticks()
            if toShoot - self.last_shot > BULLET_RATE:
                self.last_shot = toShoot
                direction = vect(1,0).rotate(-self.rotation)
                newPos = self.pos + BULLET_SHOT_CHANGE.rotate(-self.rotation)
                Bullet(self.game, newPos, direction)
                choice(self.game.weapon_sounds['laser']).play()
        '''
         FOR DIAGONAL MOVEMENT
        if self.vel.x !=0 and self.vel.y !=0:
            self.vel *= 0.7071
            '''
        '''
    def move(self,dx=0, dy=0):
        if not self.wallCollisons(dx, dy):
            self.x += dx
            self.y += dy
            '''
    def wallCollisons(self, dir):
        if dir == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.walls, False, collide_rect2)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.collide_rect.width / 2
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right + self.collide_rect.width / 2
                self.vel.x = 0
                self.collide_rect.centerx = self.pos.x
        if dir == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.walls, False, collide_rect2)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.collide_rect.height / 2
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom + self.collide_rect.height / 2
                self.vel.y = 0
                self.collide_rect.centery = self.pos.y



    def update(self):
        '''
        self.getKeys()
        self.rotation = (self.rotation + self.rotation_speed * self.game.dt) % 360
        self.image = pygame.transform.rotate(self.game.player_img, self.rotation)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
'''

        self.getKeys()
        self.rotation = (self.rotation + self.rotation_speed * self.game.dt) % 360
        self.image = pygame.transform.rotate(self.game.player_img, self.rotation)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt

        self.collide_rect.centerx = self.pos.x
        self.wallCollisons('x')
        self.collide_rect.centery = self.pos.y
        self.wallCollisons('y')
        self.rect.center = self.collide_rect.center


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.enemy
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.stand_image = choice(game.totalPeople)
        self.image = self.stand_image
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

        self.collide_rect = ENEMY_RECTANGLE.copy()
        self.collide_rect.center = self.rect.center
        self.pos = vect(x, y) * TILESIZE
        self.vel = vect(0, 0)
        self.acc = vect(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.speed = choice(ENEMY_SPEED)
        self.target = game.player
        self.last_shot = 0

    def update(self):
        target_distance = self.target.pos - self.pos
        if target_distance.length_squared() < Enemy_DETECTION_RADIUS**2:
            toShoot = pygame.time.get_ticks()
            if toShoot - self.last_shot > BULLET_RATE:
                self.last_shot = toShoot
                direction = vect(1,0).rotate(-self.rot)
                newPos = self.pos + BULLET_SHOT_CHANGE.rotate(-self.rot)
                Bullet2(self.game, newPos, direction)
                #choice(self.game.weapon_sounds['laser']).play()
            self.rot = target_distance.angle_to(vect(1, 0))
            self.image = pygame.transform.rotate(self.game.enemy_img, self.rot)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.acc = vect(1, 0).rotate(-self.rot)
            self.avoidEnemyRadius()
            self.acc.scale_to_length(self.speed)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            self.collide_rect.centerx = self.pos.x
            self.wallCollisons('x')
            self.collide_rect.centery = self.pos.y
            self.wallCollisons('y')
            self.rect.center = self.collide_rect.center
        #else:

    def shoot(self):
        self.rot_speed = 0
        self.vel = vect(0, 0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            toShoot = pygame.time.get_ticks()
            if toShoot - self.last_shot > BULLET_RATE:
                self.last_shot = toShoot
                direction = vect(1,0).rotate(-self.rot)
                newPos = self.pos + BULLET_SHOT_CHANGE.rotate(-self.rot)
                Bullet2(self.game, newPos, direction)

    def wallCollisons(self, dir):
        if dir == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.walls, False, collide_rect2)
            if hits:
                if hits[0].rect.centerx > self.collide_rect.centerx:
                    self.pos.x = hits[0].rect.left - self.collide_rect.width / 2
                if hits[0].rect.centerx < self.collide_rect.centerx:
                    self.pos.x = hits[0].rect.right + self.collide_rect.width / 2
                self.vel.x = 0
                self.collide_rect.centerx = self.pos.x
        if dir == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.walls, False, collide_rect2)
            if hits:
                if hits[0].rect.centery > self.collide_rect.centery:
                    self.pos.y = hits[0].rect.top - self.collide_rect.height / 2
                if hits[0].rect.centery < self.collide_rect.centery:
                    self.pos.y = hits[0].rect.bottom + self.collide_rect.height / 2
                self.vel.y = 0
                self.collide_rect.centery = self.pos.y

    def avoidEnemyRadius(self):
        # For each enemy in group, we get the diffrence betwence distance of all enemy and if within ENEMY_RADIUS
        # we accelerate away from them
        for enemy in self.game.enemy:
            if enemy != self:
                dist = self.pos - enemy.pos
                if 0 < dist.length() < ENEMY_RADIUS:
                    self.acc += dist.normalize()


class Bullet2(pygame.sprite.Sprite):
    def __init__(self, game, pos, direction):

        self.groups = game.all_sprites, game.bullets2
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.enemyBullet_img
        self.image= pygame.transform.scale(game.enemy_img,(10,10))
        self.rect = self.image.get_rect()
        self.pos = vect(pos)
        self.rect.center = self.pos
        self.vel = direction * BULLET_SPEED
        self.bullet_time = pygame.time.get_ticks()

    def update(self):
        # Position after shot
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos

        # Kill bullet after it hits wall
        if pygame.sprite.spritecollideany(self, self.game.walls):
            self.kill()

        # compares duration of bullet and if longer than enemy's last time then bullet is killed
        if pygame.time.get_ticks() - self.bullet_time > ENEMY_BULLET_LAST:
            self.kill()


class Bullet(pygame.sprite.Sprite):
    """Bullet that player shoots. Hits Enemy.

    Parameters
    ----------
    game : type
        Description of parameter `game`.
    pos : type
        Description of parameter `pos`.
    direction : type


    """
    def __init__(self, game, pos, direction):
        self.groups = game.all_sprites, game.bullets
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bullet_img
        self.rect = self.image.get_rect()  # Rectangle of image
        self.pos = vect(pos)
        self.rect.center = self.pos
        self.vel = direction * BULLET_SPEED
        self.bullet_time = pygame.time.get_ticks()

    def update(self):
        # Position after shot
        self.pos +=  self.vel * self.game.dt  # Calculates the position
        self.rect.center = self.pos

        # If bullet hits walls, then bullet is killed
        if pygame.sprite.spritecollideany(self, self.game.walls):
            self.kill()

        # compares duration of bullet and if longer than last time then bullet is killed
        if pygame.time.get_ticks() - self.bullet_time > BULLET_LAST:
            self.kill()


class Wall(pygame.sprite.Sprite):
    """WAll INFORMATION.

    Parameters
    ----------
    game : class
        Description of parameter `passes the game class`.
    x : type
        Description of parameter `passes the row`.
    y : type
        Description of parameter `passes the column`.

    Attributes
    ----------
    groups : type
        Description of attribute `creates a wall group to store all the walls`.
    image : type
        Description of attribute `creates the the tile images.
    rect : type
        Description of attribute `makes a rectangle of the image`.
    """
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(choice(COLORS))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
##########################PRINCESS NOT USED##################################################
'''
class Princess(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.image = game.princess_image
'''
##############################################################################################
