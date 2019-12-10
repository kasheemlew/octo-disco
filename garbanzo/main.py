import asyncio

from garbanzo.controller import MainController

if __name__ == '__main__':
    controller = MainController()
    asyncio.run(controller.run())
