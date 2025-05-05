import socket

class RCON:
    def __init__(self, host, port, password):
        self.host = host
        self.port = port
        self.password = password
        self.socket = None

    def __enter__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(5)
        self.socket.connect((self.host, self.port))
        self._auth()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.socket:
            self.socket.close()

    def _auth(self):
        self.socket.sendall((self.password + "\n").encode())

    def send_command(self, command):
        self.socket.sendall((command + "\n").encode())
        data = self.socket.recv(4096).decode()
        return data