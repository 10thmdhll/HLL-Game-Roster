from hll_rcon import RCON
import config
import logging

def fetch_live_players(server_name):
    """
    Attempts to connect to the specified RCON server and fetch a list of SteamIDs.
    Returns a tuple: (steam_id_list, error_message)
    If the request fails, steam_id_list is empty and error_message contains the reason.
    """
    server = config.SERVERS[server_name]
    try:
        with RCON(server['host'], server['port'], server['password']) as rcon:
            response = rcon.send_command('Players')

    except Exception as e:
        logging.error(f"Failed to fetch players from RCON server '{server_name}': {e}")
        return [], f"Failed to fetch players from RCON server '{server_name}': {e}"
    
    print("RCON raw response:\n", response)

    steam_ids = []
    for line in response.splitlines():
        parts = line.strip().split()
        for part in parts:
            if part.isdigit() and len(part) >= 17:
                steam_ids.append(part)
                break

    return steam_ids, None
