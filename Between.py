import pyxel
from random import randint


# Between Minigame Processing
class Between():

    # Creation
    def __init__(self, nGames):
        self.difficulty = 1                     # Difficulty
        self.nGames = nGames                    # Number of minigames
        self.game = randint(1, self.nGames)     # Starting Game
        self.first = True
        self.running = False
        self.win = False

    # Between Minigame calculations
    def calc(self, win, practice, mute):
        self.running = True
        self.practice = practice
        if not mute:
            if win:
                pyxel.play(0, 50)
            else:
                pyxel.play(0, 51)
        # Minigame Win(Normal)
        if win and not practice:
            self.difficulty += 1
            self.win = True
            self.randomize()
        # Minigame Lose(Normal)
        elif not practice:
            self.win = False
            self.first = True
            self.randomize()
        # Minigame End(Practice)
        else:
            self.win = win
            self.first = True

    # Minigame Randomizing
    def randomize(self):
        self.game += randint(1, self.nGames - 1)
        if self.game > self.nGames:
            self.game -= self.nGames

    # Result Screen
    def draw(self, win, startingDifficulty):
        pyxel.load("assets.pyxres")
        pyxel.cls(0)
        # Minigame Win Screen
        if win:
            # Practice Win
            if self.practice:
                pyxel.text(70, 30, "You Won !", pyxel.COLOR_YELLOW)
                pyxel.text(50, 40, "Now try on Normal Game", pyxel.COLOR_RED)
                pyxel.text(45, 110, "Press Enter to continue", pyxel.COLOR_RED)
            # Normal Win
            else:
                pyxel.text(70, 30, "You Won !", pyxel.COLOR_YELLOW)
                pyxel.text(55, 40, "Difficulty Increased", pyxel.COLOR_RED)
                pyxel.text(45, 110, "Press Enter to continue", pyxel.COLOR_RED)
        # Minigame Lose Screen
        else:
            # Practice Lose
            if self.practice:
                pyxel.text(70, 30, "You Lose !", pyxel.COLOR_YELLOW)
                text = "Look like you need to practice more"
                pyxel.text(20, 40, text, pyxel.COLOR_RED)
                pyxel.text(45, 110, "Press Enter to continue", pyxel.COLOR_RED)
            # Normal Lose
            else:
                pyxel.text(45, 110, "Press Enter to continue", pyxel.COLOR_RED)
                pyxel.text(70, 30, "You Lose !", pyxel.COLOR_YELLOW)
                text = str(self.difficulty-startingDifficulty)
                pyxel.text(65, 40, "Your Score: " + text, pyxel.COLOR_RED)

    # Update
    def update(self):
        if pyxel.btn(pyxel.KEY_RETURN):
            self.running = False
