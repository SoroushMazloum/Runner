#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

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

chmod +x *
rcssmonitor --auto-reconnect-mode on --auto-reconnect-wait 4 &

for(( i=1; i <= $(wc -l < Games_test.txt); i++)) do
    TEAM=$(sed -n "$i"p Games_test.txt)
	if [ "$TEAM" = --- ]; then
	    continue
    fi
    TEAMT=$(sed -n "$i"p Games_test.txt)
    TEAMT="helios"
    sed -i '/^\s*$/d' Games_test.txt

    rcssserver server::fullstate_l = $FULLSTATE server::fullstate_r = $FULLSTATE server::auto_mode = true server::synch_mode = $SYNCH_MODE server::game_log_dir = `pwd` server::keepaway_log_dir = `pwd` server::text_log_dir = `pwd` server::nr_extra_halfs = 0 server::penalty_shoot_outs = false server::nr_normal_halfs = 1 server::nr_extra_halfs = 0 server::half_time = 30 &
    sleep 0.5
    server_pid=$!
    sleep 1
    cd Bins/$TEAM && ./localStartAll >/dev/null 2>&1 &
    sleep 5
    cd Bins/$TEAMT && ./localStartAll >/dev/null 2>&1 &
    wait $server_pid
    sleep 0.5
    ./change_log_dir.sh
    sleep 15
    rm *.rcg *.rcl
    echo -e "${RED}=======================================================================${NC}"
done
