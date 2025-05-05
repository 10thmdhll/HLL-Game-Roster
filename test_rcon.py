# test_rcon.py
# Quick harness to verify HTTP-based RCON API functionality and helper fetch.

import os
import config
from hll_rcon import RCON, RCONError
from rcon_client import fetch_live_players

# Configuration: override or set defaults here
HOST = os.getenv('RCON_HOST', 'rcon.10thmd.org')
PORT = int(os.getenv('RCON_PORT', '8010'))
PASSWORD = os.getenv('RCON_PASSWORD', 'readonly202505010000000000000000')
API_ENDPOINT = "http://rcon.10thmd.org:8011/api/get_live_game_stats"

# Ensure our API endpoint is used by hll_rcon
config.RCON_API_ENDPOINT = API_ENDPOINT


def test_direct_rcon():
    """
    Test the low-level RCON class via HTTP API endpoint.
    """
    print("\n== Direct RCON Test ==")
    print(f"Host: {HOST}\nPort: {PORT}\nAPI Endpoint: {API_ENDPOINT}")

    try:
        with RCON(HOST, PORT, PASSWORD) as client:
            response = client.send_command("players")
            if response:
                print("RCON Response:\n", response)
            else:
                print("RCON returned no data.")
    except RCONError as e:
        print("RCONError:", e)
    except Exception as e:
        print("Unexpected error:", e)


def test_helper_fetch():
    """
    Test the convenience helper fetch_live_players() from rcon_client.
    """
    print("\n== fetch_live_players() Test ==")
    try:
        players, err = fetch_live_players(config.DEFAULT_SERVER)
        print("Players:", players)
        print("Error:", err)
    except Exception as e:
        print("Error calling fetch_live_players():", e)


if __name__ == "__main__":
    print("Starting RCON tests...")
    test_direct_rcon()
    test_helper_fetch()
    print("RCON tests complete.")
