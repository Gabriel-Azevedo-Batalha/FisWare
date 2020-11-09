import pyxel, pymunk 
import Pong, BallNChain, Dodge
import Menu, Between

pyxel.init(180, 120, fps = 30)
Chain = BallNChain.BallNChain()
Pong = Pong.Pong()
Dodge = Dodge.Dodge()
Menu = Menu.Menu()
Between = Between.Between(nGames = 3)
games = [Pong, Chain, Dodge]

def update():
    if Between.running:
        Between.update()
    elif Menu.running:
        Menu.update()
        if Between.difficulty != 1:
            Between.difficulty = 1
    elif Menu.practice != 0:
        Between.game = Menu.practice
        Between.first = False
        Between.difficulty = Menu.difficulty
        start()
        Menu.practice = 0
    else:
        if Chain.running:
            Chain.update()
        elif Pong.running:
            Pong.update()
        elif Dodge.running:
            Dodge.update()
        elif not Between.first:
            if games[Between.game - 1].win:
                games[Between.game - 1].win = False
                Between.calc(win = True, practice=games[Between.game - 1].practice)
                if games[Between.game - 1].practice:
                    Menu.running = True
                else:
                    start()
            else:
                Between.calc(win = False, practice=games[Between.game - 1].practice)
                Menu.running = True
        else:
            Between.first = False
            Between.difficulty = Menu.difficulty
            start()


def draw():
    pyxel.cls(0)
    if Between.running:
        Between.draw(Between.win, Menu.difficulty)
    elif Menu.running:
        Menu.draw()
    elif Chain.running:
        Chain.draw()
    elif Pong.running:
        Pong.draw()
    elif Dodge.running:
            Dodge.draw()
   
def start():
    if Menu.practice == 0:
        games[Between.game - 1].start(difficulty=Between.difficulty)
    else :
        games[Between.game - 1].start(difficulty=Between.difficulty, practice=True)

pyxel.load("assets.pyxres")
pyxel.playm(0, loop=True)
pyxel.run(update, draw)