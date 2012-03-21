from turtle import *
import random
import math

xmin = 0 
xmax = 20
numparticles = 50
noisefactor = 0.3

def noisify(x):
    return x * ((random.random() * 2 * noisefactor) + (1 - noisefactor))

# from http://stackoverflow.com/questions/509994/best-way-to-write-a-python-function-that-integrates-a-gaussian 
def make_gauss(N, sigma, mu):
    k = N / (sigma * math.sqrt(2*math.pi))
    s = -1.0 / (2 * sigma * sigma)
    def f(x):
        return k * math.exp(s * (x - mu)*(x - mu))
    return f

# todo turn this into a world definition and build these two functions accordingly
def at_door(x):
    return (x >= 3 and x <= 5) or (x >= 7 and x <= 9) or (x >= 15 and x < 17) 

def all_gauss():
    gauss1 = make_gauss(1/4, 0.5, 4)
    gauss2 = make_gauss(1/4, 0.5, 8)
    gauss3 = make_gauss(1/4, 0.5, 16)
    def f(x):
        return gauss1(x) + gauss2(x) + gauss3(x) + (xmax / 0.25)
    return f

def pick_particle(particles):
    r = random.random()
    cumulW = 0
    lastX = 0
    for p in particles:
        cumulW += p.w
        #if cumulW * (p.x - lastX) >= r:
        if cumulW >= r:
            return p.clone()
        lastX = p.x

def draw_particles(turtle, particles, y):
    turtle.reset()
    turtle.ht()

    turtle.up()
    turtle.goto(0, y)
    turtle.color('black')
    turtle.down()
    turtle.goto(xmax, y)
    turtle.up()
    turtle.color('blue')

    for p in particles:
        turtle.goto(p.x, y)
        turtle.down()
        turtle.goto(p.x, y + (p.w * 10))
        turtle.up()
    
class P(object):
    def __init__(self, x, w = 1):
        self.x = int(x * 10) / 10
        self.w = w

    def __repr__(self):
        return "x = %f, w = %f" % (self.x, self.w)

    def move(self, x):
        self.x += x

    def setw(self, w):
        self.w = w
   
    def clone(self):
        return P(self.x, self.w)


#initialise particles
particles = []
for _ in range(0, numparticles):
    particles.append(P(random.uniform(0, xmax) ))

# normalise particles
for p in particles:
    p.w = p.w * (1 / len(particles))

gauss = all_gauss()

s = Screen()
t1 = RawTurtle(s)
t2 = RawTurtle(s)
t3 = RawTurtle(s)

#s.tracer(5, 250)
s.tracer(5000, 0)
s.title("Foo")
s.register_shape("fooShape", ((3,0), (0, 3), (-3, 0), (0, -3)))
s.setworldcoordinates(xmin, -1, xmax, 5)

def draw_measurements(m):
    t1.reset()
    t1.color('red', 'blue')
    t1.up()
    t1.shape("fooShape")
    t1.ht()
    t1.goto(0, 4)
    t1.down()
    t1.goto(xmax, 4)
    t1.up()
    t1.goto(0, 4)
    for i in range(xmin * 10, xmax * 10):
        if m:
            t1.goto(i / 10, gauss(i / 10) + 4)
        else:
            t1.goto(i / 10, 4)
        t1.stamp()
    t1.st()


t2.setheading(0)
t2.up()
t2.goto(1.5, 3)


#main loop

for i in range(20, 100, 5):
    pos = i/10
    print("actual pos is " + str(pos))
    print("at door is " + str(at_door(pos)))
    draw_measurements(at_door(pos)) 
    draw_particles(t3, particles, 2)
    if (at_door(pos)): 
        input("about to weight particles")
        newTotal = 0
        #this should be possible to do in a single loop
        for p in particles:
            #print(str(p.x) + ": was " + str(p.w) + " is now " + str(gauss(p.x)))
            p.setw(gauss(p.x))
            newTotal += p.w
        for p in particles:
            #print(str(p.x) + ": was " + str(p.w) + " is now " + str(p.w / newTotal))
            p.setw(p.w / newTotal)

    else:
        input("normalising particles")
        for p in particles:
            #print(str(p.x) + ": was " + str(p.w) + " is now " + str(1 / len(particles)))
            p.setw(1 / len(particles))
    totalW = 0
    for p in particles:
        totalW += p.w
    print("new total weight is " + str(totalW))
    draw_particles(t3, particles, 2)
    input("selecting particles")
    newparticles = []
    #for _ in range(0, numparticles):
    while len(newparticles) < numparticles:
        p = pick_particle(particles)
        if p != None:
            newparticles.append(p)
    particles = newparticles
    draw_particles(t3, particles, 2)
    print("normalising particles post selection to make sure it still adds up")
    newTotal = 0
    for p in particles:
        newTotal += p.w

    for p in particles:
        #print(str(p.x) + ": was " + str(p.w) + " is now " + str(p.w / newTotal))
        p.setw(p.w / newTotal)
    draw_particles(t3, particles, 2)
    totalW = 0
    for p in particles:
        totalW += p.w
    print("new total weight is " + str(totalW))
    
    input("moving particles and robot")
    t2.down()
    t2.goto(pos, 3)
    t2.up()
    for p in particles:
        p.move(noisify(0.5))
        #if we move out of the world, then regenerate it
        if (p.x) > xmax:
            p.x = random.uniform(0, xmax)

    draw_particles(t3, particles, 2)
    input("step finished, press return")
    

input("Finished, press return to exit")

#drawing the turtle star
#width(3)
#color('red', 'blue')
#begin_fill()
#circle(50, 180)
#i = 0
#for _ in range(0,36):
#    i = i + 1
#    forward(200)
#    left(170)
#    print(i)
#end_fill()
#done()

