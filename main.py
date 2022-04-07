from Engine import *

import pygame
pygame.init()

if __name__ == "__main__":

  screen = pygame.display.set_mode([500, 500])
  
  world = World(size=(500,500))
  engine  = Engine(world)
  
  engine.frameRate(60)
  
  engine.enableGravity(True)
  engine.setGravity(Vector(0, 1))

  el = Ellipse(10, 10)
  
  world.add(shape = el, pos = Vector(250,250), mass = 1, gravity = True)
  world.add(shape = Rect(500,10),pos = Vector(250,500), gravity = False, immovable = True)

  while True:
    # print(*engine.getObjects(), sep='\n')

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    pygame.draw.circle(screen, (0, 0, 0), (250, 250), 75)

    pygame.display.flip()
    
    engine.update()

  pygame.quit()
    
  