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

for(( i=1; i <= $(wc -l < Games.txt); i++)) do
    TEAM=$(sed -n "$i"p Games.txt)
	if [ "$TEAM" = --- ]; then
	    continue
    fi
    i=$((i+1))
    TEAMT=$(sed -n "$i"p Games.txt)
    sed -i '/^\s*$/d' Games.txt
    #edit
    rcssserver server::fullstate_l = $FULLSTATE server::fullstate_r = $FULLSTATE server::auto_mode = true server::synch_mode = $SYNCH_MODE server::game_log_dir = `pwd` server::keepaway_log_dir = `pwd` server::text_log_dir = `pwd` server::nr_extra_halfs = 0 server::penalty_shoot_outs = false &
    sleep 2
    server_pid=$!
    sleep 1
    cd Bins/$TEAM && ./localStartAll >/dev/null 2>&1 &
    sleep 5
    cd Bins/$TEAMT && ./localStartAll >/dev/null 2>&1 &
    wait $server_pid
    sleep 5
    wait $server_pid
    sleep 2
    cp *.rc* Analyzer -r
    python3 Analyzer/get_winner.py
    sleep 1
    rm Analyzer/*.rc*
    ./change_log_dir.sh
    sleep 1
    rm *.rcg *.rcl
done
