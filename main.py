from Engine import *

if __name__ == "__main__":
  world = World(size=(500,500))
  engine  = Engine(world)

  world.add(Ellipse(10, 10), Vector(0,0))

  while True:
    engine.update()
  