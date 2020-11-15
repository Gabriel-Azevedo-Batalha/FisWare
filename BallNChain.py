import pyxel
import pymunk
import random
import Space


class BallNChain():
    def __init__(self):
        # Initial Minigame Properties
        self.practice = False
        self.running = False
        self.win = False
        # Space init
        self.Space = pymunk.Space()
        # Collision Types
        self.collisionTypes = {"ball": 1, "target": 2,
                               "player": 3, "wall": 4}
        # Player Init
        self.player = pymunk.Body(mass=100, moment=float("inf"))
        playerShape = pymunk.Poly(self.player, [(0, 0), (0, 7), (7, 7), (7, 0)])
        playerShape.collision_type = self.collisionTypes["player"]
        # Target Init
        self.targets, targetShape = [[], []]
        for i in range(3):
            self.targets.append(pymunk.Body(mass=10, moment=10,
                                            body_type=pymunk.Body.KINEMATIC))
            targetShape.append(pymunk.Circle(body=self.targets[i], radius=5))
            targetShape[i].collision_type = self.collisionTypes["target"]
        # Ball Init
        self.ball = pymunk.Body(mass=500, moment=10)
        ballShape = pymunk.Circle(body=self.ball, radius=5, offset=[5, 5])
        ballShape.collision_type = self.collisionTypes["ball"]
        # Walls Init
        walls = [pymunk.Segment(self.Space.static_body, (-1, -1), (-1, 121), 2)
                ,pymunk.Segment(self.Space.static_body, (-1, -1), (181, -1), 2)
                ,pymunk.Segment(self.Space.static_body, (182, 122), (182, -1), 2)
                ,pymunk.Segment(self.Space.static_body, (182, 122), (-1, 122), 2)]
        for i in range(4):
            walls[i].collision_type = self.collisionTypes["wall"]
        # Space Add
        self.Space.add(self.ball, self.player, *self.targets,
                       playerShape, ballShape, *targetShape, walls)
        # Ball Target CollisionHandler
        BallTarget = self.Space.add_collision_handler(
            self.collisionTypes["ball"],
            self.collisionTypes["target"])
        BallTarget.begin = Space.BallTarget
        # Player Target CollisionHandler
        PlayerTarget = self.Space.add_collision_handler(
            self.collisionTypes["player"],
            self.collisionTypes["target"])
        PlayerTarget.begin = Space.PlayerTarget

    def start(self, difficulty=1, practice=False):
        self.practice = practice
        # Initial Positions
        self.targets[0].position = [-10*5, random.randint(5, 115)]
        self.targets[1].position = [random.randint(5, 175), -10*10]
        self.targets[2].position = [180+10*15, random.randint(5, 115)]
        self.player.position = [25, 25]
        self.playerC = self.player.position + [3, 4]
        self.ball.position = [10, 60]
        # Initial velocities
        self.targets[0].velocity = [0.2*difficulty, 0]
        self.targets[1].velocity = [0, 0.2*difficulty]
        self.targets[2].velocity = [-0.2*difficulty, 0]
        # Obstacle colors
        self.targets[0].color = pyxel.COLOR_WHITE
        self.targets[1].color = pyxel.COLOR_WHITE
        self.targets[2].color = pyxel.COLOR_WHITE
        # self.ball.velocity = [0 , 100]
        self.vx, self.vy = (0, 100)
        # Start running
        self.running = True

    def update(self):
        
        # PLAYER
        x, y = self.player.velocity
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
        # xb = 10
        # yb = 60

        k = 300
        g = 5
        dt = 1/30
        self.playerC = self.player.position + [3, 4]
        Fx, Fy = -k*(self.ball.position-self.playerC)-g*[self.vx, self.vy]
        #self.ball.apply_force_at_local_point((Fx, Fy), self.ball.position)
        
        ax = Fx / self.ball.mass
        ay = Fy / self.ball.mass
        # ball.velocity += [ax * dt, ay * dt]
        # vx, vy = self.ball.velocity
        self.vx += ax * dt
        self.vy += ay * dt
        self.ball.position += [self.vx * dt, self.vy * dt]

        # Win
        if (self.targets[0].color == self.targets[1].color
                and self.targets[0].color == self.targets[2].color
                and self.targets[0].color == pyxel.COLOR_BLACK):
            self.win = True
            self.running = False
        # Lose
        if (self.targets[0].position[0] > 185
                or self.targets[1].position[1] > 125
                or self.targets[2].position[0] < -5):
            self.win = False
            self.running = False
        self.Space.step(1)

    def draw(self):
        pyxel.load("assets.pyxres")
        # DRAW OBSTACLES
        pyxel.circ(*self.targets[0].position, 5, self.targets[0].color)
        pyxel.circ(*self.targets[1].position, 5, self.targets[1].color)
        pyxel.circ(*self.targets[2].position, 5, self.targets[2].color)
        # Draw Instruction
        pyxel.text(75, 0, "Destroy !", pyxel.COLOR_YELLOW)
        # DRAW CHAIN
        ballCx, ballCy = self.ball.position+[5, 5]
        playerC = self.player.position+[3, 4]
        pyxel.line(ballCx, ballCy, *playerC, pyxel.COLOR_GRAY)
        # DRAW PLAYER
        pyxel.blt(*self.player.position, 0, 5, 2, 7, 7, pyxel.COLOR_WHITE)
        # DRAW BALL
        pyxel.blt(*self.ball.position, 0, 19, 4, 11, 11, pyxel.COLOR_WHITE)
        
