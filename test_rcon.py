# test_rcon.py
# Quick harness to verify both HTTP and UDP RCON functionality

import config
from hll_rcon import RCON, RCONError
from rcon_client import fetch_live_players


def test_direct_rcon():
    """
    Test the low-level RCON class directly (UDP or HTTP based on config).
    """
    host = "rcon.10thmd.org"
    port = 8010
    pwd = "readonly202505010000000000000000"
    api = "/api/get_live_game_stats"

    print(f"\n== Direct RCON Test ==")
    print(f"Host: {host}\nPort: {port}\nPassword: {'*' * len(pwd)}\nAPI Endpoint: {api}")

    try:
        with RCON(host, port, pwd) as client:
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
    print(f"\n== fetch_live_players() Test ==")
    try:
        players, err = fetch_live_players(config.DEFAULT_SERVER)
        print(f"Players: {players}")
        print(f"Error: {err}")
    except Exception as e:
        print("Error calling fetch_live_players():", e)


if __name__ == "__main__":
    print("Starting RCON tests...")
    test_direct_rcon()
    test_helper_fetch()
    print("RCON tests complete.")
