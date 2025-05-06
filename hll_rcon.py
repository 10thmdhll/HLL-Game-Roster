import requests
import json
import config

class RCONError(Exception):
    """Exception raised for RCON errors."""
    pass

class RCON:
    """
    RCON client over HTTP API endpoint.
    Fetches live game stats, then extracts player IDs.
    """
    def __init__(self, host, port, password):
        # Construct API endpoint from host and port
        self.api_endpoint = f"http://{host}:{port}/api/get_live_game_stats"
        self.password = password

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def send_command(self, command):
        # Only 'players' command is supported; command argument is ignored
        params = {'password': self.password}
        try:
            resp = requests.get(self.api_endpoint, params=params, timeout=10)
            resp.raise_for_status()
        except requests.RequestException as e:
            raise RCONError(f"HTTP API request failed: {e}")
        try:
            data = resp.json()
        except json.JSONDecodeError as e:
            raise RCONError(f"Invalid JSON response: {e}")
        # Parse stats array
        result = data.get('result', {})
        stats = result.get('stats') if isinstance(result, dict) else None
        if stats is None and isinstance(data, list):
            stats = data
        stats = stats or []
        # Extract and return player_id values
        ids = [str(item['player_id']) for item in stats if 'player_id' in item]
        print(ids)
        return "".join(ids)