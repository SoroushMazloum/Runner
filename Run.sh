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
./rename.sh

trap 'rm -f *.rcg *.rcl Analyzer/*.rc*' EXIT

rm -f wins.txt Results.txt LogsConf/*.conf LogsJSON/*.json Logs/*.rc* Analysis_Results/*.png

echo "Major ? (n/y): "
read m
echo "synch_mode ? (false/true): "
read sm

echo "Select tournament mode:"
echo "1) Normal (Round-Robin)"
echo "2) Elimination (Winner-Stays)"
read -p "Your choice (1 or 2): " mode

case "$m" in
    "n" | "N" | "y" | "Y")
        if [[ "$sm" == "true" || "$sm" == "false" ]]; then
            echo "Start a Tournament Runner ..."
            rcssmonitor --auto-reconnect-mode on --auto-reconnect-wait 2 &
            chmod +x *.sh

            while true
            do
                sed -i '/^\s*$/d' Games.txt
		        sed -i -e '$a\\' Games.txt

                line_count=$(wc -l < Games.txt)
                if [ "$line_count" -lt 2 ]; then
                    break
                fi

                team_one=$(head -n 1 Games.txt)
                team_two=$(sed -n '2p' Games.txt)

                case "$m" in
                    "n" | "N")
                        if [ "$mode" = "1" ]; then
                            rcssserver server::fullstate_l=true server::fullstate_r=true server::auto_mode=true server::synch_mode=$sm server::game_log_dir=$(pwd) server::keepaway_log_dir=$(pwd) server::text_log_dir=$(pwd) server::nr_extra_halfs=0 server::penalty_shoot_outs=false &
                        elif [ "$mode" = "2" ]; then
                            rcssserver server::fullstate_l=true server::fullstate_r=true server::auto_mode=true server::synch_mode=$sm server::game_log_dir=$(pwd) server::keepaway_log_dir=$(pwd) server::text_log_dir=$(pwd) server::nr_extra_halfs=2 server::penalty_shoot_outs=true &
                        else
                            echo "Unknown mode selected."
                            break
                        fi ;;

                    "y" | "Y")
                        if [ "$mode" = "1" ]; then
                            rcssserver server::fullstate_l=false server::fullstate_r=false server::auto_mode=true server::synch_mode=$sm server::game_log_dir=$(pwd) server::keepaway_log_dir=$(pwd) server::text_log_dir=$(pwd) server::nr_extra_halfs=0 server::penalty_shoot_outs=false &
                        elif [ "$mode" = "2" ]; then
                            rcssserver server::fullstate_l=false server::fullstate_r=false server::auto_mode=true server::synch_mode=$sm server::game_log_dir=$(pwd) server::keepaway_log_dir=$(pwd) server::text_log_dir=$(pwd) server::nr_extra_halfs=2 server::penalty_shoot_outs=true &
                        else
                            echo "Unknown mode selected."
                            break
                        fi ;;
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

                cp *.rc* Analyzer -r
                full_result=$(python3 Analyzer/Say_winner.py)
                winner=$(echo "$full_result" | awk -F '->' '{print $2}' | xargs)
                echo "$full_result" >> wins.txt
                echo "Result of the game: $full_result"

                rm -f Analyzer/*.rc*
                ./ChangeLogDir.sh
                rm -f *.rcg *.rcl
                sleep 1

                if [ "$mode" = "1" ]; then
                    tail -n +3 Games.txt > G
                    mv G Games.txt

                elif [ "$mode" = "2" ]; then
                    tail -n +3 Games.txt > rest
                    echo "$winner" > Games.txt
                    cat rest >> Games.txt
                    rm -f rest

                    new_line_count=$(wc -l < Games.txt)
                    if [ "$new_line_count" -eq 1 ]; then
                        echo "\n The tournament is over! The final winner: $(head -n 1 Games.txt)"
                        break
                    fi
                else
                    echo "Unknown mode selected."
                    break
                fi
            done

            python3 Analyzer/AnalyzeResult.py > Result.txt
            python3 Analyzer/graph_bar_points.py
            python3 Analyzer/match_graph_with_winners.py
	        ./install_Analayzer.sh
	        ./convert_logs.sh
	        ./generate_reports.sh

        else
            echo "The synch_mode value must be 'true' or 'false'."
        fi ;;
    *)
        echo "The command received is incorrect." ;;
esac
