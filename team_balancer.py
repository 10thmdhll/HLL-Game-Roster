from collections import defaultdict

def build_teams(players, roster_data, mode="two_teams"):
    print(f"Building teams with mode: {mode}")
    print(f"Incoming players: {players}")
    print(f"Roster data keys: {list(roster_data.keys())[:10]}...")  # sample only

    matched = []
    unmatched = []

    for pid in players:
        pid_str = str(pid).strip()
        if pid_str in roster_data:
            matched.append(pid_str)
            print(f"Matched player: {pid_str} → {roster_data[pid_str]}")
        else:
            unmatched.append(pid_str)
            print(f"Unmatched player: {pid_str}")

    # Group players by role and assignment
    roles = defaultdict(lambda: {"players": [], "role_info": None})
    for pid in matched:
        role_info = roster_data[pid]
        key = (
            role_info.get("role_type", "infantry"),
            role_info.get("company", ""),
            role_info.get("platoon", ""),
            role_info.get("squad", "")
        )
        roles[key]["players"].append(pid)
        roles[key]["role_info"] = role_info  # Store role_info with the group

    # Build squads within role caps
    team1, team2 = [], []
    team_toggle = True

    for key, value in roles.items():
        group = value["players"]
        role_info = value["role_info"]
        role_type = role_info.get("role_type", "infantry")
        max_size = role_info.get("squad_size", 6 if role_type == "infantry" else 3)

        subgroups = [group[i:i+max_size] for i in range(0, len(group), max_size)]

        for squad in subgroups:
            if mode == "one_team":
                team1.append(squad)
            else:
                if team_toggle:
                    team1.append(squad)
                else:
                    team2.append(squad)
                team_toggle = not team_toggle

    return team1, team2
