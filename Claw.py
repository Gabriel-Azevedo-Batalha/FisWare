import pyxel
import pymunk


class Claw():
    def __init__(self):
        # Initial Minigame Properties
        self.running = False
        self.practice = False
        self.win = False
        self.name = "Claw"
        # Space Creation
        self.Space = pymunk.Space()
        # Claw Creation
        self.upClaw = pymunk.Body(mass=200, moment=float("inf"))
        self.lClaw = pymunk.Body(mass=100, moment=1)
        self.rClaw = pymunk.Body(mass=100, moment=1)
        origin1 = (0, 0)
        origin2 = (5, 5)
        origin3 = (-5, 5)
        clawShape = [pymunk.Segment(self.rClaw, origin1, origin2, 1),
                     pymunk.Segment(self.lClaw, origin1, origin3, 1),
                     pymunk.Segment(self.rClaw, origin2, (2, 8), 1),
                     pymunk.Segment(self.lClaw, origin3, (-2, 8), 1)]
        self.Space.add(self.upClaw, self.lClaw, self.rClaw, clawShape)
        # Rope creation
        ropev = pymunk.Body(mass=100, moment=float("inf"))
        ropeh = pymunk.Body(mass=100, moment=float("inf"))
        vrope = pymunk.Segment(ropev, (0, 0), (0, 30), 1)
        hrope = pymunk.Segment(ropeh, (-90, -30), (90, -30), 1)
        # self.Space.add(vrope, hrope, ropeh, ropev)

        # Object Creation
        self.object = pymunk.Body(mass=1, moment=10)
        ball = pymunk.Circle(self.object, 2)
        self.Space.add(ball, self.object)
        # Objective (Temp)
        self.objective = pymunk.Body(mass=1, moment=10)
        self.objective.position = (20, 20)
        self.Space.add(self.objective)
        # Left Claw Pivot
        pivot = pymunk.PivotJoint(self.upClaw, self.lClaw, (0, 0), (0, 0))
        pivot.collide_bodies = False
        self.Space.add(pivot)
        # R Claw Pivot
        pivot = pymunk.PivotJoint(self.upClaw, self.rClaw, (0, 0), (0, 0))
        pivot.collide_bodies = False
        self.Space.add(pivot)
        # Bi Pivot
        pivot = pymunk.RotaryLimitJoint(self.lClaw, self.rClaw, 0.5, 1)
        pivot.collide_bodies = False
        self.Space.add(pivot)

        # V Rope
        pivot = pymunk.PivotJoint(self.upClaw, ropev, (0, 0), (0, 30))
        pivot.collide_bodies = False
        # self.Space.add(pivot)
        # H Rope
        pivot = pymunk.PivotJoint(ropeh, ropev, (0, 0), (0, 30))
        pivot.collide_bodies = False
        # self.Space.add(pivot)

        # Motors
        self.motorl = pymunk.SimpleMotor(self.lClaw, self.upClaw, 0)
        self.motorr = pymunk.SimpleMotor(self.rClaw, self.upClaw, 0)
        self.Space.add(self.motorl, self.motorr)
        # Walls
        origin4 = (179, 119)
        walls = [pymunk.Segment(self.Space.static_body, (-1, 0), (-1, 121), 1),
                 pymunk.Segment(self.Space.static_body, (-1, 0), (181, 0), 1),
                 pymunk.Segment(self.Space.static_body, origin4, (179, -1), 1),
                 pymunk.Segment(self.Space.static_body, origin4, (-1, 119), 1)]
        self.Space.add(walls)

    def start(self, difficulty=1, practice=False):
        # Modifiers
        self.difficulty = difficulty
        self.practice = practice
        # Initial positions
        self.upClaw.position = (90, 60)
        self.rClaw.position = (90, 60)
        self.lClaw.position = (90, 60)
        self.object.position = (40, 80)
        # Start Running
        self.running = True
        self.win = False

    def update(self):
        # Claw
        x, y = self.upClaw.velocity
        L = self.lClaw.local_to_world((-2, 8))
        R = self.rClaw.local_to_world((2, 8))
        if pyxel.btn(pyxel.KEY_LEFT):
            if x > -2:
                x -= 0.2
        if pyxel.btn(pyxel.KEY_RIGHT):
            if x < 2:
                x += 0.2
        if pyxel.btn(pyxel.KEY_DOWN):
            if y < 2:
                y += 0.2
        if pyxel.btn(pyxel.KEY_UP):
            if y > -2:
                y -= 0.2
        if (pyxel.btn(pyxel.KEY_SPACE) and L[1] > self.upClaw.position[1]):
            self.motorl.rate = 0.1
            self.motorr.rate = -0.1
        elif (R[0] - L[0] >= 5):
            self.motorl.rate = -0.1
            self.motorr.rate = 0.1
        else:
            self.motorl.rate = 0.0
            self.motorr.rate = 0.0
        if (not (pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_DOWN))):
            y *= 0.8
        if (not (pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_RIGHT))):
            x *= 0.8
        self.upClaw.velocity = [x, y]

        if ((self.objective.position[0] >= self.object.position[0]-5
             and self.objective.position[0] <= self.object.position[0]+5) and
            (self.objective.position[1] >= self.object.position[1]-5
             and self.objective.position[1] <= self.object.position[1]+5)):
            self.running = False
            self.win = True
        self.Space.step(0.5)
        self.Space.step(0.5)

    def draw(self):
        pyxel.cls(0)
        # Draw Objective (Temp)
        pyxel.circ(20, 20, 5, pyxel.COLOR_RED)
        for i in self.Space.shapes:
            # Draw Segments
            if type(i) == pymunk.Segment:
                if (i.body == self.lClaw or i.body == self.rClaw):
                    color = pyxel.COLOR_YELLOW
                else:
                    color = pyxel.COLOR_GRAY
                x, y = i.body.local_to_world(i.a)
                x2, y2 = i.body.local_to_world(i.b)
                pyxel.line(x, y, x2, y2, color)
            # Draw Circles
            if type(i) == pymunk.Circle:
                x, y = i.body.position
                pyxel.circ(x, y, i.radius, pyxel.COLOR_GREEN)