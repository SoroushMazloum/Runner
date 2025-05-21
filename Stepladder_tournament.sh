#!/bin/bash

rm G.txt
chmod +x *.sh

while true
do
    python EditMoment.py
    mv G.txt Games.txt
    rm G.txt
    line_count=$(wc -l < Games.txt)
    if [ $line_count -eq 0 ]; then
        echo Breaking
        break;
    fi
    team_one=$(head -n 1 Games.txt)
    team_two=$(sed -n '2p' Games.txt)

    rcssserver server::fullstate_l = true server::fullstate_r = true server::auto_mode = true server::synch_mode = true server::game_log_dir = `pwd` server::keepaway_log_dir = `pwd` server::text_log_dir = `pwd` server::nr_extra_halfs = 2 server::penalty_shoot_outs = false &
    sleep 1
    server_pid=$!
    sleep 1
    cd Bins/$team_one && ./localStartAll &
    sleep 1
    cd Bins/$team_two && ./localStartAll &
    wait $server_pid
    sleep 1
    sed -i '1,2d' Games.txt
    cp *.rc* Analyzer -r
    winner=$(python Analyzer/Say_winner.py)
    rm Analyzer/*.rc*
    echo "$winner"
    ./LogCompressor.sh
    ./ChangeLogDir.sh
    if [ "$winner" = "NONE" ]
    then
        echo "$team_two" > tmpfile
        cat Games.txt >> tmpfile
        mv tmpfile Games.txt
    else
        echo "$winner" > tmpfile
        cat Games.txt >> tmpfile
        mv tmpfile Games.txt
    fi
    rm *.rcg.tar.gz *.rcl.tar.gz
    sleep 1
done
