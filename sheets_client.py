import gspread
from google.oauth2.service_account import Credentials
import config

def fetch_roster_data():
    """
    Fetches the 'Main Roster' and 'Squad Designations' sheets and returns a dict mapping RCON ID strings to row dicts,
    explicitly including the 'Name' column.
    Debug prints are included to trace execution and data retrieval.
    """
    #print("fetch_roster_data: start")
    try:
        creds = Credentials.from_service_account_file(
            "secrets/google_service_account.json",
            scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
        )
        #print("Credentials loaded successfully")
        client = gspread.authorize(creds)
        #print("Gspread client authorized")
        sheet = client.open_by_key(config.GOOGLE_SHEET_ID)
        #print(f"Opened spreadsheet with key: {config.GOOGLE_SHEET_ID}")

        main_roster = sheet.worksheet("Main Roster").get_all_records()
        #print(f"Fetched {len(main_roster)} rows from 'Main Roster'")
        designations = sheet.worksheet("Squad Designations").get_all_records()
        #print(f"Fetched {len(designations)} rows from 'Squad Designations'")

        role_map = {}
        for idx, row in enumerate(designations, start=1):
            #print(f"Designation row {idx}: {row}")
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
        for idx, row in enumerate(main_roster, start=1):
            #print(f"Roster row {idx}: {row}")
            sid = str(row.get("RCON ID", "")).strip()
            if not sid:
                print(f"Skipping row {idx}: no RCON ID")
                continue
            Name = str(row.get("Name", "")).strip()
            company = str(row.get("Company", "")).strip()
            platoon = str(row.get("Platoon", "")).strip()
            squad = str(row.get("Squad", "")).strip()

            key_full = (Name, company, platoon, squad)
            key_partial = (Name, company, platoon, "")
            key_minimal = (Name, company, "", "")
            key_member = (Name, "", "", "")
            role_info = role_map.get(key_full) or role_map.get(key_partial) or role_map.get(key_minimal) or role_map.get(key_member) or {
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
        #print("fetch_roster_data: end")
        return roster_data
    except Exception as e:
        print(f"fetch_roster_data: exception: {e}")
        raise