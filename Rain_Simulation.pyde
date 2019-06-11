"""
  * Rain Simulation with Puddle and Splashes
  * by Mirza MY Humayung
  *
  *
  * MIT License
  */
"""
class Spring:
    vx = 0.0
    vy = 0.0
    target_x = 0.0
    target_y = 0.0

    def __init__(self, xpos, ypos, gravity, mass, damping, spring_constant):
        self.x = xpos
        self.y = ypos
        self.gravity = gravity
        self.mass = mass
        self.spring_constant = spring_constant
        self.damping = damping

    def update(self, target_x, target_y):
        self.target_x = target_x
        self.target_y = target_y

        forceX = (target_x - self.x) * self.spring_constant
        ax = forceX / self.mass
        self.vx = self.damping * (self.vx + ax)
        self.x += self.vx

        forceY = (target_y - self.y) * self.spring_constant
        forceY += self.gravity
        ay = forceY / self.mass
        self.vy = self.damping * (self.vy + ay)
        self.y += self.vy

        if (abs(self.vy) < 0.01):
            self.vy = 0.0
        if (abs(self.vx) < 0.01):
            self.vx = 0.0

class WaterSurface:

    def __init__(self, y, segment, gravity, mass, damping, viscosity):
        self.posy = y
        self.segment = segment
        self.spacing = width / self.segment
        self.gravity = gravity
        self.springs = []
        self.damping = damping
        self.viscosity = viscosity
        self.mass = mass
        self.y = y
        for i in range(segment):
            self.springs.append(
                Spring(i * width / self.segment, y, gravity, mass, damping, viscosity))

    def run(self):
        springs = self.springs
        strokeWeight(0.2)
        fill(255)
        beginShape()
        vertex(0, height)
        for i in range(len(self.springs)):
            if (i == 0):
                springs[0].update(springs[0].x, springs[1].y)
                springs[0].update(springs[0].x, self.posy)
            elif (i == len(springs) - 1):
                springs[len(springs) - 1].update(
                    springs[len(springs) - 1].x, springs[len(springs) - 2].y)
                springs[
                    len(springs) - 1].update(springs[len(springs) - 1].x, self.posy)
            else:
                springs[i].update(
                    springs[i - 1].x, springs[i - 1].y)
                springs[i].update(
                    springs[i + 1].x, springs[i + 1].y)
                springs[i].update(springs[i].x, self.posy)
            curveVertex(springs[i].x, springs[i].y)
        vertex(width, height)
        endShape()
        springs[self.segment - 1].x = width + 50
        springs[0].x = -50

    def currentSegment(self, pos, vel):
        for i in range(self.segment):
            if (pos.x > self.springs[i].x) and (pos.x < self.springs[i].x + self.spacing) and (pos.y + vel > self.springs[i].y):
                return True
        return False

    def drop(self, x, force):
        for i in range(self.segment):
            if (x > self.springs[i].x and x < self.springs[i].x + self.spacing):
                self.springs[i].vy += force

class Droplet:

    def __init__(self, x, y, z, distance):
        self.pos = PVector(x, y, z)
        self.vel = PVector(0, 1)
        self.vel.mult(8 / distance)
        self.off = False
        self.size = 2 / distance
        self.length = 6 / distance

    def show(self):
        stroke(255)
        strokeWeight(self.size + random(0.5))
        line(self.pos.x, self.pos.y, self.pos.x, self.pos.y + self.length)

    def update(self):
        self.vel.add(gravity)
        self.pos.add(self.vel)
        if(ws.currentSegment(self.pos, self.vel.y)):
            ps.init(self.pos.x, self.pos.y + 20, self.pos.z,
                    self.size * 10, self.size, self.vel.mag())
            force = 0.5 * self.size * self.vel.magSq()
            ws.drop(self.pos.x, force*0.0018)
            self.off = True

class Particle:

    def __init__(self, x, y, z, splatterP, size):
        self.pos = PVector(x, y)
        self.angle = random(-PI + 0.1, -0.1)
        self.size = random(0, size * 2)
        self.vel = PVector.random2D()

        self.vel.mult(sqrt(splatterP))
        self.vel.mult(random(1))
        self.off = False

    def update(self):
        if (self.pos.y > height - 50):
            self.off = True
        else:
            self.vel.add(gravity)
            self.pos.add(self.vel)

    def show(self):
        noStroke()
        ellipse(self.pos.x, self.pos.y, random(self.size / 2) +
                self.size, random(self.size / 2) + self.size)

class ParticleSystem:
    sparks = []

    def run(self):
        for i in range(len(self.sparks) - 1, 0, -1):
            s = self.sparks[i]
            if (s.off):
                self.sparks.pop(i)
            else:
                s.update()
                s.show()

    def init(self, x, y, z, amount, size, splatterP):
        for i in range(floor(amount)):
            self.sparks.append(Particle(x, y, z, splatterP, size))

class RainSystem:

    def __init__(self, f):
        self.f = f
        self.droplets = []

    def run(self):
        for i in range(self.f):
            self.droplets.append(Droplet(random(width), random(-100, -1000),
                                         random(500), random(random(0.5, 3),
                                                             random(11))))
        for i in range(len(self.droplets) - 1, 0, -1):
            d = self.droplets[i]
            if (d.off):
                self.droplets.pop(i)
            else:
                d.update()
                d.show()


def setup():
    fullScreen()
    noStroke()
    global ws
    global ps
    global rs
    global gravity
    gravity = PVector(0, 0.25)
    rs = RainSystem(8)
    ps = ParticleSystem()
    ws = WaterSurface(height - 100, 200, 5, 50, 0.99, 0.5)

def draw():
    background(0)
    ws.run()
    rs.run()
    ps.run()
