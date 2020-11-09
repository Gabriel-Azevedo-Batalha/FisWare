import pyxel
from time import sleep
from random import randint

class Between():
    
    def __init__(self, nGames):
        self.difficulty = 1                     # Difficulty
        self.nGames = nGames                    # Number of minigames
        self.game = randint(1, self.nGames)     # Starting Game
        self.first = True
        self.running = False
        self.win = False

    def calc(self, win, practice):
        # Minigame win screen
        self.running = True
        self.practice = practice
        if win and not practice:
            self.difficulty += 1 
            self.win = True
            self.randomize()
        elif not practice:
            self.win = False
            self.first = True
            self.randomize()
        else:
            self.win = win
            self.first = True    
    def randomize(self):
        # Minigame Randomizing
        self.game += randint(1, self.nGames - 1)
        if self.game > self.nGames:
            self.game -= self.nGames
    def draw(self, win, startingDifficulty):

        if win:
            if self.practice:
                pyxel.text(70, 30, "You Won !", pyxel.COLOR_YELLOW)
                pyxel.text(50, 40, "Now try on Normal Game", pyxel.COLOR_RED)
                pyxel.text(45, 110, "Press Enter to continue", pyxel.COLOR_RED)
            else:
                pyxel.text(70, 30, "You Won !", pyxel.COLOR_YELLOW)
                pyxel.text(55, 40, "Difficulty Increased", pyxel.COLOR_RED)
                pyxel.text(45, 110, "Press Enter to continue", pyxel.COLOR_RED)
        else:
            if self.practice:
                pyxel.text(70, 30, "You Lose !", pyxel.COLOR_YELLOW)
                pyxel.text(20, 40, "Look like you need to practice more", pyxel.COLOR_RED)
                pyxel.text(45, 110, "Press Enter to continue", pyxel.COLOR_RED)
            else:
                pyxel.text(45, 110, "Press Enter to continue", pyxel.COLOR_RED)
                pyxel.text(70, 30, "You Lose !", pyxel.COLOR_YELLOW)
                pyxel.text(65, 40, "Your Score: "+str(self.difficulty-startingDifficulty), pyxel.COLOR_RED)
    def update(self):
        if pyxel.btn(pyxel.KEY_ENTER):
            self.running = False