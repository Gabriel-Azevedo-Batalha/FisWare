import pyxel


# Menu
class Menu():
    # Creation
    def __init__(self):
        self.running = True
        self.buttons = [60, 60]
        self.title = [65, 30]
        self.option = "menu"
        self.practice = 0
        self.difficulty = 1

    # Draw
    def draw(self, games):
        pyxel.cls(0)
        # 1st Button coordnate
        x, y = self.buttons
        # Initial Screen
        if self.option == "menu":
            pyxel.text(x, y, "-[S]tart", pyxel.COLOR_RED)
            pyxel.text(x, y + 10, "-[P]ractice", pyxel.COLOR_RED)
            pyxel.text(x, y + 20, "-[O]ptions", pyxel.COLOR_RED)
            pyxel.blt(*self.title, 1, 0, 0, 50, 9, pyxel.COLOR_BLACK)
        # Practice Screen
        elif self.option == "practice":
            count = 1
            for i in games:
                line = '-[' + str(count) + '] ' + i   
                off = (count-1)*10              
                pyxel.text(x, y + off, line, pyxel.COLOR_RED)
                count += 1
            pyxel.text(x, y + 10 + off, "-[B]ack", pyxel.COLOR_RED)
            # pyxel.text(x, y + 30, "-[4] Claw", pyxel.COLOR_RED)
            # pyxel.text(x, y + 40, "-[B]ack", pyxel.COLOR_RED)
            pyxel.blt(*self.title, 1, 0, 0, 50, 9, pyxel.COLOR_BLACK)
        # Options Screen
        elif self.option == "options":
            text = f"-Difficulty [<]{self.difficulty}[>]"
            pyxel.text(x, y, text, pyxel.COLOR_RED)
            pyxel.text(x, y + 10, "-[B]ack", pyxel.COLOR_RED)
            pyxel.blt(*self.title, 1, 0, 0, 50, 9, pyxel.COLOR_BLACK)

    # Update
    def update(self, games):
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
            # Games
            count = 1
            for i in games:
                key = 'KEY_' + str(count)
                key = pyxel._get_constant_number(key)
                if pyxel.btn(key):
                    self.practice = count
                    self.option = "menu"
                    self.running = False
                count += 1
  
        # Options Menu
        elif self.option == "options":
            # Back
            if pyxel.btn(pyxel.KEY_B):
                self.option = "menu"
            # Difficulty Changer - btnr: 1 change per press(No holding)
            if pyxel.btnr(pyxel.KEY_COMMA):  # Down
                if self.difficulty > 1:
                    self.difficulty -= 1
            elif pyxel.btnr(pyxel.KEY_PERIOD):  # Up
                    self.difficulty += 1
