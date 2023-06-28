import pyxel


# Menu
class Menu():
    def __init__(self):
        self.running = True
        self.buttons = [60, 60]
        self.title = [65, 30]
        self.option = "menu"
        self.practice = 0
        self.difficulty = 1
        self.music = False
        self.mute = False

    # Get Minigames Names
    def GetName(self, game):
        return game.name

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
            # Minigame list
            for i in games:
                line = '-[' + str(count) + '] ' + i
                off = (count-1)*10
                pyxel.text(x, y + off, line, pyxel.COLOR_RED)
                count += 1
            pyxel.text(x, y + 10 + off, "-[B]ack", pyxel.COLOR_RED)
            pyxel.blt(*self.title, 1, 0, 0, 50, 9, pyxel.COLOR_BLACK)
        # Options Screen
        elif self.option == "options":
            text = f"-Difficulty [<]{self.difficulty}[>]"
            pyxel.text(x, y, text, pyxel.COLOR_RED)
            pyxel.text(x, y + 10, "-[M]ute", pyxel.COLOR_RED)
            pyxel.text(x, y + 20, "-[B]ack", pyxel.COLOR_RED)
            pyxel.blt(*self.title, 1, 0, 0, 50, 9, pyxel.COLOR_BLACK)

    # Update
    def update(self, games):
        # Music
        if not self.music and not self.mute:
            self.music = True
            pyxel.playm(1, loop=True)
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
            # Keys for each minigame(Numbers)
            for i in games:
                key = 'KEY_' + str(count)
                key = getattr(pyxel, key)
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
            # Mute
            if pyxel.btnr(pyxel.KEY_M):
                if self.mute:
                    self.mute = False
                    pyxel.playm(1, loop=True)
                else:
                    self.mute = True
                    pyxel.stop()
