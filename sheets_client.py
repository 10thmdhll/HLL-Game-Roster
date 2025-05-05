import gspread
from google.oauth2.service_account import Credentials
import config

def fetch_roster_data():
    creds = Credentials.from_service_account_file(
        "secrets/google_service_account.json",
        scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
    )
    client = gspread.authorize(creds)
    sheet = client.open_by_key(config.GOOGLE_SHEET_ID)

    main_roster = sheet.worksheet("Main Roster").get_all_records()
    designations = sheet.worksheet("Squad Designations").get_all_records()

    role_map = {}
    for row in designations:
        key = (
            str(row.get("Company", "")).strip(),
            str(row.get("Platoon", "")).strip(),
            str(row.get("Squad", "")).strip()
        )
        role_map[key] = {
            "role_type": str(row.get("Type", "")).strip().lower(),
            "squad_size": int(row.get("Squad Size", config.DEFAULT_SQUAD_SIZE))
        }

    roster_data = {}
    for row in main_roster:
        sid = str(row.get("RCON ID", "")).strip()
        if not sid:
            continue
        Name: str(row["Name"]).strip()
        company = str(row["Company"]).strip()
        platoon = str(row["Platoon"]).strip()
        squad = str(row.get("Squad", "")).strip()

        key_full = (Name, company, platoon, squad)
        key_partial = (Name, company, platoon, "")
        role_info = role_map.get(key_full) or role_map.get(key_partial) or {
            "role_type": config.DEFAULT_ROLE_TYPE,
            "squad_size": config.DEFAULT_SQUAD_SIZE
        }

        roster_data[sid] = {
            "Name": Name,
            "company": company,
            "platoon": platoon,
            "squad": squad,
            "role_type": role_info["role_type"],
            "squad_size": role_info["squad_size"]
        }
        #print(sid)

    return roster_data
