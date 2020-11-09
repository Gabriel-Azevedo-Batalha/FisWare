import pyxel

class Menu():
    def __init__(self):
        self.running = True
        self.start = [60,60]
        self.title = [65,30]
        self.option = "menu"
        self.practice = 0
        self.difficulty = 1

    def draw(self):
        if self.option == "menu":
            pyxel.text(self.start[0], self.start[1], "-[S]tart", pyxel.COLOR_RED)
            pyxel.text(self.start[0], self.start[1] + 10, "-[P]ractice", pyxel.COLOR_RED)
            pyxel.text(self.start[0], self.start[1] + 20, "-[O]ptions", pyxel.COLOR_RED)
            pyxel.blt( self.title[0], self.title[1], 1, 0, 0, 50, 9, pyxel.COLOR_BLACK)
        elif self.option == "practice":
            pyxel.text(self.start[0], self.start[1] , "-[1] Pong", pyxel.COLOR_RED)
            pyxel.text(self.start[0], self.start[1] + 10, "-[2] BallNChain", pyxel.COLOR_RED)
            pyxel.text(self.start[0], self.start[1] + 20, "-[3] Dodge", pyxel.COLOR_RED)
            pyxel.text(self.start[0], self.start[1] + 30, "-[B]ack", pyxel.COLOR_RED)
            pyxel.blt (self.title[0], self.title[1], 1, 0, 0, 50, 9, pyxel.COLOR_BLACK)
        elif self.option == "options":
            pyxel.text(self.start[0], self.start[1] + 0, f"-Difficulty [<]{self.difficulty}[>]", pyxel.COLOR_RED)
            pyxel.text(self.start[0], self.start[1] + 10, "-[B]ack", pyxel.COLOR_RED)
            pyxel.blt (self.title[0], self.title[1], 1, 0, 0, 50, 9, pyxel.COLOR_BLACK)
    def update(self):
        # Start Menu
        if self.option == "menu":
            # Start
            if pyxel.btn(pyxel.KEY_S):
                self.running = False
            # Pratice
            elif pyxel.btn(pyxel.KEY_P):
                self.option = "practice"
            # Options
            elif pyxel.btn(pyxel.KEY_O):
                self.option = "options"
        # Pratice Menu
        elif self.option == "practice":
            # Back
            if pyxel.btn(pyxel.KEY_B):
                self.option = "menu"
            # Pong
            elif pyxel.btn(pyxel.KEY_1):
                self.practice = 1
                self.option = "menu"
                self.running = False
            # BallNChain
            elif pyxel.btn(pyxel.KEY_2):
                self.practice = 2
                self.option = "menu"
                self.running = False
            # Dodge
            elif pyxel.btn(pyxel.KEY_3):
                self.practice = 3
                self.option = "menu"
                self.running = False
        # Options Menu
        elif self.option == "options":
            # Back
            if pyxel.btn(pyxel.KEY_B):
                self.option = "menu"
            # Difficulty Changer - btnr: 1 change per press(No holding)
            if pyxel.btnr(pyxel.KEY_COMMA):
                if self.difficulty > 1:
                    self.difficulty -= 1
            elif pyxel.btnr(pyxel.KEY_PERIOD):
                    self.difficulty += 1
