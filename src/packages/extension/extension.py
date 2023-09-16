from abc import ABC
from ..cache import Cache
from ..config import Config
from typing import Callable
from ..server import Client


class Extension(ABC):
    """Base class for extensions."""

    cache: Cache
    config: Config
    extension_name: str
    variables: dict[str, str]

    command: dict[str, Callable[[Client, dict], dict]]

    def __init__(self, cache: Cache, config: Config,
                 extensions_name: str) -> None:
        self.cache = cache
        self.config = config
        self.extension_name = extensions_name
        self.variables = {}

    def launch(self, command: str, client: Client, parameters) -> dict:
        """Launch a command."""
        if command in self.command:
            return self.command[command](client, parameters)
        else:
            return {"ok": False, "error": "command not found"}
