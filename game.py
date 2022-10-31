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
platform = image.load("purpleplatform_tintedcropped.png")
platform = transform.scale(platform,(200,50))
background = image.load("background.jpg")
background = transform.scale(background, (1000,800))


class Entity:
    def __init__(self, x, y):
        self.posX = x
        self.posY = y
        self.vy = -8
        self.gravityVy = 1
        self.jumping = False
        self.falling = False
        self.grounded = True
        self.radius = 40

    def movePlayer(self):

        keys = key.get_pressed()

        self.grounded = False

        if not self.grounded and not self.jumping:
            self.falling = True
            self.gravityVy += 0.125
            self.posY += self.gravityVy

        if (level.getSquare(player.posY) == 0 and self.posY > height-player.radius):
            self.grounded = True
            self.posY = height-player.radius
            self.gravityVy = 1
            self.falling = False

        for platform in levels[level.currentLevel][level.getSquare(player.posY)]:
            r1 = Rect(self.posX-20, self.posY-20, 40, 42)
            r2 = Rect(platform)
            if Rect.colliderect(r1, r2):
                if (r2[1] < r1[1]+42 < r2[1]+r2[3]):
                    self.posY = r2[1]-20
                    self.grounded = True
                    self.falling = False
                    self.gravityVy = 1

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
            self.falling = False
            if level.getSquare(self.posY) == 0 and self.posY > height-player.radius:
                self.posY = height-player.radius
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
                            self.falling = False
                            self.grounded = True
                        else:
                            self.vy = 1
                        break
        
        draw.circle(screen, RED, (player.posX, player.posY), player.radius)

class Level():
    def __init__(self):
        self.currentLevel = 0
        self.square = 0

    def getSquare(self, y):
        if y < 0 and self.square < 2:
            self.square+=1
            player.posY = height-30
        elif y > height and self.square > 0:
            self.square-=1
            player.posY = 30
            player.grounded = False
        return(self.square)

    def draw(self):
        for platformIn in levels[self.currentLevel][self.getSquare(player.posY)]:
            screen.blit(platform, (platformIn[0],platformIn[1]))

player = Entity(20, 760)
level = Level()

while running:
    
    # screen.fill((255, 255, 255))
    screen.blit(background, (0,0))

    mx,my=mouse.get_pos()
    mb=mouse.get_pressed()

    for evt in event.get():
        if evt.type==QUIT:
            running=False
        if evt.type==KEYDOWN:
            if evt.key == K_SPACE and not player.jumping and not player.falling:
                player.jumping = True
        if evt.type == MOUSEBUTTONDOWN:
            if evt.button == 1:
                levels[level.currentLevel][level.getSquare(player.posY)].append((mx, my, 200, 50))
            if evt.button == 2:
                print(levels)

    player.movePlayer()
    level.draw()

    myClock.tick(60)
    display.flip()
            
quit()
