from collections import defaultdict
import random

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
    for pid in matched:
        role_info = roster_data[pid]
        key = (
            role_info.get("role_type", "infantry"),
            role_info.get("company", ""),
            role_info.get("platoon", ""),
            role_info.get("squad", "")
        )
        roles[key].append(pid)

    # Build squads within role caps
    team1, team2 = [], []
    team_toggle = True

    for key, group in roles.items():
        role_type, company, platoon, squad = key
        max_size = role_info.get("squad_size", 6 if role_type == "infantry" else 3)

        # Split large squads
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
