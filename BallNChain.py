import pyxel
import pymunk
import random

class BallNChain():
    def __init__(self):
        self.practice = False
        self.running = False
        self.player = pymunk.Body(mass= 100,moment = 1000)
        self.ball = pymunk.Body(mass= 10,moment = 10)
        self.obstacle1= pymunk.Body(mass= 10,moment = 10)
        self.obstacle2= pymunk.Body(mass= 10,moment = 10)
        self.obstacle3= pymunk.Body(mass= 10,moment = 10)
        circleB = pymunk.Circle(body=self.ball,radius= 5, offset = [5,5])
        circleOb1 = pymunk.Circle(body=self.obstacle1,radius= 5)
        circleOb2 = pymunk.Circle(body=self.obstacle2,radius= 5)
        circleOb3 = pymunk.Circle(body=self.obstacle3,radius= 5)        
        self.Space = pymunk.Space()
        self.Space.add(self.ball, self.player, self.obstacle1, self.obstacle2, self.obstacle3)
        self.win = False 
    
    def start(self,difficulty = 1, practice=False):
        self.practice = practice
        # Initial Positions
        self.obstacle1.position = [-10*5, random.randint(5, 115)]
        self.obstacle2.position = [random.randint(5, 175), -10*10]
        self.obstacle3.position = [180+10*15, random.randint(5, 115)] 
        self.player.position = [25, 25]
        self.ball.position = [10, 60]
        # Initial velocities
        self.obstacle1.velocity = [0.2*difficulty, 0]
        self.obstacle2.velocity = [0, 0.2*difficulty]
        self.obstacle3.velocity = [-0.2*difficulty, 0]
        # Obstacle colors
        self.obstacle1.color = pyxel.COLOR_WHITE
        self.obstacle2.color = pyxel.COLOR_WHITE
        self.obstacle3.color = pyxel.COLOR_WHITE
        #self.ball.velocity = [0 , 100]
        self.vx, self.vy = (0, 100)
        # Start running
        self.running = True

    def update(self):
        # PLAYER
        x,y = self.player.velocity 
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
        if (not (pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_DOWN))):
            y *= 0.8
        if (not (pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_RIGHT))):
            x *= 0.8
        self.player.velocity = [x, y]
        # BALL NEED FIX
        #xb = 10
        #yb = 60
        
        k = 20
        g = 5
        dt = 1/30
        Fx = - k * (self.ball.position[0] - self.player.position[0] + 3) - g * self.vx#self.ball.velocity[0]
        Fy = - k * (self.ball.position[1] - self.player.position[0] + 4) - g * self.vy#self.ball.velocity[1]
        #ball.force = [Fx, Fy]
        ax = Fx / self.ball.mass
        ay = Fy / self.ball.mass
        #ball.velocity += [ax * dt, ay * dt]
        #vx, vy = self.ball.velocity
        self.vx += ax * dt
        self.vy += ay * dt
        self.ball.position +=[self.vx * dt, self.vy * dt]

        # Targets(Obstacles)

        # Ball/Obstacle Colision
        if (abs(self.ball.position[0] - self.obstacle1.position[0]) < 10 
            and abs(self.ball.position[1] - self.obstacle1.position[1]) < 10):
            self.obstacle1.color = pyxel.COLOR_RED
            self.obstacle1.velocity =[0, 0]
        if (abs(self.ball.position[0] - self.obstacle2.position[0]) < 10 
            and abs(self.ball.position[1] - self.obstacle2.position[1]) < 10):
            self.obstacle2.color = pyxel.COLOR_RED
            self.obstacle2.velocity =[0, 0]
        if (abs(self.ball.position[0] - self.obstacle3.position[0]) < 10 
            and abs(self.ball.position[1] - self.obstacle3.position[1]) < 10):
            self.obstacle3.color = pyxel.COLOR_RED
            self.obstacle3.velocity =[0, 0]
        # Win
        if (self.obstacle1.color == self.obstacle2.color 
            and self.obstacle1.color == self.obstacle3.color 
            and self.obstacle1.color == pyxel.COLOR_RED):
            self.win = True
            self.running = False
        # Lose
        if (self.obstacle1.position[0] > 185 
            or self.obstacle2.position[1] > 125 
            or self.obstacle3.position[0] < -5):
            self.win = False 
            self.running = False
        self.Space.step(1)

    def draw(self):
        pyxel.load("assets.pyxres")
        # Draw Instruction
        pyxel.text(75, 0, "Destroy !", pyxel.COLOR_YELLOW)
        # DRAW CHAIN
        pyxel.line(self.ball.position[0] + 5, self.ball.position[1] + 5, self.player.position[0] + 3, self.player.position[1] + 4, pyxel.COLOR_GRAY)
        # DRAW PLAYER
        pyxel.blt(self.player.position[0], self.player.position[1], 0, 5, 2, 7, 7, pyxel.COLOR_WHITE)
        # DRAW BALL
        pyxel.blt(self.ball.position[0], self.ball.position[1], 0, 19, 4, 11, 11, pyxel.COLOR_WHITE)
        # DRAW OBSTACLES
        pyxel.circ(self.obstacle1.position[0], self.obstacle1.position[1], 5, self.obstacle1.color)
        pyxel.circ(self.obstacle2.position[0], self.obstacle2.position[1], 5, self.obstacle2.color)
        pyxel.circ(self.obstacle3.position[0], self.obstacle3.position[1], 5, self.obstacle3.color)
        