import socket
import json
import os

CLIENT_VERSION = "0.0.1"


class Client:
    """Client class."""

    port: int
    host: str
    socket: socket.socket
    variables: dict[str, str]

    def __init__(self, host: str, port: int) -> None:
        """Initialize the client."""
        self.port = port
        self.host = host
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.variables = {}
        self.socket.send(json.dumps({"command": "Marline.connection",
                                     "version": CLIENT_VERSION}).encode())
        data = json.loads(self.recv().decode())
        if not data["ok"]:
            raise Exception(data["error"])
        self.variables = data["variables"]
        self.variables = {key: self.set_variable(value)
                          for key, value in self.variables.items()}
        self.socket.send(json.dumps({"command": "Marline.return_variables",
                                     "variables": self.variables}).encode())
        data = json.loads(self.recv().decode())
        if not data["ok"]:
            raise Exception(data["error"])

    def set_variable(self, value: str) -> str:
        """Initialize a variable."""
        while value.find("${") != -1:
            start = value.find("${")
            end = value.find("}")
            variable = value[start + 2:end]
            value = value[:start] + os.environ[variable] + value[end + 1:]
        return value

    def recv(self, size: int = 4096) -> bytes:
        """Receive data from the client."""
        return self.socket.recv(size)

    def send(self, data: bytes) -> None:
        """Send data to the client."""
        self.socket.send(data)

    def close(self) -> None:
        """Close the client."""
        self.socket.close()


if __name__ == "__main__":
    port: int = 4469
    client = Client("127.0.0.1", port)
    try:
        repo_config = json.load(open("marline.json"))
    except FileNotFoundError:
        raise Exception("marline.json not found")
    # TODO

