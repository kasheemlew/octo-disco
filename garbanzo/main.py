import sys
import os

import asyncio
from loguru import logger

from garbanzo.controller import MainController

if __name__ == '__main__':
    logger.remove()
    logger.add(sys.stderr, level=os.environ.get("LOGLEVEL", "INFO"))

    controller = MainController()
    asyncio.run(controller.run())
