import argparse
import json
import logging
import os
from collections import defaultdict
from typing import Any, Dict, List, Tuple

from sheets_client import fetch_roster_data

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def build_teams(
    players: List[str],
    roster_data: Dict[str, Dict[str, Any]],
    mode: str = "two_teams"
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    :param players: list of RCON ID strings
    :param roster_data: mapping RCON ID → {Name, company, platoon, squad, role_type, squad_size}
    :param mode: "two_teams" (default) or "one_team"
    :returns: (team1_squads, team2_squads)
    """
    matched, unmatched = [], []
    for pid in players:
        pid_str = str(pid).strip()
        if pid_str in roster_data:
            matched.append(pid_str)
        else:
            unmatched.append(pid_str)
            logger.warning("Unmatched player: %s", pid_str)

    # Group players by (role_type, company, platoon, squad)
    roles: Dict[Tuple[str, str, str, str], List[str]] = defaultdict(list)
    for pid in matched:
        info = roster_data[pid]
        key = (
            info["role_type"],
            info["company"],
            info["platoon"],
            info["squad"]
        )
        roles[key].append(pid)

    # Build squads (chunks) and split them while balancing team sizes
    team1, team2 = [], []
    count1, count2 = 0, 0

    for (role_type, company, platoon, squad_name), group in roles.items():
        # squad_size always present in roster_data
        max_size = roster_data[group[0]]["squad_size"]

        for i in range(0, len(group), max_size):
            squad_members = group[i : i + max_size]
            label = "/".join(filter(None, [company, platoon, squad_name]))
            squad_dict = {
                "squad": label,
                "players": [roster_data[pid]["Name"] for pid in squad_members]
            }
            squad_size = len(squad_members)

            if mode == "one_team":
                team1.append(squad_dict)
                count1 += squad_size
            else:
                # assign to the lighter team
                if count1 <= count2:
                    team1.append(squad_dict)
                    count1 += squad_size
                else:
                    team2.append(squad_dict)
                    count2 += squad_size

    return team1, team2


def main():
    parser = argparse.ArgumentParser(description="Balance HLL teams by squad caps")
    parser.add_argument(
        "--players",
        required=True,
        help="Comma-separated RCON IDs or path to a file listing one ID per line."
    )
    parser.add_argument(
        "--mode",
        choices=["one_team", "two_teams"],
        default="two_teams",
        help="Assign all squads to one team or alternate between two."
    )
    args = parser.parse_args()

    if os.path.isfile(args.players):
        with open(args.players) as f:
            players = [line.strip() for line in f if line.strip()]
    else:
        players = [p.strip() for p in args.players.split(",") if p.strip()]

    roster = fetch_roster_data()
    team1, team2 = build_teams(players, roster, mode=args.mode)

    print(json.dumps({"team1": team1, "team2": team2}, indent=2))


if __name__ == "__main__":
    main()

