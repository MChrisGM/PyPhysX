from Engine import *

if __name__ == "__main__":
  world = World(size=(500,500))
  engine  = Engine(world)
  
  engine.frameRate(60)
  
  engine.enableGravity(True)
  engine.setGravity(Vector(0, 10))

  world.add(Ellipse(10, 10), Vector(250,250))

  while True:
    engine.update()
    
  