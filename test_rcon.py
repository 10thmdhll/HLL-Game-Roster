#!/usr/bin/env python3
# test_rcon.py
"""
Test the RCON HTTP API endpoint directly and via the RCON class and helper.
"""

# Top-level check to confirm script execution
import sys
print("=== test_rcon.py loaded ===", flush=True)

import os
import requests
import config
from hll_rcon import RCON, RCONError
from rcon_client import fetch_live_players

# Configuration
HOST = os.getenv('RCON_HOST', 'rcon.10thmd.org')
PORT = int(os.getenv('RCON_PORT', '8010'))
PASSWORD = os.getenv('RCON_PASSWORD', 'readonly202505010000000000000000')  # default password
API_URL = "http://rcon.10thmd.org:8011/api/get_live_game_stats"
DEFAULT_SERVER = getattr(config, 'DEFAULT_SERVER', None)


def test_http_api():
    """Directly GET the API endpoint with query params to retrieve live game stats."""
    print("\n== HTTP API Direct Test ==", flush=True)
    try:
        params = {'password': PASSWORD}
        if DEFAULT_SERVER:
            params['server'] = DEFAULT_SERVER
        resp = requests.get(API_URL, params=params, timeout=5)
        print(f"Request URL: {resp.url}", flush=True)
        print(f"Status Code: {resp.status_code}", flush=True)
        print("Response Body:\n", resp.text, flush=True)
    except Exception as e:
        print("HTTP API Test Error:", e, flush=True)


def test_rcon_class():
    """Test the RCON class using HTTP API endpoint override."""
    print("\n== RCON Class Test (HTTP) ==", flush=True)
    config.RCON_API_ENDPOINT = API_URL
    try:
        with RCON(HOST, PORT, PASSWORD) as client:
            out = client.send_command("players")
            print("RCON Class Response:\n", out if out else "<empty>", flush=True)
    except RCONError as e:
        print("RCONError:", e, flush=True)
    except Exception as e:
        print("Unexpected Error:", e, flush=True)


def test_helper_fetch():
    """Test the helper fetch_live_players() which uses RCON class under the hood."""
    print("\n== fetch_live_players() Test ==", flush=True)
    try:
        players, err = fetch_live_players(DEFAULT_SERVER)
        print("Players:", players, flush=True)
        print("Error:", err, flush=True)
    except Exception as e:
        print("fetch_live_players() Error:", e, flush=True)


if __name__ == "__main__":
    print("Starting RCON HTTP API tests...", flush=True)
    test_http_api()
    test_rcon_class()
    test_helper_fetch()
    print("RCON HTTP API tests complete.", flush=True)
