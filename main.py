from team_balancer import build_teams
from poster_generator import generate_poster
from sheets_client import fetch_roster_data
from rcon_client import fetch_live_players
from config import DEFAULT_SERVER
import sys
import os
import logging
from datetime import datetime
from discord_webhook import send_to_discord
from utils import cleanup_old_files

os.makedirs("logs", exist_ok=True)
log_file = f"logs/{datetime.now().strftime('%Y-%m-%d')}.log"
logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

cleanup_old_files("logs", days=15)
cleanup_old_files("poster_output", days=15)

def main():
    server = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SERVER
    mode = sys.argv[2] if len(sys.argv) > 2 else "two_teams"
    logging.info(f"Starting roster generation for server '{server}' in mode '{mode}'.")

    players = fetch_live_players(server)
    roster_data = fetch_roster_data()
    team1, team2 = build_teams(players, roster_data, mode)

    image_path = generate_poster(team1, team2, mode)
    send_to_discord(image_path)

    logging.info("Roster build complete.")

if __name__ == "__main__":
    main()
