import json
from typing import List


class Job:
    def __init__(
            self,
            name: str,
            host: str,
            sources: List[str],
            filters: List[Filter],
            targets: List['Job'],
    ):
        self.name = name,
        self.host = host,
        self.sources = sources
        self.filters = filters
        self.targets = targets
