from packages import setup_log, Server, Cache, Extension, Client, \
     generate_extensions
import packages.function as function
import json
from typing import Any
import os


class Main:
    config: dict[str, Any]
    server: Server
    cache: Cache
    extensions: dict[str, Extension]
    commands: dict[str, Extension]

    def __init__(self, config_file: str) -> None:
        self.config = json.load(open(config_file))
        setup_log(self.config["log_folder"])
        self.server = Server(self.config["port"])
        self.cache = Cache(self.config["cache_file"])
        os.makedirs(self.config["config_folder"], exist_ok=True)
        self.extensions = generate_extensions(self.config["extensions_folder"],
                                              self.cache,
                                              self.config["config_folder"])

    def run(self) -> None:
        self.server.listen(self.handle)

    def handle_marline(self, client: Client, data: dict) -> None:
        command = data["command"].split(".")[1]
        match command:
            case "connection":
                function.client_function(data, client, self.extensions)
            case "return_variables":
                function.variable_function(data, client)

    def handle_command(self, client: Client, data: dict) -> None:
        extension = data["command"].split(".")[0]
        command = data["command"].split(".")[1]
        parameters = data["parameters"]
        if extension not in self.extensions:
            client.send(json.dumps({"ok": False,
                                    "error": "extension not found"}).encode())
        if command in self.extensions[extension].command:
            self.extensions[extension].command[command](client, parameters)
        else:
            client.send(json.dumps({"ok": False,
                                    "error": "command not found"}).encode())

    def handle(self, client: Client) -> None:
        stop = False
        while not stop:
            data = client.receive()
            if not data:
                stop = True
                break
            data = json.loads(data.decode())
            if data["command"].startswith('Marline.'):
                self.handle_marline(client, data)
            else:
                self.handle_command(client, data)
        client.close()


if __name__ == "__main__":
    main = Main("config.json")
    main.run()
