import os
from collections import defaultdict
import math

def analyze_results():
    base_path = os.path.dirname(os.path.abspath(__file__))
    wins_path = os.path.join(base_path, "..", "wins.txt")

    stats = defaultdict(lambda: {
        "W": 0, "D": 0, "L": 0,
        "GF": 0, "GA": 0, "P": 0,
        "FirstGame": float("inf"),
        "LastGame": -1,
        "ElimRound": -1
    })

    active_teams = set()
    round_counter = 0

    with open(wins_path) as f:
        lines = [line.strip() for line in f if "->" in line]

    for i, line in enumerate(lines):
        parts = line.split("->")
        score_part, winner = map(str.strip, parts)
        teams = score_part.strip().split()
        if len(teams) < 5:
            continue

        team1, score1, _, score2, team2 = teams
        score1, score2 = int(score1), int(score2)

        for team in (team1, team2):
            stats[team]["FirstGame"] = min(stats[team]["FirstGame"], i)
            stats[team]["LastGame"] = i
            active_teams.add(team)

        stats[team1]["GF"] += score1
        stats[team1]["GA"] += score2
        stats[team2]["GF"] += score2
        stats[team2]["GA"] += score1

        if score1 > score2:
            loser = team2
            stats[team1]["W"] += 1
            stats[team2]["L"] += 1
        elif score2 > score1:
            loser = team1
            stats[team2]["W"] += 1
            stats[team1]["L"] += 1
        else:
            stats[team1]["D"] += 1
            stats[team2]["D"] += 1
            loser = None  # draw shouldn't happen in elimination

        if loser:
            stats[loser]["ElimRound"] = i

    for team in stats:
        s = stats[team]
        s["P"] = s["W"] * 3 + s["D"]
        s["GD"] = s["GF"] - s["GA"]

    is_elimination = len(lines) == len(active_teams) - 1

    if is_elimination:
        for team in stats:
            if stats[team]["ElimRound"] == -1:
                stats[team]["ElimRound"] = math.inf

        sorted_teams = sorted(
            stats.items(),
            key=lambda x: (-x[1]["ElimRound"], x[1]["FirstGame"], x[0])
        )

        print(f"{'Rank':<5}{'Team':<20}")
        print("-" * 25)
        for idx, (team, _) in enumerate(sorted_teams, 1):
            print(f"{idx:<5}{team:<20}")

    else:
        sorted_teams = sorted(stats.items(), key=lambda x: (-x[1]["P"], -x[1]["GD"], -x[1]["W"], x[0]))
        print(f"{'Pos':<4}{'Team':<20}{'W':>3}{'D':>3}{'L':>3}{'GF':>5}{'GA':>5}{'GD':>5}{'P':>7}")
        print("-" * 60)
        for idx, (team, s) in enumerate(sorted_teams, 1):
            print(f"{idx:<4}{team:<20}{s['W']:>3}{s['D']:>3}{s['L']:>3}{s['GF']:>5}{s['GA']:>5}{s['GD']:>5}{s['P']:>7}")

analyze_results()
