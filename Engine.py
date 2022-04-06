import math

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


class Ellipse:
  def __init__(self, rx = 0, ry = 0):
    self.rx = rx
    self.ry = ry
    return

  def getSize(self):
    if self.rx > self.ry:
      return self.rx
    else:
      return self.ry


class Rect:
  def __init__(self, w = 0, h = 0):
    self.w = w
    self.h = h
    return


class Object:
  def __init__(self, objectType = Ellipse(0, 0), pos = Vector(0,0)):
    self.shape = objectType
    self.position = pos
    self.size = self.shape.getSize()
    return
    
  def update(self):
    return
  def interact(self, obj):
    return



class Engine:
  def __init__(self, world):
    self.world = world
    self.objects = []
    return

  def update(self):
    self.world.advance()
    return


class World:
  def __init__(self, size = (100,100), qtreeSize = 4):
    self.size = size
    self.qTreeSize = qtreeSize
    self.boundary = Rectangle(self.size[0]/2, self.size[1]/2, self.size[0], self.size[1])
    self.qtree = QuadTree(self.boundary, self.qTreeSize)
    self.objects = []
    return

  def advance(self):
    for p in self.objects:
      object = Point(p.position.x, p.position.y, p)
      self.qtree.insert(object)
      p.update()

    for p in self.objects:
      range = Circle(p.position.x, p.position.y, p.size * 2)
      points = self.qtree.query(range);
      for obj in points:
        other = obj.userData
        p.interact(other)

  def add(self, obj = Ellipse(0, 0), pos = Vector(0, 0)):
    self.objects.append(Object(obj, pos))
    return

