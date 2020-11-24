import pyxel
import pymunk
import random
import Space
'''
Things to maybe do:
- Improve ball movement
'''


class BallNChain():
    def __init__(self):
        # Initial Minigame Properties
        self.practice = False
        self.running = False
        self.name = "BallNChain"
        self.win = False
        # Space init
        self.Space = pymunk.Space()
        self.Space.damping = 0.96
        # Collision Types
        self.collisionTypes = {"ball": 1, "target": 2,
                               "player": 3, "wall": 4}
        # Player Init
        self.player = pymunk.Body(mass=10000, moment=float("inf"))
        vertices = [(0, 0), (0, 7), (7, 7), (7, 0)]
        playerShape = pymunk.Poly(self.player, vertices)
        playerShape.collision_type = self.collisionTypes["player"]
        # Target Init
        self.targets, targetShape = [[], []]
        for i in range(3):
            self.targets.append(pymunk.Body(mass=50, moment=10,
                                            body_type=pymunk.Body.KINEMATIC))
            targetShape.append(pymunk.Circle(body=self.targets[i], radius=5))
            targetShape[i].collision_type = self.collisionTypes["target"]
        # Ball Init
        self.ball = pymunk.Body(mass=5, moment=float("inf"))
        ballShape = pymunk.Circle(body=self.ball, radius=5, offset=[5, 5])
        ballShape.collision_type = self.collisionTypes["ball"]
        ballShape.elasticity = 0.8
        # Chain Init
        chain = pymunk.SlideJoint(self.ball, self.player,
                                  (0, 0), (0, 0), 0, 50)
        # Walls Init
        origin1 = (-1, -1)
        origin2 = (182, 122)
        walls = [pymunk.Segment(self.Space.static_body, origin1, (-1, 121), 2),
                 pymunk.Segment(self.Space.static_body, origin1, (181, -1), 2),
                 pymunk.Segment(self.Space.static_body, origin2, (182, -1), 2),
                 pymunk.Segment(self.Space.static_body, origin2, (-1, 122), 2)]
        for i in range(4):
            walls[i].elasticity = 0.8
            walls[i].collision_type = self.collisionTypes["wall"]
        # Space Add
        self.Space.add(self.ball, self.player, *self.targets,
                       playerShape, ballShape, *targetShape, walls,
                       chain)
        # Ball Target CollisionHandler
        BallTarget = self.Space.add_collision_handler(
            self.collisionTypes["ball"],
            self.collisionTypes["target"])
        BallTarget.begin = Space.BallTarget
        # Wall Target CollisionHandler
        WallTarget = self.Space.add_collision_handler(
            self.collisionTypes["wall"],
            self.collisionTypes["target"])
        WallTarget.begin = Space.WallTarget
        # Player Target CollisionHandler
        PlayerTarget = self.Space.add_collision_handler(
            self.collisionTypes["player"],
            self.collisionTypes["target"])
        PlayerTarget.begin = Space.PlayerTarget
        # Player Ball CollisionHandler
        PlayerTarget = self.Space.add_collision_handler(
            self.collisionTypes["player"],
            self.collisionTypes["ball"])
        PlayerTarget.begin = Space.PlayerBall

    def start(self, difficulty=1, practice=False):
        # Modifiers
        self.practice = practice
        # Initial Positions
        self.targets[0].position = (-10*5, random.randint(5, 115))
        self.targets[1].position = (random.randint(5, 175), -10*10)
        self.targets[2].position = (180+10*15, random.randint(5, 115))
        self.player.position = [50, 50]
        self.ball.position = [50, 60]
        # Initial velocities
        self.targets[0].velocity = (0.2*difficulty, 0)
        self.targets[1].velocity = (0, 0.2*difficulty)
        self.targets[2].velocity = (-0.2*difficulty, 0)
        self.ball.velocity = (0, 0)
        self.player.velocity = (0, 0)
        # Obstacle colors
        self.targets[0].color = pyxel.COLOR_WHITE
        self.targets[1].color = pyxel.COLOR_WHITE
        self.targets[2].color = pyxel.COLOR_WHITE
        self.vx, self.vy = (0, 100)
        # Start running
        self.running = True

    def update(self):
        # Player
        x, y = self.player.velocity
        if pyxel.btn(pyxel.KEY_LEFT):
            if x > -2:
                x -= 0.5
        if pyxel.btn(pyxel.KEY_RIGHT):
            if x < 2:
                x += 0.5
        if pyxel.btn(pyxel.KEY_DOWN):
            if y < 2:
                y += 0.5
        if pyxel.btn(pyxel.KEY_UP):
            if y > -2:
                y -= 0.5

        self.player.velocity = [x, y]

        # Win
        if (self.targets[0].color == self.targets[1].color
                and self.targets[0].color == self.targets[2].color
                and self.targets[0].color == pyxel.COLOR_BLACK):
            self.win = True
            self.running = False
        # Lose
        if (self.targets[0].position[0] > 185
                or self.targets[1].position[1] > 125
                or self.targets[2].position[0] < -5
                or self.player.position[0] < 0):
            self.win = False
            self.running = False
        # Step
        self.Space.step(0.5)
        self.Space.step(0.5)

    def draw(self):
        pyxel.load("assets.pyxres")
        pyxel.cls(0)
        # Draw Targets
        pyxel.circ(*self.targets[0].position, 5, self.targets[0].color)
        pyxel.circ(*self.targets[1].position, 5, self.targets[1].color)
        pyxel.circ(*self.targets[2].position, 5, self.targets[2].color)
        # Draw Instruction
        pyxel.text(75, 0, "Destroy !", pyxel.COLOR_YELLOW)
        # Draw Chain
        ballCx, ballCy = self.ball.position+[5, 5]
        playerC = self.player.position+[3, 4]
        pyxel.line(ballCx, ballCy, *playerC, pyxel.COLOR_GRAY)
        # Draw Player
        pyxel.blt(*self.player.position, 0, 5, 2, 7, 7, pyxel.COLOR_WHITE)
        # Draw Ball
        pyxel.blt(*self.ball.position, 0, 19, 4, 11, 11, pyxel.COLOR_WHITE)
