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
    roles = defaultdict(list)
    role_infos = {}
    for pid in matched:
        role_info = roster_data[pid]
        key = (
            role_info.get("role_type", "infantry"),
            role_info.get("company", ""),
            role_info.get("platoon", ""),
            role_info.get("squad", "")
        )
        roles[key].append(pid)
        role_infos[key] = role_info  # Store one example role_info for each key

    # Build squads within role caps
    team1, team2 = [], []
    team_toggle = True

    for key, group in roles.items():
        role_info = role_infos.get(key, {})
        role_type, company, platoon, squad_name = key
        max_size = role_info.get("squad_size", 6 if role_type == "infantry" else 3)

        subgroups = [group[i:i+max_size] for i in range(0, len(group), max_size)]

        for squad in subgroups:
            squad_dict = {
                "squad": f"{company}/{platoon}/{squad_name}",
                "players": [roster_data[pid].get("Name", pid) for pid in squad]
            }

            if mode == "one_team":
                team1.append(squad_dict)
            else:
                if team_toggle:
                    team1.append(squad_dict)
                else:
                    team2.append(squad_dict)
                team_toggle = not team_toggle

    return team1, team2
