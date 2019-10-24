import aiochan as ac

from src.controller import MainController

if __name__ == '__main__':
    controller = MainController(ac.Chan(), ac.Chan(), ac.Chan(), ac.Chan(), ac.Chan())
    controller.run()
