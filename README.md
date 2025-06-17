# Runner Tournament Manager

[**English**](README.md) | **[فارسی](README-Fa.md)**

A simple and practical system for running Runner Tournaments with game management, result recording, and visual/text analysis generation capabilities.

## Introduction

This project is designed to run runner team tournaments. Simply place each team's binary files in the `Bins/` folder, define the games in the `Games.txt` file, and start the tournament by executing the `Run.sh` script.

### Features

- Automatic execution of games between different teams
- Saving game results in `wins.txt` with winner determination
- Summary of overall tournament results in `Result.txt`
- Generation of result analysis charts saved in the `Analysis_Results/` folder
- Storage of all game logs in the `Logs/` folder
- Raw game analysis in the `LogsJSON/` folder
- Detailed game analysis in the `LogsConf/` folder

## Project Structure

```
Runner/
├── Bins/                    # Team executable files
├── Games.txt                # Game definitions (matches between teams)
├── wins.txt                 # Game results (output)
├── Result.txt               # Overall results summary (output)
├── static/                  # Analysis result images
├── run.sh                   # Tournament execution script
├── install_requirements.sh  # Install requirements
├── Analyzer/                # Processing and analysis scripts
├── LogsJSON/                # Raw game analysis
├── LogsConf/                # Detailed game analysis
├── Logs/                    # Game logs
└── README.md
```

## Usage Guide

### Preparing Teams

Place team executable files (binaries) in the `Bins/` folder. Each team must be independently executable.

### Defining Matches

In the `Games.txt` file, every two lines define a match between two teams. The format should be as follows:

Note: Team names must match their display names.

**Mode 1: `Normal (Round-Robin)`:**

```
Team1
Team2
---
Team3
Team4
---
```

Note: In this mode, the first match will be between `Team1` and `Team2`, and the next match between `Team3` and `Team4`.

**Mode 2: `Elimination (Stepladder)`:**

```
TeamA
TeamB
TeamC
```

Note: In this mode, the first match is between `Team1` and `Team2`, and the winner then plays against `Team3`.

### Running the Tournament

To run the entire tournament, execute the `Run.sh` script and correctly answer the prompts:

Note: You may need to grant execution permission on first run.

```sh
./Run.sh
```

This script will execute games according to `Games.txt`, save results in wins.txt and `Result.txt`, generate visual analyses in the `Analysis_Results/` folder, and produce detailed game analysis `.conf` files in the `LogsConf/` folder.


# Outputs

- `wins.txt`: Detailed results of each game with winner determination.
- `Result.txt`: Summary of overall results (wins, losses, draws per team).
- `Analysis_Results/` folder: Tournament analysis charts and visualizations. *
- `.conf` files in `LogsConf/`: Detailed game analysis using the Namira Log-Analyzer tool. *

*: Analysis must be run manually after the games are finished.
```bash
./ANALYZE.sh
```

# Requirements

- Python 3.x (with networkx, matplotlib etc.)
- Execute permission for Run.sh (chmod +x Run.sh)

# Installing Requirements
Execute the `install_requirements.sh` file:

```sh
./install_requirements.sh
```

# License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

# Contact

For issues/questions, please use the repository's Issues section.

---

[**Soroush Mazloum**](https://github.com/SoroushMazloum)

[**Saleh Hamrahi**](https://github.com/SalehHamrahi)
