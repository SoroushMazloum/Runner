#!/bin/bash
set -e

if [ ! -f "Games.txt" ]; then
    echo "Games.txt file not found!"
    exit 1
fi

if [ ! -d "Bins" ]; then
    echo "Bins folder not found!"
    exit 1
fi
trap 'rm -f G.txt *.rcg *.rcl Analyzer/*.rc*' EXIT

echo "Major ? (n/y): "
read m
echo "synch_mode ? (false/true): "
read sm

case "$m" in
    "n" | "N" | "y" | "Y")
        if [[ "$sm" == "true" || "$sm" == "false" ]]; then
            echo "Start a Tournament Runner ..."
            ./rcssmonitor --auto-reconnect-mode on --auto-reconnect-wait 2 &

            rm -f G.txt
            chmod +x *.sh

            while true
            do
                line_count=$(wc -l < Games.txt)
                if [ $line_count -eq 0 ]; then
                    echo "Breaking"
                    break;
                fi
                team_one=$(head -n 1 Games.txt)
                team_two=$(sed -n '2p' Games.txt)
                case "$m" in
                    "n" | "N")
                        rcssserver server::fullstate_l=true server::fullstate_r=true server::auto_mode=true server::synch_mode=$sm server::game_log_dir=$(pwd) server::keepaway_log_dir=$(pwd) server::text_log_dir=$(pwd) server::nr_extra_halfs=2 server::penalty_shoot_outs=false & ;;
                    "y" | "Y")
                        rcssserver server::fullstate_l=false server::fullstate_r=false server::auto_mode=true server::synch_mode=$sm server::game_log_dir=$(pwd) server::keepaway_log_dir=$(pwd) server::text_log_dir=$(pwd) server::nr_extra_halfs=2 server::penalty_shoot_outs=false & ;;
                    *)
                        echo "The command received is incorrect."
                        break;;
                esac
                sleep 1
                server_pid=$!
                sleep 1
                cd Bins/$team_one && ./localStartAll &
                sleep 1
                cd Bins/$team_two && ./localStartAll &
                wait $server_pid
                sleep 1
                tail -n +3 Games.txt > G
                rm -f Games.txt
                mv G Games.txt
                cp *.rc* Analyzer -r
                winner=$(python3 Analyzer/Say_winner.py)
                echo "$winner" >> wins.txt
                echo "Results of the game: $winner"
                rm -f Analyzer/*.rc*
                ./ChangeLogDir.sh
                rm -f *.rcg *.rcl
                sleep 1
            done
            result=$(python3 Analyzer/AnalyzeResult.py)
            echo "$result" > Result.txt
            python3 Analyzer/graph_bar_points.py
            python3 Analyzer/match_graph_with_winners.py

        else
            echo "The command received is incorrect."
        fi;;
    *)
        echo "The command received is incorrect.";;
esac
