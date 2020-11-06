import pyxel

class Menu():
    def __init__(self):
        self.running = True
        self.start = [70,60]
        self.title = [65,30]
        self.option = "menu"
        self.practice = 0

    def draw(self):
        if self.option == "menu":
            pyxel.text(self.start[0], self.start[1], "[S]tart", pyxel.COLOR_RED)
            pyxel.text(self.start[0], self.start[1] + 10, "[P]ractice", pyxel.COLOR_RED)
            pyxel.blt( self.title[0], self.title[1], 1, 0, 0, 50, 9, pyxel.COLOR_BLACK)
        elif self.option == "practice":
            pyxel.text(self.start[0], self.start[1] , "[1] Pong", pyxel.COLOR_RED)
            pyxel.text(self.start[0], self.start[1] + 10, "[2] BallNChain", pyxel.COLOR_RED)
            pyxel.text(self.start[0], self.start[1] + 20, "[3] Dodge", pyxel.COLOR_RED)
            pyxel.text(self.start[0], self.start[1] + 30, "[B]ack", pyxel.COLOR_RED)
            pyxel.blt (self.title[0], self.title[1], 1, 0, 0, 50, 9, pyxel.COLOR_BLACK)
    
    def update(self):
        if self.option == "menu":
            if pyxel.btn(pyxel.KEY_S):
                self.running = False
            elif pyxel.btn(pyxel.KEY_P):
                self.option = "practice"
        elif self.option == "practice":
            if pyxel.btn(pyxel.KEY_B):
                self.option = "menu"
            elif pyxel.btn(pyxel.KEY_1):
                self.practice = 1
                self.option = "menu"
                self.running = False
            elif pyxel.btn(pyxel.KEY_2):
                self.practice = 2
                self.option = "menu"
                self.running = False
            elif pyxel.btn(pyxel.KEY_3):
                self.practice = 3
                self.option = "menu"
                self.running = False