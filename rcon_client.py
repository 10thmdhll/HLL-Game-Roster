from hll_rcon import RCON
import config
import logging
import re

def fetch_live_players(server_name):
    server = config.SERVERS[server_name]
    print(f"Connecting to RCON at {server['host']}:{server['port']}")

    try:
        with RCON(server['host'], server['port'], server['password']) as rcon:
            response = rcon.send_command('Players')
            print("RCON response:\n", response)
    except Exception as e:
        logging.error(f"Failed to fetch players from RCON server '{server_name}': {e}")
        return [], f"Failed to fetch players from RCON server '{server_name}': {e}"

    steam_ids = re.findall(r'7656119\d{10}', response)
    return steam_ids, None