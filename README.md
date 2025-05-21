# Runner Tournament Manager

[**فارسی**](README-Fa.md)

A simple and practical system for running Runner Tournaments with game management, result recording, and visual/textual analysis capabilities.

## Introduction

This project is designed to manage Runner team tournaments. Simply place each team's binary files in the `Bins/` folder, define the games in `Games.txt`, and start the tournament by running `Run.sh`.

### Features

- Automated game execution between teams
- Game results recording in `wins.txt` with winner determination
- Tournament summary in `Result.txt`
- Visual analysis charts in `static/` folder

## Project Structure

```
Runner/
├── Bins/         # Teams' executable files
├── Games.txt     # Game definitions (team matchups)
├── wins.txt      # Game results (output)
├── Result.txt    # Overall results summary (output)
├── static/       # Visual analysis images
├── run.sh        # Tournament execution script
├── Analyzer/     # Processing and analysis scripts
└── README.md
```

## Usage Guide

### Team Preparation

Place team executable files (binaries) in the `Bins/` folder. Each team must be independently executable.

### Match Definitions

In `Games.txt`, every two lines define a match between two teams. Format:

```
TeamA
TeamB
```

Note: Use the folder name containing the team's binary, not the team name.

### Running the Tournament

Execute the tournament with:

```bash
./Run.sh
```

This will:

1. Run games according to Games.txt
2. Save results in wins.txt and Result.txt
3. Generate visual analyses in static/

# Outputs

- wins.txt: Detailed game results with winners
- Result.txt: Summary of wins/losses/draws per team
- static/: Tournament analysis charts

# Requirements

- Linux or macOS
- Python 3.x (with networkx, matplotlib etc.)
- Execute permission for Run.sh (chmod +x Run.sh)

# License

MIT License

# Contact

For issues/questions, please use the repository's Issues section.

---

[**Soroush Mazloum**](https://github.com/SoroushMazloum)

[**Saleh Hamrahi**](https://github.com/SalehHamrahi)
