# HLL-Game-Roster

A Python tool and Discord bot for the WWII mil-sim **Hell Let Loose** that:

- Fetches the current player list via CRCON (v11.5.1)  
- Balances teams into squads according to configurable rules  
- Generates a polished “roster poster” image (PNG)  
- Posts the poster to Discord via webhook or slash-command bot  
- (Optionally) integrates with Google Sheets for custom squad templates, player metadata, etc.

---

## 🚀 Features

- **RCON integration** (`hll_rcon.py` / `rcon_client.py`)  
- **Team balancing** (`team_balancer.py`) with squad size limits  
- **Image generation** (`poster_generator.py`) using Pillow  
- **Discord delivery** (`discord_webhook.py` / `bot.py`) via webhook or bot token  
- **Google Sheets sync** (`sheets_client.py`) for player data/templates  
- Fully configurable via `.env` and `config.py`

---

## 🛠️ Requirements

- **Python** 3.8+  
- A Hell Let Loose server with **CRCON** enabled - (https://github.com/MarechJ/hll_rcon_tool)
- **Discord**: webhook URL _or_ bot token (with `applications.commands` intent)  
- **Google Sheets** (if using Sheets integration): service-account JSON credentials  
- **Recommended**: [`venv`](https://docs.python.org/3/library/venv.html) or [Poetry](https://python-poetry.org/)

---

## ⚙️ Installation

`git clone https://github.com/10thmdhll/HLL-Game-Roster.git`

`cd HLL-Game-Roster`

# Create & activate virtual environment
`python3 -m venv venv`

`source venv/bin/activate`

# Install dependencies
`pip install --upgrade pip`

`pip install -r requirements.txt`

##📝 Configuration
Copy the example env file:

`cp default.env .env`

Edit .env with your values:

Copy the example config.py file:

`cp config_example.py config.py`

Edit config with your values:

GOOGLE_SHEET_ID = "IDofGoogleSheet"

SERVERS = {
    "Server 1": {
        "host": "127.0.0.1",
        "port": 8010,
        "password": "readonlyAPI",
        "name": "Server Name 1"
    },
    "Server 2":{
        "host": "127.0.0.1",
        "port": 8011,
        "password": "readonlyAPI",
        "name": "Server Name 2"
    }
}

ROSTER_MODES = ["one_team", "two_teams"]

DISCORD_WEBHOOK_URL = "HookURL"

EVENT_NAME = "Training Event"

POSTER_OUTPUT_DIR = "poster_output"
LOG_DIR = "logs"
LOG_RETENTION_DAYS = 15
POSTER_RETENTION_DAYS = 15

DEFAULT_ROLE_TYPE = "infantry"
DEFAULT_SQUAD_SIZE = 6


🚀 Usage
1. Command-Line (CLI)
Generate a roster poster manually:

python main.py \
  --mode split       \ # “split” or other modes you’ve defined
  --output roster.png \
  --sheet-template   \ # if you want to pull squad templates from Sheets

2. Discord Bot
Ensure .env has DISCORD_BOT_TOKEN.

Run the bot:

`python bot.py`

In your server, use the slash command:

/roster

The bot will reply with the generated poster image.

📂 Directory Layout
HLL-Game-Roster/
├── bot.py                 # Discord bot entrypoint
├── main.py                # CLI entrypoint
├── hll_rcon.py            # RCON command parser  Currently set to get_live_game_stats endpoint
├── rcon_client.py         # RCON connection wrapper
├── team_balancer.py       # Team-splitting logic
├── poster_generator.py    # Pillow image composition
├── discord_webhook.py     # Simple webhook poster
├── sheets_client.py       # Google Sheets helper
├── utils.py               # Shared utilities
├── config.py              # App-wide settings loader
├── default.env            # Example environment variables -> copy to .env
├── requirements.txt       # Pinned dependencies
└── README.md              # ← You are here

📄 License
This project is licensed under the MIT License. See LICENSE for details.