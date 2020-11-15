import pyxel
import pymunk
from random import randint

class Dodge():
    def __init__(self):
        self.practice = False
        self.running = False
        self.player = pymunk.Body(mass= 100,moment = float("inf"))
        playerShape = pymunk.Poly(self.player, [(0, 0), (0, 7), (7, 7), (7, 0)])
        self.lasers = []
        self.Space = pymunk.Space()
        
        self.win = False 
        walls = [pymunk.Segment(self.Space.static_body, (-1, -1), (-1, 121), 2)
                ,pymunk.Segment(self.Space.static_body, (-1, -1), (181, -1), 2)
                ,pymunk.Segment(self.Space.static_body, (182, 122), (182, -1), 2)
                ,pymunk.Segment(self.Space.static_body, (182, 122), (-1, 122), 2)] 
        self.Space.add(self.player, walls, playerShape)
    
    def start(self,difficulty = 1, practice = False):
        self.practice = practice
        # Laser creation
        self.lasers = []
        for i in range(difficulty + 2):
            info = {}
            info["body"] = pymunk.Body(mass= 1,moment = 1)
            
            r = randint (1, 4)
            info["direction"] = r
            if r == 1:
                info["body"].position = [-2940, randint(5, 113)]
                info["body"].velocity = [50, 0]
                danger = [2, info["body"].position[1] - 5]
                
            elif r == 2:
                info["body"].position = [randint(5, 175), -3000]
                info["body"].velocity = [0, 50]
                danger = [info["body"].position[0] -5, 1]
            elif r == 3:
                info["body"].position = [randint(5, 175), 3120]
                info["body"].velocity = [0, -50]
                danger = [info["body"].position[0] -5, 109]
            elif r == 4:
                info["body"].position = [3120, randint(5, 113)]
                info["body"].velocity = [-50, 0]
                danger = [168, info["body"].position[1] - 5] 
            info["danger"] = danger
            self.lasers.append(info)
            self.Space.add(self.lasers[i]["body"])
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
        
        # Win
        if (self.time >= 5.0):
            self.win = True
            self.running = False
        # Lose
        
        for laser in self.lasers:
            
            if ((laser["direction"] == 1 and self.player.position[1] - 1 <= laser["body"].position[1] and
                self.player.position[1] + 8 >= laser["body"].position[1] and
                self.player.position[0] - 1 <= laser["body"].position[0]) or
                (laser["direction"] == 2 and self.player.position[0] - 1 <= laser["body"].position[0] and
                self.player.position[0] + 8 >= laser["body"].position[0] and
                self.player.position[1] -1  <= laser["body"].position[1]) or
                (laser["direction"] == 3 and self.player.position[0] - 1 <= laser["body"].position[0] and
                self.player.position[0] + 8 >= laser["body"].position[0] and
                self.player.position[1] + 8 >= laser["body"].position[1]) or
                (laser["direction"] == 4 and self.player.position[1] - 1 <= laser["body"].position[1] and
                self.player.position[1] + 8 >= laser["body"].position[1] and
                self.player.position[0] + 8 >= laser["body"].position[0])):
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
            if laser["direction"] == 1:
                pyxel.line(-1, laser["body"].position[1], laser["body"].position[0], laser["body"].position[1], pyxel.COLOR_RED)
                pyxel.line(-1, laser["body"].position[1]-1, laser["body"].position[0], laser["body"].position[1]-1, pyxel.COLOR_RED)
                pyxel.line(-1, laser["body"].position[1]+1, laser["body"].position[0], laser["body"].position[1]+1, pyxel.COLOR_RED)
            elif laser["direction"] == 2:
                pyxel.line(laser["body"].position[0]-1, -1, laser["body"].position[0]-1, laser["body"].position[1], pyxel.COLOR_RED)
                pyxel.line(laser["body"].position[0], -1, laser["body"].position[0], laser["body"].position[1], pyxel.COLOR_RED)
                pyxel.line(laser["body"].position[0]+1, -1, laser["body"].position[0]+1, laser["body"].position[1], pyxel.COLOR_RED)
            elif laser["direction"] == 3:
                pyxel.line(laser["body"].position[0]-1, 121, laser["body"].position[0]-1, laser["body"].position[1], pyxel.COLOR_RED)
                pyxel.line(laser["body"].position[0], 121, laser["body"].position[0], laser["body"].position[1], pyxel.COLOR_RED)
                pyxel.line(laser["body"].position[0]+1, 121, laser["body"].position[0]+1, laser["body"].position[1], pyxel.COLOR_RED)
            elif laser["direction"] == 4:
                pyxel.line(181, laser["body"].position[1]-1, laser["body"].position[0], laser["body"].position[1]-1, pyxel.COLOR_RED)
                pyxel.line(181, laser["body"].position[1], laser["body"].position[0], laser["body"].position[1], pyxel.COLOR_RED)
                pyxel.line(181, laser["body"].position[1]+1, laser["body"].position[0], laser["body"].position[1]+1, pyxel.COLOR_RED)
            # Danger
            if ((laser["body"].position[0] < 0 and laser["direction"] == 1)
                or (laser["body"].position[0] > 180 and laser["direction"] == 4)
                or (laser["body"].position[1] < 0 and laser["direction"] == 2)
                or (laser["body"].position[1] > 120 and laser["direction"] == 3)):
                pyxel.blt(laser["danger"][0], laser["danger"][1], 0, 33, 0, 11, 10, pyxel.COLOR_WHITE)
