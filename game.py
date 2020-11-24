# Engine
import pyxel
import pymunk
# Games
import Pong
import BallNChain
import Dodge
#(Not implemented) import Claw
# Menu and between minigames processing
import Menu
import Between

# Inits
pyxel.init(180, 120, fps=30)
Chain = BallNChain.BallNChain()
Pong = Pong.Pong()
Dodge = Dodge.Dodge()
Menu = Menu.Menu()
games = [Pong, Chain, Dodge]
Between = Between.Between(nGames=len(games))
gameNames = list(map(Menu.GetName, games))  # Game names for practice
# Not implemented
# Claw = Claw.Claw()
# games.append(Claw)


# Update
def update():
    # Between update
    if Between.running:
        Between.update()
    # Menu update
    elif Menu.running:
        Menu.update(gameNames)
        # Change difficulty to base difficulty
        if Between.difficulty != Menu.difficulty:
            Between.difficulty = Menu.difficulty
    # Practice Start
    elif Menu.practice != 0:
        Between.game = Menu.practice
        Between.first = False
        start()
        Menu.practice = 0
    # Minigame update
    else:
        # Game running
        if games[Between.game-1].running:
            games[Between.game-1].update()
        # Between minigames
        elif not Between.first:
            # Won last minigame
            if games[Between.game-1].win:
                games[Between.game-1].win = False
                Between.calc(True, games[Between.game - 1].practice)
                # Practice End
                if games[Between.game-1].practice:
                    Menu.running = True
                else:
                    start()
            # Lost last minigame
            else:
                Between.calc(False, games[Between.game-1].practice)
                Menu.running = True
        # First minigame
        else:
            Between.first = False
            start()


# Draw
def draw():
    # Result Screen
    if Between.running:
        Between.draw(Between.win, Menu.difficulty)
    # Menu
    elif Menu.running:
        Menu.draw(gameNames)
    # Minigame
    elif games[Between.game-1].running:
            games[Between.game-1].draw()


# Start Minigame
def start():
    # Normal Mode
    if Menu.practice == 0:
        games[Between.game-1].start(Between.difficulty)
    # Practice Mode
    else:
        games[Between.game-1].start(Between.difficulty, practice=True)


# Game Load
pyxel.load("assets.pyxres")
pyxel.playm(0, loop=True)
pyxel.run(update, draw)
