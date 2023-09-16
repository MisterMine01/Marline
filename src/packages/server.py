import socket
from typing import Callable, Any
import threading
import logging


class Client:
    socket: socket.socket
    address: Any
    variables: dict[str, str]

    def __init__(self, socket: socket.socket, address: Any) -> None:
        self.socket = socket
        self.address = address

    def send(self, data: bytes) -> None:
        self.socket.send(data)

    def receive(self, size: int) -> bytes:
        return self.socket.recv(size)

    def close(self) -> None:
        self.socket.close()


class Server:
    port: int
    socket: socket.socket
    thread: list[threading.Thread]

    def __init__(self, port: int) -> None:
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('', self.port))
        self.thread = []

    def listen(self, callback: Callable[[Client], None]) -> None:
        while True:
            self.socket.listen(5)
            client, address = self.socket.accept()
            client_class = Client(client, address)
            logging.info(f"Connected to {address[0]}:{address[1]}")
            thread = threading.Thread(target=callback, args=(client_class,))
            thread.start()
            self.thread.append(thread)
