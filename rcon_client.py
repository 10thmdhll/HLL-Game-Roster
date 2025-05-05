import config
import logging
from hll_rcon import RCON

def fetch_live_players(server_name):
    server = config.SERVERS[server_name]
    try:
        with RCON(server['host'], server['port'], server['password']) as rcon:
            response = rcon.send_command('players')
            players = response.strip().splitlines()
            return players, None
    except Exception as e:
        logging.error(f"Failed to fetch players from API for '{server_name}': {e}")
        return [], str(e)


# test_rcon.py
def main():
    host = config.RCON_HOST      # e.g. "127.0.0.1"
    port = config.RCON_PORT      # e.g. 27015
    pwd  = config.RCON_PASSWORD  # your server’s RCON password

    print(f"Testing RCON to {host}:{port}…")
    try:
        with RCON(host, port, pwd) as client:
            resp = client.send_command("players")  # or any valid HLL RCON command
            if resp:
                print("RCON response:\n", resp)
            else:
                print("RCON returned no data.")
    except RCONError as e:
        print("RCONError:", e)
    except Exception as e:
        print("Unexpected error:", e)

if __name__ == "__main__":
    main()
