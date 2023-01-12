import pygame
import sys
import math
import random
from config import *

class Spritesheet:
    def __init__(self, file):
        self.sheet=pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite=pygame.Surface([width, height])
        sprite.blit(self.sheet, (0,0), (x,y,width,height))
        sprite.set_colorkey(BLACK)
        return sprite

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game=game
        self._layer=PLAYER_LAYER
        self.groups=self.game.all_sprites
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x=x*TILESIZE
        self.y=y*TILESIZE
        self.width=TILESIZE*2
        self.height=TILESIZE*2

        self.x_change=0
        self.y_change=0

        self.facing='down'
        self.animation_loop=1
        
        self.image=self.game.player_spritesheet.get_sprite(0,640,self.width,self.width)

        self.rect=self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y

        self.down_animations = [self.game.player_spritesheet.get_sprite(0, 640, self.width, self.height),
                           self.game.player_spritesheet.get_sprite(192, 640, self.width, self.height),
                           self.game.player_spritesheet.get_sprite(384, 640, self.width, self.height)]

        self.up_animations = [self.game.player_spritesheet.get_sprite(0,512, self.width, self.height),
                         self.game.player_spritesheet.get_sprite(192, 512, self.width, self.height),
                         self.game.player_spritesheet.get_sprite(384, 512, self.width, self.height)]

        self.left_animations = [self.game.player_spritesheet.get_sprite(0, 574, self.width, self.height),
                           self.game.player_spritesheet.get_sprite(192, 574, self.width, self.height),
                           self.game.player_spritesheet.get_sprite(384, 574, self.width, self.height)]

        self.right_animations = [self.game.player_spritesheet.get_sprite(0, 704, self.width, self.height),
                            self.game.player_spritesheet.get_sprite(192, 704, self.width, self.height),
                            self.game.player_spritesheet.get_sprite(384, 704, self.width, self.height)]
        
    def update(self):

        self.movement()

        if self.rect.y+self.height>WINDOW_HEIGHT:
            self.rect.y=WINDOW_HEIGHT-self.height
        if self.rect.y<0:
            self.rect.y=0

        self.animate()
        self.collide_enemy()

        self.rect.x+=self.x_change
        self.collide_blocks('x')
        self.rect.y+=self.y_change
        self.collide_blocks('y')


        self.x_change=0
        self.y_change=0
    


    def movement(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if self.rect.x<WINDOW_WIDTH/2:
                for sprite in self.game.all_sprites:
                    sprite.rect.x+=PLAYER_SPEED
            self.x_change-=PLAYER_SPEED
            self.facing='left'
        if keys[pygame.K_RIGHT]:
            if self.rect.x>WINDOW_WIDTH/2:
                for sprite in self.game.all_sprites:
                    sprite.rect.x-=PLAYER_SPEED
            self.x_change+=PLAYER_SPEED
            self.facing='right'
        if keys[pygame.K_UP]:
            #for sprite in self.game.all_sprites:
            #    sprite.rect.y-=PLAYER_SPEED
            self.y_change-=PLAYER_SPEED
            self.facing='up'
        if keys[pygame.K_DOWN]:
            #for sprite in self.game.all_sprites:
            #    sprite.rect.y+=PLAYER_SPEED
            self.y_change+=PLAYER_SPEED
            self.facing='down'

    def collide_enemy(self):
        hits=pygame.sprite.spritecollide(self,self.game.enemies,False)
        if hits:
            self.kill()
            self.game.playing=False

    def collide_blocks(self, direction):
        if direction=="x":
            hits=pygame.sprite.spritecollide(self,self.game.blocks,False)
            if hits:
                if self.x_change>0:
                    self.rect.x=hits[0].rect.left-self.rect.width
                if self.x_change<0:
                    self.rect.x=hits[0].rect.right
        if direction=="y":
            hits=pygame.sprite.spritecollide(self,self.game.blocks,False)
            if hits:
                if self.y_change>0:
                    self.rect.y=hits[0].rect.top-self.rect.height
                if self.y_change<0:
                    self.rect.y=hits[0].rect.bottom

    def animate(self):
        
        if self.facing=="down":
            if self.y_change==0:
                self.image=self.game.player_spritesheet.get_sprite(0,640,self.width,self.height)
            else:
                self.image=self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop+=0.1
                if self.animation_loop>=3:
                    self.animation_loop=1

        if self.facing=="up":
            if self.y_change==0:
                self.image=self.game.player_spritesheet.get_sprite(0,512,self.width,self.height)
            else:
                self.image=self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop+=0.1
                if self.animation_loop>=3:
                    self.animation_loop=1

        if self.facing=="left":
            if self.x_change==0:
                self.image=self.game.player_spritesheet.get_sprite(0, 574,self.width,self.height)
            else:
                self.image=self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop+=0.1
                if self.animation_loop>=3:
                    self.animation_loop=1

        if self.facing=="right":
            if self.x_change==0:
                self.image=self.game.player_spritesheet.get_sprite(0, 704,self.width,self.height)
            else:
                self.image=self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop+=0.1
                if self.animation_loop>=3:
                    self.animation_loop=1

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x,y):

        self.game=game
        self._layer=ENEMY_LAYER
        self.groups=self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x=x*TILESIZE
        self.y=y*TILESIZE
        self.width=TILESIZE
        self.height=TILESIZE

        self.x_change=0
        self.y_change=0

        self.facing=random.choice(['left','right','down'])

        self.animation_loop=1
        self.movement_loop=0
        self.max_travel=random.randint(10,30)

        self.image=self.game.enemy_spritesheet.get_sprite(3,2,self.width,self.height)
        self.image.set_colorkey(BLACK)

        self.rect=self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y
        
        self.down_animations = [self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(35, 2, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(68, 2, self.width, self.height)]

        self.up_animations = [self.game.enemy_spritesheet.get_sprite(3, 34, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(35, 34, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(68, 34, self.width, self.height)]
        
        self.left_animations = [self.game.enemy_spritesheet.get_sprite(3, 98, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(35, 98, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(68, 98, self.width, self.height)]

        self.right_animations = [self.game.enemy_spritesheet.get_sprite(3, 66, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(35, 66, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(68, 66, self.width, self.height)]
        
    def update(self):
        self.movement()
        self.rect.y+=1
        if self.rect.y+self.height>WINDOW_HEIGHT:
            self.kill()
        if self.rect.y<0:
            self.kill()
        self.animate()
        self.rect.x+=self.x_change
        self.rect.y+=self.y_change
        self.x_change=0
        self.y_change=0
    
    def movement(self):
        if self.facing=='left':
            self.x_change-=ENEMY_SPEED
            self.movement_loop-=1
            if self.movement_loop<=-self.max_travel:
                self.facing='right'

        if self.facing=='right':
            self.x_change+=ENEMY_SPEED
            self.movement_loop+=1
            if self.movement_loop>=self.max_travel:
                self.facing='left'

        if self.facing=='down':
            self.y_change+=ENEMY_SPEED
            self.movement_loop-=1
            if self.movement_loop<=-self.max_travel:
                self.facing='down'

        if self.facing=='up':
            self.y_change-=ENEMY_SPEED
            self.movement_loop+=1
            if self.movement_loop>=self.max_travel:
                self.facing='up'

    def animate(self):
        
        if self.facing=="down":
            if self.y_change==0:
                self.image=self.game.enemy_spritesheet.get_sprite(3,2,self.width,self.height)
            else:
                self.image=self.down_animations[math.floor(self.animation_loop)]

                self.animation_loop+=0.1
                if self.animation_loop>=3:
                    self.animation_loop=1

        if self.facing=="up":
            if self.y_change==0:
                self.image=self.game.enemy_spritesheet.get_sprite(3,34,self.width,self.height)
            else:
                self.image=self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop+=0.1
                if self.animation_loop>=3:
                    self.animation_loop=1
        
        if self.facing=="left":
            if self.x_change==0:
                self.image=self.game.enemy_spritesheet.get_sprite(3,98,self.width,self.height)
            else:
                self.image=self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop+=0.1
                if self.animation_loop>=3:
                    self.animation_loop=1

        if self.facing=="right":
            if self.x_change==0:
                self.image=self.game.enemy_spritesheet.get_sprite(3,66,self.width,self.height)
            else:
                self.image=self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop+=0.1
                if self.animation_loop>=3:
                    self.animation_loop=1

class LightOrc(pygame.sprite.Sprite):
    def __init__(self, game, x,y):

        self.game=game
        self._layer=ENEMY_LAYER
        self.groups=self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x=x*TILESIZE
        self.y=y*TILESIZE
        self.width=TILESIZE*2
        self.height=TILESIZE*2

        self.x_change=0
        self.y_change=0

        self.facing=random.choice(['left','right','down'])

        self.animation_loop=1
        self.movement_loop=0
        self.max_travel=random.randint(10,30)

        self.image=self.game.Lightorc_spritesheet.get_sprite(0,640,self.width,self.height)
        self.image.set_colorkey(BLACK)

        self.rect=self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y

        
        self.down_animations = [self.game.Lightorc_spritesheet.get_sprite(0,640, self.width, self.height),
                           self.game.Lightorc_spritesheet.get_sprite(192,640, self.width, self.height),
                           self.game.Lightorc_spritesheet.get_sprite(384, 640, self.width, self.height)]

        self.up_animations = [self.game.Lightorc_spritesheet.get_sprite(0,512, self.width, self.height),
                         self.game.Lightorc_spritesheet.get_sprite(192,512, self.width, self.height),
                         self.game.Lightorc_spritesheet.get_sprite(384,512, self.width, self.height)]
        
        self.left_animations = [self.game.Lightorc_spritesheet.get_sprite(0,575, self.width, self.height),
                           self.game.Lightorc_spritesheet.get_sprite(192, 575, self.width, self.height),
                           self.game.Lightorc_spritesheet.get_sprite(384, 575, self.width, self.height)]

        self.right_animations = [self.game.Lightorc_spritesheet.get_sprite(0, 705, self.width, self.height),
                            self.game.Lightorc_spritesheet.get_sprite(192, 705, self.width, self.height),
                            self.game.Lightorc_spritesheet.get_sprite(384, 705, self.width, self.height)]
        

    def update(self):
        self.movement()
        if self.rect.y+self.height>WINDOW_HEIGHT:
            self.kill()
        if self.rect.y<0:
            self.kill()
        self.animate()
        self.rect.x+=self.x_change
        self.rect.y+=self.y_change
        self.rect.y+=1
        self.x_change=0
        self.y_change=0
    
    def movement(self):
        if self.facing=='left':
            self.x_change-=ENEMY2_SPEED
            self.movement_loop-=1
            if self.movement_loop<=-self.max_travel:
                self.facing='right'

        if self.facing=='right':
            self.x_change+=ENEMY2_SPEED
            self.movement_loop+=1
            if self.movement_loop>=self.max_travel:
                self.facing='left'

        if self.facing=='down':
            self.y_change+=ENEMY2_SPEED
            self.movement_loop-=1
            if self.movement_loop<=-self.max_travel:
                self.facing='down'

        if self.facing=='up':
            self.y_change-=ENEMY2_SPEED
            self.movement_loop+=1
            if self.movement_loop>=self.max_travel:
                self.facing='up'

    def animate(self):
        
        if self.facing=="down":
            if self.y_change==0:
                self.image=self.game.Lightorc_spritesheet.get_sprite(0,640,self.width,self.height)
            else:
                self.image=self.down_animations[math.floor(self.animation_loop)]

                self.animation_loop+=0.1
                if self.animation_loop>=3:
                    self.animation_loop=1

        if self.facing=="up":
            if self.y_change==0:
                self.image=self.game.Lightorc_spritesheet.get_sprite(0,512,self.width,self.height)
            else:
                self.image=self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop+=0.1
                if self.animation_loop>=3:
                    self.animation_loop=1
        
        if self.facing=="left":
            if self.x_change==0:
                self.image=self.game.Lightorc_spritesheet.get_sprite(0,575,self.width,self.height)
            else:
                self.image=self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop+=0.1
                if self.animation_loop>=3:
                    self.animation_loop=1

        if self.facing=="right":
            if self.x_change==0:
                self.image=self.game.Lightorc_spritesheet.get_sprite(0,705,self.width,self.height)
            else:
                self.image=self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop+=0.1
                if self.animation_loop>=3:
                    self.animation_loop=1

class HeavyOrc(pygame.sprite.Sprite):
    def __init__(self, game, x,y):

        self.game=game
        self._layer=ENEMY_LAYER
        self.groups=self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x=x*TILESIZE
        self.y=y*TILESIZE
        self.width=TILESIZE*2
        self.height=TILESIZE*2

        self.x_change=0
        self.y_change=0

        self.facing=random.choice(['left','right','down'])

        self.animation_loop=1
        self.movement_loop=0
        self.max_travel=random.randint(10,30)

        self.image=self.game.HeavyOrc_spritesheet.get_sprite(0,640,self.width,self.height)
        self.image.set_colorkey(BLACK)

        self.rect=self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y

        
        self.down_animations = [self.game.HeavyOrc_spritesheet.get_sprite(0,640, self.width, self.height),
                           self.game.HeavyOrc_spritesheet.get_sprite(192,640, self.width, self.height),
                           self.game.HeavyOrc_spritesheet.get_sprite(384, 640, self.width, self.height)]

        self.up_animations = [self.game.HeavyOrc_spritesheet.get_sprite(0,512, self.width, self.height),
                         self.game.HeavyOrc_spritesheet.get_sprite(192,512, self.width, self.height),
                         self.game.HeavyOrc_spritesheet.get_sprite(384,512, self.width, self.height)]
        
        self.left_animations = [self.game.HeavyOrc_spritesheet.get_sprite(0,575, self.width, self.height),
                           self.game.HeavyOrc_spritesheet.get_sprite(192, 575, self.width, self.height),
                           self.game.HeavyOrc_spritesheet.get_sprite(384, 575, self.width, self.height)]

        self.right_animations = [self.game.HeavyOrc_spritesheet.get_sprite(0, 705, self.width, self.height),
                            self.game.HeavyOrc_spritesheet.get_sprite(192, 705, self.width, self.height),
                            self.game.HeavyOrc_spritesheet.get_sprite(384, 705, self.width, self.height)]
        

    def update(self):
        self.movement()
        if self.rect.y+self.height>WINDOW_HEIGHT:
            self.kill()
        if self.rect.y<0:
            self.kill()
        self.animate()
        self.rect.x+=self.x_change
        self.rect.y+=self.y_change
        self.rect.y+=1
        self.x_change=0
        self.y_change=0
    
    def movement(self):
        if self.facing=='left':
            self.x_change-=ENEMY_SPEED
            self.movement_loop-=1
            if self.movement_loop<=-self.max_travel:
                self.facing='right'

        if self.facing=='right':
            self.x_change+=ENEMY_SPEED
            self.movement_loop+=1
            if self.movement_loop>=self.max_travel:
                self.facing='left'

        if self.facing=='down':
            self.y_change+=ENEMY_SPEED
            self.movement_loop-=1
            if self.movement_loop<=-self.max_travel:
                self.facing='down'

        if self.facing=='up':
            self.y_change-=ENEMY_SPEED
            self.movement_loop+=1
            if self.movement_loop>=self.max_travel:
                self.facing='up'

    def animate(self):
        
        if self.facing=="down":
            if self.y_change==0:
                self.image=self.game.HeavyOrc_spritesheet.get_sprite(0,640,self.width,self.height)
            else:
                self.image=self.down_animations[math.floor(self.animation_loop)]

                self.animation_loop+=0.1
                if self.animation_loop>=3:
                    self.animation_loop=1

        if self.facing=="up":
            if self.y_change==0:
                self.image=self.game.HeavyOrc_spritesheet.get_sprite(0,512,self.width,self.height)
            else:
                self.image=self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop+=0.1
                if self.animation_loop>=3:
                    self.animation_loop=1
        
        if self.facing=="left":
            if self.x_change==0:
                self.image=self.game.HeavyOrc_spritesheet.get_sprite(0,575,self.width,self.height)
            else:
                self.image=self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop+=0.1
                if self.animation_loop>=3:
                    self.animation_loop=1

        if self.facing=="right":
            if self.x_change==0:
                self.image=self.game.HeavyOrc_spritesheet.get_sprite(0,705,self.width,self.height)
            else:
                self.image=self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop+=0.1
                if self.animation_loop>=3:
                    self.animation_loop=1

class Sarumaun(pygame.sprite.Sprite):
    def __init__(self, game, x,y):

        self.game=game
        self._layer=ENEMY_LAYER
        self.groups=self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x=x*TILESIZE
        self.y=y*TILESIZE
        self.width=TILESIZE*2
        self.height=TILESIZE*2

        self.x_change=0
        self.y_change=0

        self.facing=random.choice(['left','right','down'])

        self.animation_loop=1
        self.movement_loop=0
        self.max_travel=random.randint(10,30)

        self.image=self.game.Sarumaun_spritesheet.get_sprite(0,640,self.width,self.height)
        self.image.set_colorkey(BLACK)

        self.rect=self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y

        
        self.down_animations = [self.game.Sarumaun_spritesheet.get_sprite(0,640, self.width, self.height),
                           self.game.Sarumaun_spritesheet.get_sprite(192,640, self.width, self.height),
                           self.game.Sarumaun_spritesheet.get_sprite(384, 640, self.width, self.height)]

        self.up_animations = [self.game.Sarumaun_spritesheet.get_sprite(0,512, self.width, self.height),
                         self.game.Sarumaun_spritesheet.get_sprite(192,512, self.width, self.height),
                         self.game.Sarumaun_spritesheet.get_sprite(384,512, self.width, self.height)]
        
        self.left_animations = [self.game.Sarumaun_spritesheet.get_sprite(0,574, self.width, self.height),
                           self.game.Sarumaun_spritesheet.get_sprite(192, 574, self.width, self.height),
                           self.game.Sarumaun_spritesheet.get_sprite(384, 574, self.width, self.height)]

        self.right_animations = [self.game.Sarumaun_spritesheet.get_sprite(0, 704, self.width, self.height),
                            self.game.Sarumaun_spritesheet.get_sprite(192, 704, self.width, self.height),
                            self.game.Sarumaun_spritesheet.get_sprite(384, 704, self.width, self.height)]
        

    def update(self):
        self.movement()
        if self.rect.y+self.height>WINDOW_HEIGHT:
            self.kill()
        if self.rect.y<0:
            self.kill()
        self.animate()
        self.rect.x+=self.x_change
        self.rect.y+=self.y_change
        self.rect.y+=1
        self.x_change=0
        self.y_change=0
    
    def movement(self):
        if self.facing=='left':
            self.x_change-=ENEMY_SPEED
            self.movement_loop-=1
            if self.movement_loop<=-self.max_travel:
                self.facing='right'

        if self.facing=='right':
            self.x_change+=ENEMY_SPEED
            self.movement_loop+=1
            if self.movement_loop>=self.max_travel:
                self.facing='left'

        if self.facing=='down':
            self.y_change+=ENEMY_SPEED
            self.movement_loop-=1
            if self.movement_loop<=-self.max_travel:
                self.facing='down'

        if self.facing=='up':
            self.y_change-=ENEMY_SPEED
            self.movement_loop+=1
            if self.movement_loop>=self.max_travel:
                self.facing='up'

    def animate(self):
        
        if self.facing=="down":
            if self.y_change==0:
                self.image=self.game.Sarumaun_spritesheet.get_sprite(0,640,self.width,self.height)
            else:
                self.image=self.down_animations[math.floor(self.animation_loop)]

                self.animation_loop+=0.1
                if self.animation_loop>=3:
                    self.animation_loop=1

        if self.facing=="up":
            if self.y_change==0:
                self.image=self.game.Sarumaun_spritesheet.get_sprite(0,512,self.width,self.height)
            else:
                self.image=self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop+=0.1
                if self.animation_loop>=3:
                    self.animation_loop=1
        
        if self.facing=="left":
            if self.x_change==0:
                self.image=self.game.Sarumaun_spritesheet.get_sprite(0,574,self.width,self.height)
            else:
                self.image=self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop+=0.1
                if self.animation_loop>=3:
                    self.animation_loop=1

        if self.facing=="right":
            if self.x_change==0:
                self.image=self.game.Sarumaun_spritesheet.get_sprite(0,704,self.width,self.height)
            else:
                self.image=self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop+=0.1
                if self.animation_loop>=3:
                    self.animation_loop=1


class Block(pygame.sprite.Sprite):
    def __init__(self, game, x,y):

        self.game=game
        self._layer=BLOCK_LAYER
        self.groups=self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self,self.groups)
        
        self.x=x*TILESIZE
        self.y=y*TILESIZE
        self.width=TILESIZE
        self.height=TILESIZE

        self.image=self.game.terrain_spritesheet.get_sprite(960,448,self.width,self.height)

        self.rect=self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y

class BlockB(pygame.sprite.Sprite):
    def __init__(self, game, x,y):

        self.game=game
        self._layer=BLOCK_LAYER
        self.groups=self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self,self.groups)
        
        self.x=x*TILESIZE
        self.y=y*TILESIZE
        self.width=TILESIZE
        self.height=TILESIZE

        self.image=self.game.terrain_spritesheet.get_sprite(960+32,448+32*3,self.width,self.height)

        self.rect=self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y

class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x,y):
        self.game=game
        self._layer=GROUND_LAYER
        self.groups=self.game.all_sprites
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x=x*TILESIZE
        self.y=y*TILESIZE
        self.width=TILESIZE
        self.height=TILESIZE

        self.image=self.game.terrain_spritesheet.get_sprite(64,352,self.width,self.height)

        self.rect=self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y

class GroundW(pygame.sprite.Sprite):
    def __init__(self, game, x,y):
        self.game=game
        self._layer=GROUND_LAYER
        self.groups=self.game.all_sprites
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x=x*TILESIZE
        self.y=y*TILESIZE
        self.width=TILESIZE
        self.height=TILESIZE

        self.image=self.game.terrain_spritesheet.get_sprite(288,480,self.width,self.height)

        self.rect=self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y

class GroundS(pygame.sprite.Sprite):
    def __init__(self, game, x,y):
        self.game=game
        self._layer=GROUND_LAYER
        self.groups=self.game.all_sprites
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x=x*TILESIZE
        self.y=y*TILESIZE
        self.width=TILESIZE
        self.height=TILESIZE

        self.image=self.game.terrain_spritesheet.get_sprite(420,95,self.width,self.height)

        self.rect=self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y

class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x,y):
        self.game=game
        self._layer=GROUND_LAYER
        self.groups=self.game.all_sprites
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x=x*TILESIZE
        self.y=y*TILESIZE
        self.width=TILESIZE
        self.height=TILESIZE

        self.image=self.game.terrain_spritesheet.get_sprite(112,447,self.width,self.height)

        self.rect=self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y

class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font=pygame.font.Font('arial.ttf', fontsize)
        self.content=content
        
        self.x=x
        self.y=y
        self.width=width
        self.height=height

        self.fg=fg
        self.bg=bg

        self.image=pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect=self.image.get_rect()

        self.rect.x=self.x
        self.rect.y=self.y

        self.text=self.font.render(self.content, True, self.fg)
        self.text_rect=self.text.get_rect(center=(self.width/2,self.height/2))
        self.image.blit(self.text,self.text_rect)

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False

class Attack(pygame.sprite.Sprite):

    def __init__(self, game, x, y):

        self.game=game
        self._layer=PLAYER_LAYER
        self.groups=self.game.all_sprites,self.game.attacks
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.x=x+16
        self.y=y+16
        self.width=TILESIZE*2
        self.height=TILESIZE*2

        self.animation_loop=0

        self.image=self.game.attack_spritesheet.get_sprite(0,0,self.width,self.height)

        self.rect=self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y
        self.down_animations = [self.game.attack_spritesheet.get_sprite(0, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32*2, 32*2, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64*2, 32*2, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96*2, 32*2, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128*2, 32*2, self.width, self.height)]
 
        self.up_animations = [self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(32*2, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(64*2, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(96*2, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(128*2, 0, self.width, self.height)]

        self.left_animations = [self.game.attack_spritesheet.get_sprite(0, 96*2, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32*2, 96*2, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64*2, 96*2, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96*2, 96*2, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128*2, 96*2, self.width, self.height)]

        self.right_animations = [self.game.attack_spritesheet.get_sprite(0, 64*2, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32*2, 64*2, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64*2, 64*2, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96*2, 64*2, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128*2, 64*2, self.width, self.height)]

    def update(self):
        self.animate()
        self.collide()

    def collide(self):
        hits=pygame.sprite.spritecollide(self,self.game.enemies,True)

    def animate(self):
        direction=self.game.player.facing

        if direction=='down':
            self.image=self.down_animations[math.floor(self.animation_loop)]
            self.animation_loop+=0.5
            if self.animation_loop>=5:
                self.kill()

        if direction=='up':
            self.image=self.up_animations[math.floor(self.animation_loop)]
            self.animation_loop+=0.5
            if self.animation_loop>=5:
                self.kill()

        if direction=='left':
            self.image=self.left_animations[math.floor(self.animation_loop)]
            self.animation_loop+=0.5
            if self.animation_loop>=5:
                self.kill()

        if direction=='right':
            self.image=self.right_animations[math.floor(self.animation_loop)]
            self.animation_loop+=0.5
            if self.animation_loop>=5:
                self.kill()