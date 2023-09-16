import json
from typing import Any
import os


class Config(dict[str, Any]):
    file: str

    def __init__(self, config_file: str) -> None:
        self.file = config_file
        if os.path.exists(config_file):
            super().__init__(json.load(open(config_file)))
        else:
            super().__init__()

    def save(self) -> None:
        with open(self.file, "w") as f:
            f.write(json.dumps(self.data, indent=4))
