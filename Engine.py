import math
import time

class Point:
  def __init__(self,x,y,userData):
    self.x = x
    self.y = y
    self.userData = userData



class Rectangle:
  def __init__(self,x,y,w,h):
    self.x = x
    self.y = y
    self.w = w
    self.h = h

  def contains(self, point):
    return (
      point.x >= self.x - self.w and 
      point.x <= self.x + self.w and 
      point.y >= self.y - self.h and 
      point.y <= self.y + self.h
    )

  def intersects(self,range):
    return not (
      range.x - range.w > self.x + self.w or
      range.x + range.w < self.x - self.w or
      range.y - range.h > self.y + self.h or
      range.y + range.h < self.y - self.h
    )


class Circle:
  def __init__(self,x,y,r):
    self.x = x
    self.y = y
    self.r = r
    self.rSquared = self.r**2

  def contains(self, point):
    d = math.pow(point.x - self.x, 2) + math.pow(point.y - self.y, 2);
    return d <= self.rSquared;

  def intersects(self, range):
    xDist = abs(range.x - self.x);
    yDist = abs(range.y - self.y);
    
    r = self.r;

    w = range.w;
    h = range.h;

    edges = math.pow(xDist - w, 2) + math.pow(yDist - h, 2);

    if (xDist > r + w or yDist > r + h):
      return False;

    if (xDist <= w or yDist <= h):
      return True;

    return edges <= self.rSquared


class QuadTree:
  def __init__(self, boundary, capacity):
    if (not boundary):
      raise ValueError('boundary is null or undefined')
      
    if not isinstance(boundary, Rectangle):
      raise ValueError('boundary should be a Rectangle')

    if type(capacity) != (int or float):
      raise ValueError('capacity should be a number but is a', type(capacity))

    if (capacity < 1):
      raise ValueError('capacity must be greater than 0')

    self.boundary = boundary;
    self.capacity = capacity;
    self.points = [];
    self.divided = False

  def subdivide(self):
    x = self.boundary.x;
    y = self.boundary.y;
    w = self.boundary.w / 2;
    h = self.boundary.h / 2;

    ne = Rectangle(x + w, y - h, w, h);
    self.northeast = QuadTree(ne, self.capacity);
    nw = Rectangle(x - w, y - h, w, h);
    self.northwest = QuadTree(nw, self.capacity);
    se = Rectangle(x + w, y + h, w, h);
    self.southeast = QuadTree(se, self.capacity);
    sw = Rectangle(x - w, y + h, w, h);
    self.southwest = QuadTree(sw, self.capacity);

    self.divided = True

  def insert(self, point):
    if not self.boundary.contains(point):
      return False

    if (len(self.points) < self.capacity):
      self.points.append(point);
      return True

    if not self.divided:
      self.subdivide()

    if (
      self.northeast.insert(point) or
      self.northwest.insert(point) or
      self.southeast.insert(point) or
      self.southwest.insert(point)
    ):
      return True

  def query(self, range, found = False):
    if not found:
      found = []

    if not range.intersects(self.boundary):
      return found

    for p in self.points:
      if range.contains(p):
        found.append(p)
        
    if self.divided:
      self.northwest.query(range, found)
      self.northeast.query(range, found)
      self.southwest.query(range, found)
      self.southeast.query(range, found)

    return found




class Vector:
  def __init__(self, x = 0, y = 0):
    self.x = x
    self.y = y

  def add(self, vector):
    self.x+=vector.x
    self.y+=vector.y

  def __str__(self):
    return "(x:"+str(self.x)+",y:"+str(self.y)+")"


class Ellipse:
  def __init__(self, rx = 0, ry = 0, detail = 1):
    self.rx = rx
    self.ry = ry
    if self.rx != 0 and self.ry != 0:
      self.atoms = self.generateAtoms(detail)
    return

  def generateAtoms(self, step = 1):
    atoms = []
    for i in range(0, 360, step):
      ePX = self.rx  * math.cos(math.radians(i))
      ePY = self.ry * math.sin(math.radians(i))
      atoms.append(Vector(ePX, ePY))
    return atoms

  def getSize(self):
    if self.rx > self.ry:
      return self.rx
    else:
      return self.ry

  def __str__(self):
    return "Ellipse ("+str(self.rx)+", "+str(self.ry)+")"


class Rect:
  def __init__(self, w = 0, h = 0):
    self.w = w
    self.h = h
    return
    
  def getSize(self):
    if self.w > self.h:
      return self.w
    else:
      return self.h
      
  def __str__(self):
    return "Rect ("+str(self.w)+", "+str(self.h)+")"


class Object:
  def __init__(self, shape = Ellipse(0, 0), pos = Vector(0,0), mass = 1, gravity = False, immovable = False):
    self.shape = shape
    self.position = pos
    self.velocity = Vector(0, 0)
    self.mass = 1
    self.size = self.shape.getSize()
    self.forces = []
    self.affectedByGravity = gravity
    self.immovable = immovable
    return
    
  def update(self, gravity = None, g = None):
    if gravity and self.affectedByGravity:
      self.applyForce(a=g)
    for f in self.forces:
      self.velocity.add(f)
    self.position.add(self.velocity)
    self.forces = []
    return

  def applyForce(self, f=None, a=None):
    if f:
      self.forces.append(f/self.mass)
    elif a:
      self.forces.append(a)
    
    return
  
  def interact(self, obj):
    if self.immovable:
      return

    return

  def __str__(self):
    return str(self.shape)+", mass: "+str(self.mass)+", position: "+str(self.position)+", velocity: "+str(self.velocity)



class Engine:
  def __init__(self, world):
    self.world = world
    self.fps = 0
    self.framerate = 30
    self.objects = []
    self.gravity = False;
    self.g = Vector(0, 0)
    return

  def getObjects(self):
    return self.world.objects

  def setGravity(self, g=Vector(0, 0)):
    self.g = g
    return

  def enableGravity(self,state):
    self.gravity = state
    return

  def frameRate(self, fps = None):
    if fps:
      self.framerate = fps
    return self.fps

  def update(self):
    starttime = time.time()
    self.world.advance(self.gravity, self.g)
    loadtime = time.time() - starttime
    if 1000/self.framerate - loadtime > 0:
      time.sleep(((1000/self.framerate)-loadtime)/1000)
    finaltime = time.time() - starttime
    self.fps = 1/finaltime
    return

class World:
  def __init__(self, size = (100,100), qtreeSize = 4):
    self.size = size
    self.qTreeSize = qtreeSize
    self.boundary = Rectangle(self.size[0]/2, self.size[1]/2, self.size[0], self.size[1])
    self.qtree = QuadTree(self.boundary, self.qTreeSize)
    self.objects = []
    return

  def advance(self, gravity = None, g = None):
    self.qtree = QuadTree(self.boundary, self.qTreeSize)
    
    for p in self.objects:
      object = Point(p.position.x, p.position.y, p)
      self.qtree.insert(object)
      p.update(gravity, g)

    for p in self.objects:
      range = Circle(p.position.x, p.position.y, p.size * 2)
      points = self.qtree.query(range);
      for obj in points:
        other = obj.userData
        p.interact(other)

  def add(self, shape = Ellipse(0, 0), pos = Vector(0, 0), mass = 1, gravity = False, immovable = False):
    self.objects.append(Object(shape = shape, pos = pos, gravity=gravity, immovable=immovable))
    return


