from pygame import *

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

levels = [[[(200, 300, 100, 50), (500, 400, 100, 50), (100, 765, 100, 50)]]]

class Entity:
    def __init__(self, x, y):
        self.posX = x
        self.posY = y
        self.jumping = False
        self.vy = -8

    def movePlayer(self):

        keys = key.get_pressed()

        if keys[K_a]:
                self.posX -= 5
        for platform in levels[level.currentLevel][level.getSquare(player.posY)]:
            r1 = Rect(self.posX-20, self.posY-20, 20, 20)
            r2 = Rect(platform)
            if Rect.colliderect(r1, r2):
                self.posX += 5

        if keys[K_d]:
                self.posX += 5
        for platform in levels[level.currentLevel][level.getSquare(player.posY)]:
            r1 = Rect(self.posX-20, self.posY-20, 20, 20)
            r2 = Rect(platform)
            if Rect.colliderect(r1, r2):
                self.posX -= 5

        #add gravity
        if self.jumping:
            self.vy += 0.25
            self.posY += self.vy
            for platform in levels[level.currentLevel][level.getSquare(player.posY)]:
                r1 = Rect(self.posX-20, self.posY-20, 40, 40)
                r2 = Rect(platform)
                if Rect.colliderect(r1, r2) or self.posY > 780:
                    self.posY-= self.vy
                    self.posY -= 0.25
                    self.jumping = False
                    self.vy = -8
                    self.useGravity = True
        
        draw.circle(screen, GREEN, (player.posX, player.posY), 20)

class Level():
    def __init__(self):
        self.currentLevel = 0
        self.square = 0

    def getSquare(self, y):
        if y < 0:
            self.square +=1 
        return(self.square)

    def draw(self):
        for platform in levels[self.currentLevel][self.getSquare(player.posY)]:
            draw.rect(screen, BLUE, platform)

player = Entity(20, 780)
level = Level()

while running:
    screen.fill(0)

    mx,my=mouse.get_pos()
    mb=mouse.get_pressed()

    for evt in event.get():
        if evt.type==QUIT:
            running=False
        if evt.type==KEYDOWN:
            if evt.key == K_SPACE and not player.jumping:
                player.jumping = True

    player.movePlayer()
    level.draw()

    myClock.tick(60)
    display.flip()
            
quit()
