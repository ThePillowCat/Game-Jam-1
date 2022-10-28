from pygame import *

width,height=800,800
screen=display.set_mode((1000, 800))
RED=(255,0,0)
GREY=(127,127,127)
BLACK=(0,0,0)
BLUE=(0,0,255)
GREEN=(0,255,0)
YELLOW=(255,255,0)

running=True

myClock = time.Clock()

levels = [[[(200, 300, 100, 50), (500, 400, 100, 50)]]]

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
        if keys[K_d]:
            self.posX += 5
        if self.jumping:
            self.vy += 0.25
            self.posY += self.vy
            if self.posY > 780:
                self.jumping = False
                self.vy = -8
                self.posY = 780

class Level():
    def __init__(self):
        pass

player = Entity(20, 780)

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

    draw.circle(screen, GREEN, (player.posX, player.posY), 20)
    for i in levels[0][0]:
        draw.rect(screen,BLUE,i)
    myClock.tick(60)
    display.flip()
            
quit()
