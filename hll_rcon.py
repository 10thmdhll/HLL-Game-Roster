import requests
import json

class RCONError(Exception):
    """Exception raised for RCON errors."""
    pass

class RCON:
    def __init__(self, host, port, password):
        self.url = f"http://{host}:{port}/api/get_live_game_stats"
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

        try:
            data = response.json()
        except json.JSONDecodeError:
            data = json.loads(response.text)

        players = []
        if "result" in data:
            result = data["result"]
            if isinstance(result, list):
                players = [p.get("player_id") for p in result if "player_id" in p]
            elif isinstance(result, dict) and "stats" in result:
                players = [p.get("player_id") for p in result["stats"] if "player_id" in p]

        return "\n".join([p for p in players if p])
