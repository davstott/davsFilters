from turtle import *
import random
import math
from tkinter import *

debug = 0
s = Screen()
canvas = s.getcanvas()
tWorld = RawTurtle(s)
tParticle = RawTurtle(s)
tRobot = RawTurtle(s)
s.tracer(5, 0)
s.title("Foo")
s.register_shape("fooShape", ((4,0), (0, 4), (-4, 0), (0, -4)))
# 1 is black, 0 is white
# P(b|b) = 0.8, P(w|b) = 0.2
# P(b|w) = 0.1, P(w|w) = 0.9
# checkerboard, not all that useful
worldData = [ [1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 1, 0] , [0, 1, 0, 1]]

worldData = [ [1, 1, 1, 0, 0], [0, 1, 0, 0, 1], [1, 0, 1, 0, 0], [0, 1, 1, 1, 0], [0, 1, 0, 0, 0]]

cellsize = 40
movesize = 20
numparticles = 50
noisefactor = 0.2

def pick_particle(particles):
    r = random.random()
    cumulW = 0
    if debug: print ("the dice says " + str(r))
    for p in particles:
        cumulW += p.w
        if debug: print ("this p is " + str(p.w) + " total so far is " + str(cumulW))
        if cumulW >= r:
            if debug: print ("found it at " + str(p.w))
            return p.clone()

def generate_move(t):
    #pick a direction, left, right, straight
    #can I move cellsize in that direction?
    #yes, move it
    #no? try again until we run out of valid moves
    validDirections = [-90, 0, 90]
    while len(validDirections) > 0 :
        i = random.randrange(0, len(validDirections))
        if debug: print("start heading = " + str(t.heading()))
        newAngle = t.heading() + validDirections[i]
        xc = t.xcor()
        yc = t.ycor()
        newX = round(cellsize * math.cos(math.radians(newAngle)), 2)
        newY = round(cellsize * math.sin(math.radians(newAngle)), 2)
        if debug: print("newx = " + str(newX) + " newy = " + str(newY))
        if (0 < (t.xcor() + newX) < w.maxx) and (0 < (t.ycor() + newY) < w.maxy):
            t.left(validDirections[i])
            t.forward(cellsize)
            if debug: print("heading: new = " + str(t.heading()) + "| should be " + str(newAngle))
            if debug: print("x: new = " + str(t.xcor()) + "| should be " + str(xc) + " + " + str(newX))
            if debug: print("y: new = " + str(t.ycor()) + "| should be " + str(yc) + " + " + str(newY))
            return (newX, newY)
        else:
            if debug: print("bouncing")
            del validDirections[i]
    return 'fail'

def noisify(x):
    return x * ((random.random() * 2 * noisefactor) + (1 - noisefactor))

def correlate(world, particle):
    if world == 0:
        if particle == 0:
            return 0.9
        else:
            return 0.1
    else:
        if particle == 0 :
            return 0.2
        else:
            return 0.8

class P(object):
    def __init__(self, x, y, w = 1):
        self.x = int(x * 10) / 10
        self.y = int(y * 10) / 10
        self.w = w
        self.sensor = 0

    def move(self, x, y):
        self.x += x
        self.y += y
        #self.x = int(self.x * 10) / 10

    def setw(self, w):
        # hack much?
        #self.w = int(w * 1000) / 1000
        self.w = w

    def set_sensor(self, s):
        self.sensor = s
        """
        # this is a correlation thingy, not a sense thingy 
        if s == 0:
            if random.random() <= 0.9:
                self.sensor = 0
            else:
                self.sensor = 1
        if s == 1:
            if random.random() <= 0.8:
                self.sensor = 1
            else:
                self.sensor = 0
        """
    def clone(self):
        return (P(self.x, self.y, self.w))


class World(object):
    def __init__(self, data):
        self.data = data
        self.x = len(data[0])
        self.y = len(data)
        self.maxx = self.x * cellsize
        self.maxy = self.y * cellsize
        s.setworldcoordinates(0, 0, self.maxx, self.maxy)

    def draw_world(self, t):
        t.ht()
        for x in range(0, self.x):
            for y in range(0, self.y):
               if self.data[y][x] == 1:
                   t.color("black", "black")
               else:
                   t.color("black", "white")
               t.setheading(90)
               t.goto(x * cellsize, y * cellsize)
               t.down()
               t.begin_fill()
               for _ in range(0, 4):
                   t.forward(cellsize)
                   t.right(90)
               t.end_fill()
               t.up()

    def draw_particles(self, particles, t):
        t.reset()
        t.shape("fooShape")
        t.width(3)
        t.up()
        for p in particles:
            t.goto(p.x, p.y)
            if p.sensor == 1:
                t.color("red", "black")
            else:
                t.color("red", "white")
            t.stamp()

    def sense(self, x, y):
        return self.data[math.floor(y / cellsize)][math.floor(x / cellsize)]

w = World(worldData)

canvas.create_line(0, 0, w.maxx, w.maxy, fill="blue")
input("pause")
w.draw_world(tWorld)

particles = []
totalW = 0
for _ in range(0, numparticles):
    p = P(random.uniform(0, w.maxx), 
          random.uniform(0, w.maxy), 
          1 / numparticles)
    totalW += p.w
    particles.append(p)

tRobot.shape("classic")
s.tracer(1,0)
tRobot.up()
tRobot.goto(round(random.uniform(0, w.maxx), 2), round(random.uniform(0, w.maxy), 2))
tRobot.color("blue")
tRobot.down()
tRobot.st()
for p in particles:
    p.set_sensor(w.sense(p.x, p.y))

input("starting with t = " + str(totalW))


while 1:
    w.draw_particles(particles, tParticle)
    newparticles = []
    totalW = 0
    newmove = generate_move(tRobot)
    for _ in range(0, numparticles):
        p = pick_particle(particles)
        if debug: print ("start pos = " + str(p.x) + ", " + str(p.y) + " w = " + str(p.w))
        p.move(noisify(newmove[0]), noisify(newmove[1]))
        if debug: print ("new pos = " + str(p.x) + ", " + str(p.y))
        if (0 <= p.x <= w.maxx) and (0 <= p.y <= w.maxy):
            p.setw(noisify(correlate(w.sense(tRobot.xcor(), tRobot.ycor()),
                                     w.sense(p.x, p.y))))
            if debug: print ("new w = " + str(p.w))
            totalW += p.w
            newparticles.append(p)
        else:
            if debug: print ("skipping 'cos it's out of bounds")
    particles = newparticles
    newTotalW = 0
    for p in particles:
        p.setw(p.w / totalW)
        newTotalW += p.w

    input("step done. t = " + str(newTotalW))

input("Done, press return to bugger off")
