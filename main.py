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

  world.add(shape = Ellipse(30, 30, 1), pos = Vector(250, 150), vel = Vector(0, 0), mass = 1, gravity = True)
  world.add(shape = Ellipse(30, 30, 1), pos = Vector(250, 250), vel = Vector(0, 0), mass = 1, gravity = True)
  world.add(shape = Rect(500,10), pos = Vector(250,500), gravity = False, immovable = True)

  running = True
  while running:
    # print(*engine.getObjects(), sep='\n')

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    for object in engine.getObjects():
      pygame.draw.polygon(screen,(0, 0, 0),object.getAtoms())

    pygame.display.flip()
    
    engine.update()

  pygame.quit()
    
  