from packages import setup_log, Server, Socket
import json
import logging
from typing import Any


class Main:
    config: dict[str, Any]
    server: Server

    def __init__(self, config_file: str) -> None:
        self.config = json.load(open(config_file))
        setup_log(self.config["log_folder"])
        self.server = Server(self.config["port"])

    def run(self) -> None:
        self.server.listen(self.handle)

    def handle(self, client: Socket, address: Any) -> None:
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
