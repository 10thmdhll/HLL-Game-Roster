import config
import logging
from hll_rcon import RCON, RCONError

def fetch_live_players(server_name):
    server = config.SERVERS[server_name]
    try:
        with RCON(server['host'], server['port'], server['password']) as rcon:
            response = rcon.send_command('players')
            players, error = response, None
            return players, None
    except Exception as e:
        logging.error(f"Failed to fetch players from API for '{server_name}': {e}")
        return [], str(e)
