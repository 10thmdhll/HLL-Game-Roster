import requests

class RCON:
    def __init__(self, host, port, token):
        self.url = f"http://{host}:{port}/api/get_live_game_stats"
        self.token = token

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass  # No cleanup needed

    def send_command(self, command):
        if command.lower() != "players":
            raise NotImplementedError("Only 'Players' command is supported via API.")
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(self.url, headers=headers)
        response.raise_for_status()
        return response.text
