import requests

class RCON:
    def __init__(self, host, port, password):
        self.url = f"http://{host}:{port}/api/get_players"
        self.token = password

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def send_command(self, command):
        if command.lower() != "players":
            raise NotImplementedError("Only 'Players' command is supported via API.")
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(self.url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, dict) and "players" in data:
            players = [p.get("player_id") for p in data["players"] if "player_id" in p]
        elif isinstance(data, list):
            players = [p.get("player_id") for p in data if "player_id" in p]
        else:
            players = []
        return "\n".join(players)

