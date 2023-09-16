import os
import runpy
from typing import Any

from .extension import Extension
from ..cache import Cache
from ..config import Config
from ..server import Client


def generate_extensions(extension_folder: str,
                        cache: Cache, cache_folder: str) \
        -> dict[str, Extension]:
    """Generate extensions from a folder."""
    extensions = {}
    for extension in os.listdir(extension_folder):
        if os.path.isdir(os.path.join(extension_folder, extension)):
            extension_file = os.path.join(extension_folder, extension,
                                          "main.py")
        if os.path.isfile(os.path.join(extension_folder, extension)):
            extension_file = os.path.join(extension_folder, extension_file)
        extension = runpy.run_path(
            extension_file,
            init_globals={
                "is_extension": True,
                "Cache": Cache,
                "Config": Config,
                "Extension": Extension,
                "Client": Client
            }
        )
        extension = extension["__extension__"]
        extension_name = extension["name"]
        extension_class = extension["class"]
        config_file = os.path.join(cache_folder, extension_name + ".json")
        config = Config(config_file)
        extensions[extension_name] = extension_class(cache, config)
    return extensions
