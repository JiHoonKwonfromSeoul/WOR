import pygame
import sys
from sprites import *
from config import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen=pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        
        self.clock=pygame.time.Clock()
        self.font=pygame.font.Font('arial.ttf',32)
        self.running=True

        self.character_spritesheet=Spritesheet('img/character.png')
        self.terrain_spritesheet=Spritesheet('img/terrain.png')
        self.enemy_spritesheet=Spritesheet('img/enemy.png')
        self.attack_spritesheet=Spritesheet('img/attack.png')
        self.intro_background=pygame.image.load('img/titleimage.png')
        self.go_background=pygame.image.load('img/gameover.jpg')
        self.player_spritesheet=Spritesheet('img/Boromir.png')


    def createTilemap(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self,j,i)
                if column=="B":
                    Block(self,j,i)
                elif column=="V":
                    BlockB(self,j,i)
                elif column=="E":
                    Enemy(self,j,i)
                elif column=="P":
                    self.player=Player(self,j,i)

    def new(self):
        self.playing=True
        self.all_sprites= pygame.sprite.LayeredUpdates()
        self.blocks=pygame.sprite.LayeredUpdates()
        self.enemies=pygame.sprite.LayeredUpdates()
        self.attacks=pygame.sprite.LayeredUpdates()
    
        self.createTilemap()


    def events(self):
        #game loop events
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.playing=False
                self.running=False

            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    if self.player.facing=='up':
                        Attack(self, self.player.rect.x, self.player.rect.y-TILESIZE)
                    if self.player.facing=='down':
                        Attack(self, self.player.rect.x, self.player.rect.y+TILESIZE)
                    if self.player.facing=='left':
                        Attack(self, self.player.rect.x-TILESIZE, self.player.rect.y)
                    if self.player.facing=='right':
                        Attack(self, self.player.rect.x+TILESIZE, self.player.rect.y )                       

    def update(self):
            self.all_sprites.update()

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)

        pygame.display.update()

    def main(self):
        #game loop
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def game_over(self):
        text=self.font.render('Game Over', True, WHITE)
        text_rect=text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        restart_button=Button(10, WINDOW_HEIGHT-60, 120, 50, WHITE, BLACK, 'Restart', 32)

        for sprite in self.all_sprites:
            sprite.kill()

        while self.running:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    self.running=False

            mouse_pos=pygame.mouse.get_pos()
            mouse_pressed=pygame.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.new()
                self.main()

            self.screen.blit(self.go_background, (0,0))
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def intro_screen(self):
        intro=True

        title=self.font.render('Defending Rohan', True, BISTRE)
        title_rect=title.get_rect(x=WINDOW_WIDTH/2-96,y=100)
        play_button=Button(WINDOW_WIDTH/2-32,WINDOW_HEIGHT/2+100,100,50,WHITE,BLACK,'Play',32)

        while intro:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    intro=False
                    self.running=False

            mouse_pos=pygame.mouse.get_pos()
            mouse_pressed=pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro=False

            self.screen.blit(self.intro_background,(0,0))
            self.screen.blit(title,title_rect)
            self.screen.blit(play_button.image,play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()


g=Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()