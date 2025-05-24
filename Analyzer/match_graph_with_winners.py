import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

def build_colored_match_graph():
    base_path = os.path.dirname(os.path.abspath(__file__))
    wins_path = os.path.join(base_path, "..", "wins.txt")

    G = nx.DiGraph()
    G_undirected = nx.Graph()

    with open(wins_path) as f:
        for line in f:
            if "->" not in line:
                continue

            parts = line.strip().split("->")
            if len(parts) != 2:
                continue 

            score_part, winner = map(str.strip, parts)

            parts = score_part.split()
            if len(parts) < 5:
                continue

            team1 = parts[0]
            score1 = int(parts[1])
            score2 = int(parts[3])
            team2 = parts[4]

            if score1 > score2:
                from_team, to_team = team2, team1
                if G.has_edge(from_team, to_team):
                    G[from_team][to_team]['weight'] += 1
                else:
                    G.add_edge(from_team, to_team, weight=1)
            elif score2 > score1:
                from_team, to_team = team1, team2
                if G.has_edge(from_team, to_team):
                    G[from_team][to_team]['weight'] += 1
                else:
                    G.add_edge(from_team, to_team, weight=1)
            else:
                edge = tuple(sorted([team1, team2]))
                if G_undirected.has_edge(*edge):
                    G_undirected[edge[0]][edge[1]]['weight'] += 1
                else:
                    G_undirected.add_edge(edge[0], edge[1], weight=1)

    combined_nodes = set(G.nodes) | set(G_undirected.nodes)
    pos = nx.spring_layout(nx.Graph(list(G.edges()) + list(G_undirected.edges())), 
                         seed=42, k=0.3, scale=2)

    fig, ax = plt.subplots(figsize=(14, 10))

    def normalize_weights(weights, min_w=1.0, max_w=3.0):
        if not weights:
            return []
        min_weight = min(weights)
        max_weight = max(weights)
        if min_weight == max_weight:
            return [(min_w + max_w) / 2] * len(weights)
        return [min_w + (w - min_weight) * (max_w - min_w) / (max_weight - min_weight) for w in weights]

    edge_weights_directed = normalize_weights([G[u][v]['weight'] for u, v in G.edges()])
    edge_weights_undirected = normalize_weights([G_undirected[u][v]['weight'] for u, v in G_undirected.edges()])

    nx.draw_networkx_edges(
        G, pos,
        width=edge_weights_directed,
        edge_color='black',
        arrows=True,
        arrowstyle='-|>',
        arrowsize=20,
        ax=ax,
        node_size=2000,
        min_source_margin=15,
        min_target_margin=15
    )

    nx.draw_networkx_edges(
        G_undirected, pos,
        width=edge_weights_undirected,
        edge_color='blue',
        style='dashed',
        ax=ax
    )

    for node in combined_nodes:
        x, y = pos[node]
        width = 0.25
        height = 0.1

        rect = patches.FancyBboxPatch(
            (x - width/2, y - height/2),
            width,
            height,
            boxstyle="round,pad=0.03",
            linewidth=1,
            edgecolor='black',
            facecolor='lightblue',
            alpha=0.6,
            zorder=2
        )
        ax.add_patch(rect)
        ax.text(x, y, node, fontsize=10, fontweight='bold',
                horizontalalignment='center', verticalalignment='center', 
                zorder=3, color='black')

    edge_labels_directed = {(u, v): G[u][v]['weight'] for u, v in G.edges()}
    edge_labels_undirected = {(u, v): G_undirected[u][v]['weight'] for u, v in G_undirected.edges()}
    
    nx.draw_networkx_edge_labels(
        G, pos, 
        edge_labels=edge_labels_directed, 
        ax=ax, 
        font_size=8,
        label_pos=0.6
    )
    nx.draw_networkx_edge_labels(
        G_undirected, pos, 
        edge_labels=edge_labels_undirected, 
        ax=ax, 
        font_size=8,
        label_pos=0.5
    )

    plt.title("Match Result Graph: Directed Wins (Black), Draws (Blue)", fontsize=14)
    plt.axis('off')
    plt.tight_layout()
    os.makedirs("Analysis_Results", exist_ok=True)
    plt.savefig("Analysis_Results/match_network_colored.png", dpi=300, bbox_inches='tight')

if __name__ == "__main__":
    build_colored_match_graph()