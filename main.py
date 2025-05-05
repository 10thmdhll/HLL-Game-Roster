import sys
import os
import logging
from datetime import datetime

from config import DEFAULT_SERVER, POSTER_OUTPUT_DIR, LOG_DIR
from sheets_client import fetch_roster_data
from rcon_client import fetch_live_players
from team_balancer import build_teams
from poster_generator import generate_poster
from discord_webhook import send_to_discord
from utils import cleanup_old_files

# Setup logging and folders
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(POSTER_OUTPUT_DIR, exist_ok=True)
log_file = f"{LOG_DIR}/{datetime.now().strftime('%Y-%m-%d')}.log"
logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Purge old logs and posters
cleanup_old_files(LOG_DIR, days=15)
cleanup_old_files(POSTER_OUTPUT_DIR, days=15)

def main():
    server = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SERVER
    mode = sys.argv[2] if len(sys.argv) > 2 else "two_teams"
    logging.info(f"Generating roster for server '{server}' with mode '{mode}'")

    # Get live players
    players, error = fetch_live_players(server)
    if error:
        logging.error(error)
        print(error)
        return

    # Load roster structure from Google Sheets
    roster_data = fetch_roster_data()
    team1, team2 = build_teams(players, roster_data, mode)

    # Generate and send poster
    image_path = generate_poster(team1, team2, mode)
    send_to_discord(image_path)
    logging.info("Roster successfully posted.")

if __name__ == "__main__":
    main()