import matplotlib.pyplot as plt
from collections import defaultdict
import os

def analyze_and_plot():
    base_path = os.path.dirname(os.path.abspath(__file__))
    wins_path = os.path.join(base_path, "..", "Results.txt")
    
    stats = defaultdict(lambda: {"W": 0, "D": 0, "L": 0})

    with open(wins_path) as f:
        for line in f:
            if "->" not in line:
                continue
            score_part = line.strip().split(" -> ")[0]
            parts = score_part.strip().split()
            if len(parts) < 5:
                continue

            team1 = parts[0]
            score1 = int(parts[1])
            score2 = int(parts[3])
            team2 = parts[4]

            if score1 > score2:
                stats[team1]["W"] += 1
                stats[team2]["L"] += 1
            elif score2 > score1:
                stats[team2]["W"] += 1
                stats[team1]["L"] += 1
            else:
                stats[team1]["D"] += 1
                stats[team2]["D"] += 1

    teams = list(stats.keys())
    wins = [stats[t]["W"] for t in teams]
    draws = [stats[t]["D"] for t in teams]
    losses = [stats[t]["L"] for t in teams]

    x = range(len(teams))

    plt.figure(figsize=(12, 6))
    plt.bar(x, wins, color='skyblue', label='Wins')
    plt.bar(x, draws, bottom=wins, color='gold', label='Draws')
    plt.bar(x, losses, bottom=[w+d for w,d in zip(wins, draws)], color='salmon', label='Losses')

    plt.xticks(x, teams, rotation=45, ha='right')
    plt.ylabel("Number of games")
    plt.title("Team performance: win, draw, loss")
    plt.legend()
    plt.tight_layout()
    os.makedirs("Results_analysis", exist_ok=True)
    plt.savefig("Results_analysis/team_stats_chart.png")
    os.system("echo -e '\033[0;32mCreated team_stats_chart.png'")

if __name__ == "__main__":
    analyze_and_plot()
