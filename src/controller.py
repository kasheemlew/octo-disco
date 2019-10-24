from src.handlers.job import JobHandler
from src.handlers.source import SourceHandler


class MainController:
    def __init__(self, c1, c2, c3, c4, c5):
        self.source_handler = SourceHandler()

    def run(self):
        self.source_handler.parse_source()
