from pygame import *
from math import *

width,height=1000,800
screen=display.set_mode((width, height))
RED=(255,0,0)
GREY=(127,127,127)
BLACK=(0,0,0)
BLUE=(0,0,255)
GREEN=(0,255,0)
YELLOW=(255,255,0)

running=True

myClock = time.Clock()

levels = [[[],[],[]]]

class Entity:
    def __init__(self, x, y):
        self.posX = x
        self.posY = y
        self.vy = -8
        self.jumping = False
        self.grounded = False
        self.falling = False

    def movePlayer(self):

        keys = key.get_pressed()

        if keys[K_a]:
            self.posX -= 5
            for platform in levels[level.currentLevel][level.getSquare(player.posY)]:
                r1 = Rect(self.posX-20, self.posY-20, 40, 40)
                r2 = Rect(platform)
                if Rect.colliderect(r1, r2) or self.posX-20 < 0:
                    self.posX += 5

        if keys[K_d]:
            self.posX += 5
            for platform in levels[level.currentLevel][level.getSquare(player.posY)]:
                r1 = Rect(self.posX-20, self.posY-20, 40, 40)
                r2 = Rect(platform)
                if Rect.colliderect(r1, r2) or self.posX+20 > width:
                    self.posX -= 5

        if self.jumping:
            self.vy += 0.25
            self.posY += self.vy
            if self.posY > 780 and level.getSquare(self.posY) == 0:
                self.posY = 780
                self.jumping = False
                self.grounded = True
                self.vy = -8
            else: 
                for platform in levels[level.currentLevel][level.getSquare(player.posY)]:
                    r1 = Rect(self.posX-20, self.posY-20, 40, 40)
                    r2 = Rect(platform)
                    if Rect.colliderect(r1, r2):
                        if r2[1] < r1[1]+40 < r2[1]+r2[3]:
                            self.posY = r2[1]-20
                            self.vy = -8
                            self.jumping = False
                        else:
                            self.vy = 1
                        break

        draw.circle(screen, GREEN, (player.posX, player.posY), 20)

class Level():
    def __init__(self):
        self.currentLevel = 0
        self.square = 0

    def getSquare(self, y):
        if y < 0 and self.square < 2:
            self.square+=1
            player.posY = height-30
            print("This ran 1")
        elif y > height and self.square > 0:
            self.square-=1
            player.posY = 30
            print("This ran 2")
        return(self.square)

    def draw(self):
        for platform in levels[self.currentLevel][self.getSquare(player.posY)]:
            draw.rect(screen, RED, platform)

player = Entity(20, 780)
level = Level()

while running:
    screen.fill((255, 255, 255))

    mx,my=mouse.get_pos()
    mb=mouse.get_pressed()

    for evt in event.get():
        if evt.type==QUIT:
            running=False
        if evt.type==KEYDOWN:
            if evt.key == K_SPACE and not player.jumping:
                player.jumping = True
        if evt.type == MOUSEBUTTONDOWN:
            if evt.button == 1:
                levels[0][level.getSquare(player.posY)].append((mx, my, 100, 50))

    player.movePlayer()
    level.draw()

    myClock.tick(60)
    display.flip()
            
quit()
