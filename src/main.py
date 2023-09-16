from packages import setup_log, Server, Socket, Cache, Extension, Client
import json
import logging
from typing import Any
import os


class Main:
    config: dict[str, Any]
    server: Server
    cache: Cache
    extensions: dict[str, Extension]

    def __init__(self, config_file: str) -> None:
        self.config = json.load(open(config_file))
        setup_log(self.config["log_folder"])
        self.server = Server(self.config["port"])
        self.cache = Cache(self.config["cache_file"])
        os.makedirs(self.config["config_folder"])
        self.extensions = {}

    def run(self) -> None:
        self.server.listen(self.handle)

    def handle(self, client: Client) -> None:
        stop = False
        while not stop:
            data = client.recv(1024)
            if data:
                logging.info(f"Received {data} from {address[0]}:{address[1]}")
                client.send(data)
            else:
                stop = True
        client.close()


if __name__ == "__main__":
    main = Main("config.json")
    main.run()
