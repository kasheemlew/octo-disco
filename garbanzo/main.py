import asyncio

from garbanzo.controller import MainController
from garbanzo.logger import logger

if __name__ == '__main__':
    controller = MainController()
    try:
        asyncio.run(controller.run())
    except KeyboardInterrupt:
        logger.info('interrupted by keyboard')
