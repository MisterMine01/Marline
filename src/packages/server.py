import socket
from typing import Callable, Any
import threading
import logging


class Server:
    port: int
    socket: socket.socket
    thread: list[threading.Thread]

    def __init__(self, port: int) -> None:
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('', self.port))
        self.thread = []

    def listen(self, callback: Callable[[socket.socket, Any], None]) -> None:
        while True:
            self.socket.listen(5)
            client, address = self.socket.accept()
            logging.info(f"Connected to {address[0]}:{address[1]}")
            thread = threading.Thread(target=callback, args=(client, address))
            thread.start()
            self.thread.append(thread)
