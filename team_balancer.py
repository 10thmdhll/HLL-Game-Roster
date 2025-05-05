from collections import defaultdict

def build_teams(players, roster_data, mode="two_teams"):
    """
    Build teams from live players and roster data based on unit structure.
    players: List of player SteamIDs (from RCON)
    roster_data: Dict mapping SteamID -> {company, platoon, squad, role_type, squad_size}
    mode: "one_team" or "two_teams"
    """
    grouped = defaultdict(list)

    for steam_id in players:
        player_info = roster_data.get(steam_id)
        if not player_info:
            continue  # Skip unmatched
        key = (player_info['company'], player_info['platoon'], player_info['squad'], player_info['role_type'])
        grouped[key].append(steam_id)

    squads = []
    for (company, platoon, squad, role_type), members in grouped.items():
        max_size = player_info.get('squad_size', 6 if role_type == 'infantry' else 3 if role_type == 'armor' else 2)
        while len(members) > max_size:
            squads.append({
                'squad': f"{company}-{platoon}-{squad}",
                'role_type': role_type,
                'players': members[:max_size]
            })
            members = members[max_size:]
        if len(members) >= (3 if role_type == 'infantry' else max_size):
            squads.append({
                'squad': f"{company}-{platoon}-{squad}",
                'role_type': role_type,
                'players': members
            })

    if mode == "one_team":
        return squads, []

    # two-team balancing
    team1, team2 = [], []
    flip = True
    for squad in squads:
        (team1 if flip else team2).append(squad)
        flip = not flip

    return team1, team2