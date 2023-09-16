import json
from typing import Any
import os


class Cache:
    file_path: str
    data: dict[str, Any]

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        if os.path.exists(file_path):
            self.data = json.load(open(file_path))
        else:
            self.data = {}
        self.save()

    def get(self, key: str) -> Any:
        if key not in self.data:
            return None
        return self.data[key]

    def set(self, key: str, value: Any) -> None:
        self.data[key] = value
        self.save()

    def save(self) -> None:
        with open(self.file_path, "w") as f:
            f.write(json.dumps(self.data, indent=4))
