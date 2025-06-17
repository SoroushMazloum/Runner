source .venv/bin/activate
python3 Analyzer/graph_bar_points.py
python3 Analyzer/match_graph_with_winners.py
./convert_logs.sh
./generate_reports.sh
python3 tactical_analysis.py