import config
import logging
from hll_rcon import RCON

def fetch_live_players(server_name):
    server = config.SERVERS[server_name]
    try:
        with RCON(server['host'], server['port'], server['password']) as rcon:
            response = rcon.send_command('Players')
            print("Raw API response:\n", response)
            players = response.strip().splitlines()
            print("Parsed steam IDs:\n", players)
            return players, None
    except Exception as e:
        logging.error(f"Failed to fetch players from API for '{server_name}': {e}")
        return [], str(e)
