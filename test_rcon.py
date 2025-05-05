import socket
import logging
import requests
import config

class RCONError(Exception):
    """Exception raised for RCON errors."""
    pass

class RCON:
    """
    RCON client supporting both direct UDP socket and HTTP API endpoint.
    If config.RCON_API_ENDPOINT is set, commands are sent via HTTP GET with password and optional server param.
    Otherwise, falls back to UDP socket to host:port.
    """
    def __init__(self, host: str, port: int, password: str, timeout: float = 3.0):
        self.host = host
        self.port = port
        self.password = password
        self.timeout = timeout
        self.sock = None
        self.api_endpoint = getattr(config, 'RCON_API_ENDPOINT', None)

    def __enter__(self):
        if self.api_endpoint:
            # verify endpoint reachable
            try:
                resp = requests.options(self.api_endpoint, timeout=self.timeout)
                resp.raise_for_status()
                logging.debug(f"RCON API endpoint reachable: {self.api_endpoint}")
            except Exception as e:
                raise RCONError(f"Cannot reach RCON API endpoint: {e}")
            return self
        # fallback to UDP
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(self.timeout)
        # Optional auth via UDP
        auth_resp = self._send_udp(self.password)
        if 'Invalid password' in auth_resp:
            raise RCONError("RCON authentication failed (invalid password)")
        return self

    def send_command(self, command: str) -> str:
        """Send a command and return the server's response as text."""
        if self.api_endpoint:
            return self._send_http(command)
        return self._send_udp(command)

    def _send_udp(self, payload: str) -> str:
        try:
            data_out = payload.encode('utf-8')
            self.sock.sendto(data_out, (self.host, self.port))
            logging.debug(f"RCON UDP → {self.host}:{self.port}: {data_out}")
            data, _ = self.sock.recvfrom(4096)
            logging.debug(f"RCON UDP ← {data}")
            return data.decode('utf-8', errors='ignore')
        except socket.timeout:
            logging.error(f"RCON UDP request to {self.host}:{self.port} timed out")
            return ''
        except Exception as e:
            logging.error(f"RCON UDP error: {e}")
            return ''

    def _send_http(self, command: str) -> str:
        try:
            # Build query parameters
            params = {'password': self.password}
            if hasattr(config, 'DEFAULT_SERVER') and config.DEFAULT_SERVER:
                params['server'] = config.DEFAULT_SERVER
            # Optionally include command if endpoint supports it
            params['command'] = command
            resp = requests.get(self.api_endpoint, params=params, timeout=self.timeout)
            logging.debug(f"RCON HTTP GET → {resp.url}")
            resp.raise_for_status()
            logging.debug(f"RCON HTTP ← status {resp.status_code}, body {resp.text}")
            return resp.text
        except Exception as e:
            logging.error(f"RCON HTTP error: {e}")
            return ''

    def __exit__(self, exc_type, exc_value, traceback):
        if self.sock:
            self.sock.close()