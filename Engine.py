import math
import time
import numpy as np
# from numpy import (array, dot, arccos, clip)
from numpy.linalg import norm

def Engine__onSegment__(p, q, r):
    if ( (q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and
           (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y))):
        return True
    return False
 
def Engine__orientation__(p, q, r):
    val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y))
    if (val > 0):
        return 1
    elif (val < 0):
        return 2
    else:
        return 0

def Engine__SegmentIntersect__(p1,q1,p2,q2):
    o1 = Engine__orientation__(p1, q1, p2)
    o2 = Engine__orientation__(p1, q1, q2)
    o3 = Engine__orientation__(p2, q2, p1)
    o4 = Engine__orientation__(p2, q2, q1)
    if ((o1 != o2) and (o3 != o4)):
        return True
    if ((o1 == 0) and Engine__onSegment__(p1, p2, q1)):
        return True
    if ((o2 == 0) and Engine__onSegment__(p1, q2, q1)):
        return True
    if ((o3 == 0) and Engine__onSegment__(p2, p1, q2)):
        return True
    if ((o4 == 0) and Engine__onSegment__(p2, q1, q2)):
        return True
    return False

def Engine__isInside__(circle_x, circle_y, radius, x, y):
    if ((x - circle_x) * (x - circle_x) +
        (y - circle_y) * (y - circle_y) <= radius**2):
        return True
    else:
        return False

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
    d = math.pow(point.x - self.x, 2) + math.pow(point.y - self.y, 2)
    return d <= self.rSquared

  def intersects(self, range):
    xDist = abs(range.x - self.x)
    yDist = abs(range.y - self.y)
    
    r = self.r

    w = range.w
    h = range.h

    edges = math.pow(xDist - w, 2) + math.pow(yDist - h, 2)

    if (xDist > r + w or yDist > r + h):
      return False

    if (xDist <= w or yDist <= h):
      return True

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

    self.boundary = boundary
    self.capacity = capacity
    self.points = []
    self.divided = False

  def subdivide(self):
    x = self.boundary.x
    y = self.boundary.y
    w = self.boundary.w / 2
    h = self.boundary.h / 2

    ne = Rectangle(x + w, y - h, w, h)
    self.northeast = QuadTree(ne, self.capacity)
    nw = Rectangle(x - w, y - h, w, h)
    self.northwest = QuadTree(nw, self.capacity)
    se = Rectangle(x + w, y + h, w, h)
    self.southeast = QuadTree(se, self.capacity)
    sw = Rectangle(x - w, y + h, w, h)
    self.southwest = QuadTree(sw, self.capacity)

    self.divided = True

  def insert(self, point):
    if not self.boundary.contains(point):
      return False

    if (len(self.points) < self.capacity):
      self.points.append(point)
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

  def mag(self):
    return math.sqrt(self.x**2+self.y**2)

  def getA(self):
    return [self.x, self.y]

  def getT(self):
    return (self.x, self.y)

  def sub(self, vector):
    self.x-=vector.x
    self.y-=vector.y
    return self

  def add(self, vector):
    self.x+=vector.x
    self.y+=vector.y
    return self

  def dot(self,vector):
    return np.dot(np.array(self.getA()),np.array(vector.getA()))
  
  def angle(self, vector):
    a = np.array(self.getA())
    b = np.array(vector.getA())
    inner = np.inner(a, b)
    norms = np.linalg.norm(a) * np.linalg.norm(b)
    cos = inner / norms
    rad = np.arccos(np.clip(cos, -1.0, 1.0))
    return rad

  def __mul__(self, n):
    self.x*=n
    self.y*=n
    return self

  def __pow__(self, n):
    self.x = self.x**n
    self.y = self.y**n
    return self
  
  def __truediv__(self, n):
    self.x/=n
    self.y/=n
    return self

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
  def __init__(self, w = 0, h = 0, detail = 1):
    self.w = w
    self.h = h
    if self.w != 0 and self.h != 0:
      self.atoms = self.generateAtoms(detail)
    return

  def generateAtoms(self, step = 1):
    atoms = []
    for i in range(0,self.w,step):
      atoms.append(Vector(i,-self.h))
    for i in range(0,2*self.h,step):
      atoms.append(Vector(self.w, -self.h+i))
    for i in range(0,2*self.w,step):
      atoms.append(Vector(self.w-i, self.h))
    for i in range(0,2*self.h,step):
      atoms.append(Vector(-self.w,self.h-i))
    for i in range(0,self.w,step):
      atoms.append(Vector(-self.w+i,-self.h))
    return atoms
    
  def getSize(self):
    if self.w > self.h:
      return self.w
    else:
      return self.h
      
  def __str__(self):
    return "Rect ("+str(self.w)+", "+str(self.h)+")"


class Object:
  def __init__(self, shape = Ellipse(0, 0), pos = Vector(0, 0), vel = Vector(0, 0), mass = 1, gravity = False, immovable = False):
    self.shape = shape
    self.position = pos
    self.velocity = vel
    self.mass = 1
    self.size = self.shape.getSize()
    self.forces = []
    self.affectedByGravity = gravity
    self.immovable = immovable
    return

  def getAtoms(self):
    a = [atom.getT() for atom in self.shape.atoms]
    atoms = []
    for atom in a:
      atoms.append((self.position.x+atom[0],self.position.y+atom[1]))
    return atoms
    
  def update(self, gravity = None, g = None):
    if gravity and self.affectedByGravity:
      self.applyForce(a=g)
    for f in self.forces:
      self.velocity.add(f)
    self.position.add(self.velocity)
    self.forces = []
    return

  def applyForce(self, f=None, a=None, angle=None):
    if f:
<<<<<<< HEAD
      if angle or angle==0:
        fx = f.mag()*math.sin(angle)
        fy = f.mag()*-math.cos(angle)
=======
      if angle:
        fx = f.mag()*-math.sin(angle)
        fy = f.mag()*math.cos(angle)
>>>>>>> a40b6112028a7344bf32aa3ea964ef3468a363b8
        self.forces.append(Vector(fx/self.mass,fy/self.mass))
      else:
        self.forces.append(Vector(f.x/self.mass,f.y/self.mass))
    elif a:
      self.forces.append(a)
    return
  
  def interact(self, obj):
    if self.immovable:
      return

    s = [Vector(i[0],i[1]) for i in self.getAtoms()]
    so = [Vector(i[0],i[1]) for i in obj.getAtoms() if Engine__isInside__(self.position.x,self.position.y,self.size,i[0],i[1])]

    ps = [0,0,0,0]
    ints = False

    for j in range(1,len(so)):
      k2 = so[j]
      k1 = so[j-1]
      for i in s:
        intersects = Engine__SegmentIntersect__(self.position,i,k1,k2)
        if intersects:
          ps[0] = self.position
          ps[1] = i
          ps[2] = k1
          ps[3] = k2
          ints = True
          break
    if ints:
      # print('Intersected')
      # print(*ps)
      # self.velocity.y = -self.velocity.y

      # angle = math.radians(0)
      angle = (self.velocity.angle(ps[3].sub(ps[2])))-math.pi/2
<<<<<<< HEAD
      f = self.velocity
      # print(math.degrees(angle))
      # ax = (self.velocity.x*2)*math.sin(angle)
      # ay = (self.velocity.y*2)*-math.cos(angle)
      self.applyForce(f = f, angle = angle)
=======
      print(math.degrees(angle))
      f = (self.velocity)*-1
      # print(f.mag())
      # ax = f.mag()*math.sin(angle)
      # ay = f.mag()*math.cos(angle)
      # self.applyForce(a=Vector(ax,ay))
      self.applyForce(f=f, angle = angle)
>>>>>>> a40b6112028a7344bf32aa3ea964ef3468a363b8
      self.position.x-=self.velocity.x
      self.position.y-=self.velocity.y

      # print(ax,ay)

    return

  def __str__(self):
    return str(self.shape)+", mass: "+str(self.mass)+", position: "+str(self.position)+", velocity: "+str(self.velocity)



class Engine:
  def __init__(self, world):
    self.world = world
    self.fps = 0
    self.framerate = 30
    self.objects = []
    self.gravity = False
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
      if not p.immovable:
        range = Circle(p.position.x, p.position.y, p.size*2)
        points = self.qtree.query(range)
        for obj in points:
          if obj.userData == p:
            points.remove(obj)
        for obj in points:
          other = obj.userData
          p.interact(other)


  def add(self, shape = Ellipse(0, 0), pos = Vector(0, 0), vel = Vector(0, 0), mass = 1, gravity = False, immovable = False):
    self.objects.append(Object(shape = shape, pos = pos, vel = vel, gravity=gravity, immovable=immovable))
    return

