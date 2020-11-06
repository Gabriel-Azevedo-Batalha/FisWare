import pyxel
import pymunk
import random

class Pong():
    def __init__(self):
        self.practice = False
        self.running = False
        self.player = pymunk.Body(mass= 100,moment = 1000)
        self.ball = pymunk.Body(mass= 10,moment = 10)
        self.enemy= pymunk.Body(mass= 100,moment = 1000)
        circle = pymunk.Circle(body=self.ball,radius= 1)
        pLine = pymunk.Segment(self.player, (0,-10), (0,10),1)
        eLine = pymunk.Segment(self.enemy, (0,-10), (0,10),1)
        # Space creation
        self.Space = pymunk.Space()
        self.Space.add(self.ball, self.player, self.enemy)
        self.win = False 
        
    
    def start(self,difficulty = 1, practice = False):
        # Modifiers
        self.difficulty = difficulty
        self.practice = practice 
        # Initial Positions
        self.enemy.position = [178, 60]
        self.player.position = [1, 60]
        self.ball.position = [90, 60]
        # Initial velocities
        self.ball.velocity = [-1, -1]
        # Start running
        self.running = True


    def update(self):
        # Player
        x,y = self.player.velocity 
        # Player Moving Logic
        if pyxel.btn(pyxel.KEY_DOWN) : # Move Down
            if y < 2:
                y += 0.3
        if pyxel.btn(pyxel.KEY_UP): # Move Up
            if y > -2:
                y -= 0.3
        if (not (pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_DOWN))): # Desaccelerating
            y *= 0.8
        
        # Top/Down Barrier
        if (self.player.position[1] >= 110 and y > 0) or (self.player.position[1] <= 11 and y < 0):
            y = 0
        # Set Player Velocity
        self.player.velocity = [x, y]
        # Enemy
        x,y = self.enemy.velocity 

        # Enemy Moving Logic
        if self.ball.position[1] > self.enemy.position[1] + 7 and self.enemy.position[1] < 110: # Move Down
            if y < 2:
                y += 0.2 * self.difficulty
        elif self.ball.position[1] < self.enemy.position[1] - 7 and self.enemy.position[1] > 10: # Move Up
            if y > -2 :
                y -= 0.2 * self.difficulty
        # Top/Down Barrier
        else:
                y = 0
        # Set Enemy Velocity
        self.enemy.velocity = [x, y]
        # Ball
        x, y = self.ball.velocity 
        # Player/Ball colision
        if (self.ball.position[0] == 1 or (self.ball.velocity[0] + self.ball.position[0]) < 1) and (self.ball.position[1] > self.player.position[1] - 10 and self.ball.position[1] <= self.player.position[1] + 10) :
            x *= -1.1 # Reflect and accelerate ball
            y += (self.ball.position[1]-self.player.position[1])/10 # Changing vertical velocity
        # Enemy/Ball colision
        elif (self.ball.position[0] == 177 or (self.ball.velocity[0] + self.ball.position[0]) > 179) and (self.ball.position[1] > self.enemy.position[1] - 10 and self.ball.position[1] <= self.enemy.position[1] + 10) :
            x *= -1.1 # Reflect and accelerate ball
            y += (self.ball.position[1]-self.enemy.position[1])/10 # Changing vertical velocity
        # Walls
        if self.ball.position[1] <= 0 or self.ball.position[1] >= 119:
            y *= -1 # Reflect ball
        # Lose
        if self.ball.position[0] < 0 :
            self.win = False 
            self.running = False
        # Win
        if self.ball.position[0] > 179:
            self.win = True
            self.running = False
        # Set Ball Velocity
        self.ball.velocity = [x, y]
        # Update
        self.Space.step(1)

    def draw(self):
        # Draw Instruction
        pyxel.text(80, 0, "Win !", pyxel.COLOR_YELLOW)
        # Draw Player
        pyxel.line(1 , self.player.position[1] + 10, 1, self.player.position[1] - 10, pyxel.COLOR_DARKBLUE)
        # Draw Enemy
        pyxel.line(178 , self.enemy.position[1] + 10, 178, self.enemy.position[1] - 10, pyxel.COLOR_RED)
        # Draw Ball
        pyxel.circ(self.ball.position[0], self.ball.position[1], 0, pyxel.COLOR_WHITE)