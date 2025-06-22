#!/bin/bash

RED='\e[31m'
NC='\e[0m'

CONFIG_FILE="config.conf"

if [ ! -f "$CONFIG_FILE" ]; then
    echo -e "${RED}Configuration file '$CONFIG_FILE' not found. [ERROR]${NC}"
    exit 1
fi

FULLSTATE=$(grep "^fullstate=" "$CONFIG_FILE" | cut -d'=' -f2)

if [ -z "$FULLSTATE" ]; then
    echo -e "${RED}'fullstate' not found or empty in $CONFIG_FILE. [ERROR]${NC}"
    exit 1
fi

SYNCH_MODE=$(grep "^synch_mode=" "$CONFIG_FILE" | cut -d'=' -f2)

if [ -z "$SYNCH_MODE" ]; then
    echo -e "${RED}'synch_mode' not found or empty in $CONFIG_FILE. [ERROR]${nc}"
    exit 1
fi

chmod +x *.sh

while true
do
    #sed -i '/^\s*$/d' Games.txt
    sed -i -e '/./,$!d' -e :a -e '/^\s*$/{$d;N;ba' -e '}' Games.txt
    line_count=$(grep -c . < Games.txt)
    if [ $line_count -eq 1 ]; then
        echo Breaking
        break;
    fi
    team_one=$(head -n 1 Games.txt)
    team_two=$(sed -n '2p' Games.txt)

    rcssserver server::fullstate_l = $FULLSTATE server::fullstate_r = $FULLSTATE server::auto_mode = true server::synch_mode = $SYNCH_MODE server::game_log_dir = `pwd` server::keepaway_log_dir = `pwd` server::text_log_dir = `pwd` server::nr_extra_halfs = 2 server::penalty_shoot_outs = false &
    sleep 2
    server_pid=$!
    sleep 1
    cd Bins/$team_one && ./localStartAll >/dev/null 2>&1 &
    sleep 5
    cd Bins/$team_two && ./localStartAll >/dev/null 2>&1 &
    wait $server_pid
    sleep 5
    wait $server_pid
    sleep 2
    sed -i '1,2d' Games.txt
    cp *.rc* Analyzer -r
    winner=$(python3 Analyzer/get_winner.py)
    sleep 1
    rm Analyzer/*.rc*
    echo "$winner"
    ./change_log_dir.sh
    sleep 1
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
    sleep 1
    rm *.rcg *.rcl
done
