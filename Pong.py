import pyxel
import Space
import random
'''
Things to maybe do:
- Improve the use of Space Class
- Balancement
'''


class Pong():
    def __init__(self):
        self.practice = False
        self.running = False
        self.name = "Pong"
        # Player creation
        self.player = [0, 0]
        self.ball = [0, 0]
        self.enemy = [0, 0]
        # Space creation
        self.Space = Space.Space()
        self.win = False

    def start(self, difficulty=1, practice=False):
        # Modifiers
        self.difficulty = difficulty
        self.practice = practice
        # Initial Positions
        self.enemy = [178, 60]
        self.player = [1, 60]
        self.ball = [90, 60]
        # Start running
        self.ballVelocity = [-0.9 - 0.1*difficulty, -1]
        self.playerVelocity = [0, 0]
        self.enemyVelocity = [0, 0]
        self.running = True

    def update(self):
        # Player
        x, y = self.playerVelocity
        # Player Moving Logic
        if pyxel.btn(pyxel.KEY_DOWN):  # Move Down
            if y < 2:
                y += 0.3
        if pyxel.btn(pyxel.KEY_UP):  # Move Up
            if y > -2:
                y -= 0.3
        if (not(pyxel.btn(pyxel.KEY_UP) or
                pyxel.btn(pyxel.KEY_DOWN))):  # Desaccelerating
            y *= 0.8

        # Top/Down Barrier
        if ((self.player[1] >= 110 and y > 0) or
                (self.player[1] <= 11 and y < 0)):
            y = 0
        # Set Player Velocity
        self.playerVelocity = [x, y]
        # Enemy
        x, y = self.enemyVelocity
        # Enemy Moving Logic
        if (self.ball[1] > self.enemy[1] + 7 and
                self.enemy[1] < 110):  # Move Down
            if y < 2:
                y += 0.2 * self.difficulty
        elif (self.ball[1] < self.enemy[1] - 7 and
                self.enemy[1] > 10):  # Move Up
            if y > -2:
                y -= 0.2 * self.difficulty
        # Top/Down Barrier
        else:
                y = 0
        # Set Enemy Velocity
        self.enemyVelocity = [x, y]

        # Ball
        ballParams = [self.ball, self.ballVelocity]
        ballParams[1] = self.Space.checkCollision(*ballParams, self.player)
        self.ballVelocity = self.Space.checkCollision(*ballParams, self.enemy)
        check = self.Space.checkCollision(self.ball, self.ballVelocity)
        if type(check) == bool:
            self.win = check
            self.running = False
        else:
            self.ballVelocity = check
        self.ball = self.Space.applyVel(self.ball, self.ballVelocity)
        self.player = self.Space.applyVel(self.player, self.playerVelocity)
        self.enemy = self.Space.applyVel(self.enemy, self.enemyVelocity)

    def draw(self):
        pyxel.cls(0)
        # Draw Instruction
        pyxel.text(80, 0, "Win !", pyxel.COLOR_YELLOW)
        # Draw Player
        pos = self.player[1]
        pyxel.line(1, pos + 10, 1, pos - 10, pyxel.COLOR_DARKBLUE)
        # Draw Enemy
        pos = self.enemy[1]
        pyxel.line(178, pos + 10, 178, pos - 10, pyxel.COLOR_RED)
        # Draw Ball
        pyxel.circ(*self.ball, 0, pyxel.COLOR_WHITE)
