from pygame import *
from math import sin

width,height=1000,800
screen=display.set_mode((width,height))
RED=(255,0,0)
GREY=(127,127,127)
BLACK=(0,0,0)
BLUE=(0,0,255)
GREEN=(0,255,0)
YELLOW=(255,255,0)

running=True
font.init()

wordY = 100
myClock = time.Clock()
while running:

    screen.fill((255,255,255))
    comicFont=font.SysFont("Comic Sans MS",80)
    picWord=comicFont.render("Where",True,BLACK)#converting the string into a picture
    screen.blit(picWord,(250,sin(wordY)*20+80))
    wordY+=0.005

    for evt in event.get():
        if evt.type==QUIT:
            running=False
                       
    mx,my=mouse.get_pos()
    mb=mouse.get_pressed()
      
    display.flip()
            
quit()