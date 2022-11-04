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
ladder = image.load("ladder.png")
ladder = transform.scale(ladder,(50,200))
background = image.load("background.jpg")
background = transform.scale(background, (1000,800))

playerImage = image.load("transparentastronaut_2.png")
playerImageLeft = transform.flip(playerImage, True, False)

class Entity:
    def __init__(self, x):
        self.vy = -8
        self.gravityVy = 1
        self.jumping = False
        self.falling = False
        self.grounded = True
        self.climbing = False
        self.width = 40
        self.height = 80
        self.posX = x
        self.posY = height - self.height
        self.movedLeft = False
        self.movedRight = False
        self.facing = "Right"
        
    def movePlayer(self):

        self.climbing = False
        self.movedLeft = False
        self.movedRight = False
        self.grounded = False
        
        keys = key.get_pressed()

        if keys[K_a]:
            self.posX -= 5
            self.movedLeft = True
            self.facing = "Left"
            
        if keys[K_d]:
            self.posX += 5
            self.movedRight = True
            self.facing = "Right"
        
        if self.jumping:
            self.vy += 0.25
            self.posY += self.vy
            self.falling = False
            self.grounded = False

        if level.getSquare(self.posY) == 0 and self.posY >= height-player.height:
            self.posY = height-player.height
            self.jumping = False
            self.grounded = True
            self.vy = -8
        
        for platform in levels[level.currentLevel][level.getSquare(player.posY)]:
            #platform and player
            r1 = Rect(self.posX, self.posY, self.width, self.height)
            r2 = Rect(platform)
            #rectangles for different parts of platforms
            topPlat = Rect(platform[0], platform[1], platform[2], 7)
            leftPlat = Rect(platform[0], platform[1], 1, platform[3])
            rightPlat = Rect(platform[0]+platform[2], platform[1], 1, platform[3])
            bottomPlat = Rect(platform[0]+3, platform[1]+platform[3]-7, platform[2]-6, 7)
            #rectangles for different parts of player
            bottomPlayer = Rect(self.posX, self.posY+(self.height-2), self.width, 5)
            topPlayer = Rect(self.posX+3, self.posY-2, player.width-3, 2)

            if (Rect.colliderect(r1, r2)):
                if platform[2] == 50:
                    if keys[K_w]:
                        self.posY-=5
                        self.climbing = True
                        self.jumping = False
                        self.falling = False
                        self.vy = -8
                        self.gravityVy = 1

            if Rect.colliderect(bottomPlayer, topPlat):
                self.falling = False
                self.posY = r2[1]-player.height-1
                self.vy = -8
                self.jumping = False
                self.falling = False
                self.grounded = True

            if self.jumping:
                if platform[2] != 50:
                    if (Rect.colliderect(r1, r2)):
                        if Rect.colliderect(bottomPlat, topPlayer):
                            self.posY = r2[1]+r2[3]-1
                            self.vy = 1

            if platform[2] != 50:
                if (Rect.colliderect(r1, rightPlat)) and self.movedLeft:
                    self.posX+=5
                    self.movedLeft = False
                if (Rect.colliderect(r1, leftPlat)) and self.movedRight:
                    self.posX-=5
                    self.movedRight = False
        
        if not self.jumping and not self.climbing and not self.grounded:
            self.falling = True
            self.gravityVy+=0.125
            self.posY += self.gravityVy
            if level.getSquare(self.posY) == 0 and self.posY >= height-player.height:
                self.posY = height-player.height
                self.falling = False
                self.gravityVy = 1
                self.grounded = True
        
        #draw.ellipse(screen, RED, (self.posX, self.posY, self.width, self.height))
        if self.facing == "Right":
            screen.blit(playerImageLeft, (self.posX, self.posY+5))
            # draw.rect(screen,GREEN,(player.posX+player.width, player.posY+player.height/2, 10, 5))
        else:
            screen.blit(playerImage, (self.posX, self.posY+5))

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
        return(self.square)

    def draw(self):
        for platformIn in levels[self.currentLevel][self.getSquare(player.posY)]:
            if platformIn[2] == 50:
                screen.blit(ladder,(platformIn[0],platformIn[1]))
            else:
                screen.blit(platform, (platformIn[0],platformIn[1]))

class Gun():
    def __init__(self):
        self.width = 50
        self.height = 20
    def drawGun(self):
        draw.rect(screen,GREEN,(player.posX+player.width, player.posY+player.height/2, self.width, self.height))

player = Entity(100)
level = Level()
gun = Gun()

while running:

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
            if evt.button == 3:
                levels[level.currentLevel][level.getSquare(player.posY)].append((mx, my, 50, 200))

    level.draw()
    player.movePlayer()
    #gun.drawGun()

    myClock.tick(60)
    display.flip()
            
quit()
