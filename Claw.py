import pyxel
import pymunk
from random import randint
'''
Things to maybe do:
- Add Difficulty changes
- Improve general idea
'''


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
        self.lClaw = pymunk.Body(mass=100, moment=10000)
        self.rClaw = pymunk.Body(mass=100, moment=10000)
        origin1 = (0, 0)
        origin2 = (5, 5)
        origin3 = (-5, 5)
        clawShape = [pymunk.Segment(self.rClaw, origin1, origin2, 1),
                     pymunk.Segment(self.lClaw, origin1, origin3, 1),
                     pymunk.Segment(self.rClaw, origin2, (2, 8), 1),
                     pymunk.Segment(self.lClaw, origin3, (-2, 8), 1)]
        self.Space.add(self.upClaw, self.lClaw, self.rClaw, clawShape)
        # Object Creation
        self.object = pymunk.Body(mass=1, moment=10)
        ball = pymunk.Circle(self.object, 2)
        self.Space.add(ball, self.object)
        # Objective (Temp)
        self.objective = pymunk.Body(mass=1, moment=10)
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

    def start(self, difficulty=1, practice=False, mute=False):
        # Modifiers
        self.difficulty = difficulty
        self.practice = practice
        self.mute = mute
        # Initial positions
        self.upClaw.position = (90, 60)
        self.rClaw.position = (90, 60)
        self.lClaw.position = (90, 60)
        self.object.position = (randint(5, 175), randint(10, 115))
        self.objective.position = (randint(6, 174), randint(6, 114))
        # Reset Velocity
        self.object.velocity = (0, 0)
        # Reset Timer
        self.timer = 0.0
        # Start Running
        self.running = True
        self.win = False

    def update(self):
        # Lose
        if (self.timer >= 20.0):
            self.running = False
            self.win = False
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
            if not self.mute:
                pyxel.play(0, 62)
        elif (R[0] - L[0] >= 5):
            self.motorl.rate = -0.1
            self.motorr.rate = 0.1
            if (not pyxel.btn(pyxel.KEY_SPACE) and not self.mute):
                pyxel.play(0, 61)
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
        self.timer += 1/30

    def draw(self):
        pyxel.cls(0)
        # Draw Timer
        text = "Time: " + str(round(20.0 - self.timer, 2))
        pyxel.text(135, 2, text, pyxel.COLOR_WHITE)
        # Draw Objective (Temp)
        pyxel.circ(*self.objective.position, 5, pyxel.COLOR_WHITE)
        for i in range(5):
            if (i % 2 == 0):
                pyxel.circb(*self.objective.position, i, pyxel.COLOR_RED)
        pyxel.circb(*self.objective.position, 6, pyxel.COLOR_RED)
        # Shape Drawings
        for i in self.Space.shapes:
            # Draw Segments
            if type(i) == pymunk.Segment:
                if (i.body == self.lClaw or i.body == self.rClaw):
                    color = pyxel.COLOR_YELLOW
                else:
                    color = pyxel.COLOR_RED
                x, y = i.body.local_to_world(i.a)
                x2, y2 = i.body.local_to_world(i.b)
                pyxel.line(x, y, x2, y2, color)
            # Draw Circles
            if type(i) == pymunk.Circle:
                x, y = i.body.position
                pyxel.circ(x, y, i.radius, pyxel.COLOR_GREEN)
        # Draw Rope
        x = self.upClaw.position[0]
        pyxel.line(x, 1, *self.upClaw.position, pyxel.COLOR_GRAY)
        pyxel.line(x - 5, 1, self.upClaw.position[0] + 5, 1, 1)
        pyxel.line(x - 3, 2, self.upClaw.position[0] + 3, 2, 1)
