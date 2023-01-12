import pygame
import sys
from sprites import *
from config import *

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("DefendTheRohan!")
        self.icon=pygame.image.load('img/icon.png')
        pygame.display.set_icon(self.icon)
        self.screen=pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        
        self.clock=pygame.time.Clock()
        self.font=pygame.font.Font('arial.ttf',32)
        self.running=True
        self.character_spritesheet=Spritesheet('img/character.png')
        self.terrain_spritesheet=Spritesheet('img/terrain.png')
        self.enemy_spritesheet=Spritesheet('img/enemy.png')
        self.Lightorc_spritesheet=Spritesheet('img/LightOrc.png')
        self.HeavyOrc_spritesheet=Spritesheet('img/HeavyOrc.png')
        self.Sarumaun_spritesheet=Spritesheet('img/Sarumaun.png')
        self.attack_spritesheet=Spritesheet('img/attack.png')
        self.intro_background=pygame.image.load('img/titleimage.png')
        self.ingame_background=pygame.image.load('img/ingame.jpg')
        self.go_background=pygame.image.load('img/gameover.jpg')
        self.win_background=pygame.image.load('img/win.png')
        self.player_spritesheet=Spritesheet('img/Boromir.png')
        self.ingamebackground_rect=self.ingame_background.get_rect()
        
    def createTilemap(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self,j,i)
                if column=="W":
                    GroundW(self,j,i)
                elif column=="S":
                    GroundS(self, j, i)
                if column=="B":
                    Block(self,j,i)
                elif column=="V":
                    BlockB(self,j,i) and GroundW(self,j,i)
                elif column=="Z":
                    BlockB(self,j,i) and GroundS(self,j,i)
                elif column=="E":
                    Enemy(self,j,i)
                elif column=="L":
                    LightOrc(self,j,i)
                elif column=="H":
                    HeavyOrc(self,j,i)
                elif column=="M":
                    Sarumaun(self,j,i)

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

    def draw_text(surf, text, size, x, y):
        font=pygame.font.Font('arial',32)
        text_surface=font.render(text,True,WHITE)
        text_rect=text_surface.get_rect()
        text_rect.midtop=(x,y)
        surf.blit(text_surface,text_rect)

    def draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.ingame_background,self.ingamebackground_rect)
        self.all_sprites.draw(self.screen)
        text10=self.font.render("Defend!", True, BLACK)
        self.screen.blit(text10,[10,10])
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        #game loop
        while self.playing:
            start_ticks=pygame.time.get_ticks()
            self.events()
            self.update()
            self.draw()
 

    def game_over(self):
        text=self.font.render('Game Over', True, WHITE)
        text_rect=text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        restart_button=Button(WINDOW_WIDTH/2-32,WINDOW_HEIGHT/2+100,100,50,WHITE,BLACK,'Restart',24)

        for sprite in self.all_sprites:
            sprite.kill()

        while self.running:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    self.running=False
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_SPACE:
                        self.new()
                        self.main()

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
 
    def game_win(self):
        text1=self.font.render('Game WIN!', True, WHITE)
        text2=self.font.render('You Saved the Rohan!', True, WHITE)
        text1_rect=text1.get_rect(x=WINDOW_WIDTH/2-32, y=WINDOW_HEIGHT/2-54)
        text2_rect=text2.get_rect(x=WINDOW_WIDTH/2-64, y=WINDOW_HEIGHT/2)
        restart_button=Button(WINDOW_WIDTH/2-32,WINDOW_HEIGHT/2+100,100,50,WHITE,BLACK,'Restart',24)

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

            self.screen.blit(self.win_background, (0,0))
            self.screen.blit(text1, text1_rect)
            self.screen.blit(text2, text2_rect)
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
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_SPACE:
                        intro=False


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