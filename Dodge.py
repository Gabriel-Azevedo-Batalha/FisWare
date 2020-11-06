import pyxel
import pymunk
from random import randint

class Dodge():
    def __init__(self):
        self.practice = False
        self.running = False
        self.player = pymunk.Body(mass= 100,moment = 1000)
        self.lasers = []
        self.Space = pymunk.Space()
        self.Space.add(self.player)
        self.win = False 
    
    def start(self,difficulty = 1, practice = False):
        self.practice = practice
        # Laser creation
        self.lasers = []
        for laser in range(difficulty + 2):
            self.lasers.append([pymunk.Body(mass= 1,moment = 1)])
            r = randint (1, 4)
            self.lasers[laser].append(r)
            if r == 1:
                self.lasers[laser][0].position = [-5000, randint(5, 113)]
                self.lasers[laser][0].velocity = [50, 0]
                danger = [2, self.lasers[laser][0].position[1] - 5]
            elif r == 2:
                self.lasers[laser][0].position = [randint(5, 175), -5000]
                self.lasers[laser][0].velocity = [0, 50]
                danger = [self.lasers[laser][0].position[0] -5, 1]
            elif r == 3:
                self.lasers[laser][0].position = [randint(5, 175), 6200]
                self.lasers[laser][0].velocity = [0, -50]
                danger = [self.lasers[laser][0].position[0] -5, 109]
            elif r == 4:
                self.lasers[laser][0].position = [ 6800, randint(5, 113)]
                self.lasers[laser][0].velocity = [-50, 0]
                danger = [168, self.lasers[laser][0].position[1] - 5] 
            self.lasers[laser].append(danger)
            self.Space.add(self.lasers[laser][0])
        # Initial Positions
        self.player.position = [90, 60]
        # Start running
        self.running = True
        self.dt = 1/30
        self.time = 0.0

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

        # Targets(Obstacles)
        
        # Win
        if (self.time >= 6.0):
            self.win = True
            self.running = False
        # Lose
        
        for laser in self.lasers:
            
            if ((laser[1] == 1 and self.player.position[1] - 1 <= laser[0].position[1] and
                self.player.position[1] + 8 >= laser[0].position[1] and
                self.player.position[0] - 1 <= laser[0].position[0]) or
                (laser[1] == 2 and self.player.position[0] - 1 <= laser[0].position[0] and
                self.player.position[0] + 8 >= laser[0].position[0] and
                self.player.position[1] -1  <= laser[0].position[1]) or
                (laser[1] == 3 and self.player.position[0] - 1 <= laser[0].position[0] and
                self.player.position[0] + 8 >= laser[0].position[0] and
                self.player.position[1] + 8 >= laser[0].position[1]) or
                (laser[1] == 4 and self.player.position[1] - 1 <= laser[0].position[1] and
                self.player.position[1] + 8 >= laser[0].position[1] and
                self.player.position[0] + 8 >= laser[0].position[0])):
                self.win = False 
                self.running = False
        self.time += self.dt
        self.Space.step(1)

    def draw(self):
        pyxel.load("assets.pyxres")
        # Draw Instruction
        pyxel.text(80, 0, "Dodge !", pyxel.COLOR_YELLOW)
        # DRAW Player
        pyxel.blt(self.player.position[0], self.player.position[1], 0, 5, 2, 7, 7, pyxel.COLOR_WHITE)
        # DRAW Lasers
        for laser in self.lasers:
            # Laser
            if laser[1] == 1:
                pyxel.line(-1, laser[0].position[1], laser[0].position[0], laser[0].position[1], pyxel.COLOR_RED)
                pyxel.line(-1, laser[0].position[1]-1, laser[0].position[0], laser[0].position[1]-1, pyxel.COLOR_RED)
                pyxel.line(-1, laser[0].position[1]+1, laser[0].position[0], laser[0].position[1]+1, pyxel.COLOR_RED)
            elif laser[1] == 2:
                pyxel.line(laser[0].position[0]-1, -1, laser[0].position[0]-1, laser[0].position[1], pyxel.COLOR_RED)
                pyxel.line(laser[0].position[0], -1, laser[0].position[0], laser[0].position[1], pyxel.COLOR_RED)
                pyxel.line(laser[0].position[0]+1, -1, laser[0].position[0]+1, laser[0].position[1], pyxel.COLOR_RED)
            elif laser[1] == 3:
                pyxel.line(laser[0].position[0]-1, 121, laser[0].position[0]-1, laser[0].position[1], pyxel.COLOR_RED)
                pyxel.line(laser[0].position[0], 121, laser[0].position[0], laser[0].position[1], pyxel.COLOR_RED)
                pyxel.line(laser[0].position[0]+1, 121, laser[0].position[0]+1, laser[0].position[1], pyxel.COLOR_RED)
            elif laser[1] == 4:
                pyxel.line(181, laser[0].position[1]-1, laser[0].position[0], laser[0].position[1]-1, pyxel.COLOR_RED)
                pyxel.line(181, laser[0].position[1], laser[0].position[0], laser[0].position[1], pyxel.COLOR_RED)
                pyxel.line(181, laser[0].position[1]+1, laser[0].position[0], laser[0].position[1]+1, pyxel.COLOR_RED)
            # Danger
            if ((laser[0].position[0] < 0 and laser[1] == 1)
                or (laser[0].position[0] > 180 and laser[1] == 4)
                or (laser[0].position[1] < 0 and laser[1] == 2)
                or (laser[0].position[1] > 120 and laser[1] == 3)):
                pyxel.blt(laser[2][0], laser[2][1], 0, 33, 0, 11, 10, pyxel.COLOR_WHITE)
        