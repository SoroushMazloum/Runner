#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

CONFIG_FILE="config.conf"

if [[ ! -f "$CONFIG_FILE" ]]; then
  echo -e "${RED}Error: Configuration file '$CONFIG_FILE' not found. [ERROR]${NC}"
  exit 1
fi

TYPE=$(grep -E '^type=' "$CONFIG_FILE" | cut -d'=' -f2-)

if [[ -z "$TYPE" ]]; then
  echo -e "${RED}Error: 'type' not found in '$CONFIG_FILE' or its value is empty. [ERROR]${NC}"
  exit 1
fi

TYPE=$(echo "$TYPE" | xargs)

if [[ "$TYPE" == "round_robin" ]]; then
  if [[ -f "Group_tournament.sh" && -x "Group_tournament.sh" ]]; then
    echo -e "${YELLOW}type${NC} : ${GREEN}round_robin${NC}"
    ./Group_tournament.sh
  else
    echo -e "${RED}'Group_tournament.sh' not found or is not executable. [ERROR]${NC}"
    exit 1
  fi
elif [[ "$TYPE" == "stepladder" ]]; then
  if [[ -f "Stepladder_tournament.sh" && -x "Stepladder_tournament.sh" ]]; then
    echo -e "${YELLOW}type${NC} : ${GREEN}stepladder${NC}"
    ./Stepladder_tournament.sh
  else
    echo -e "${RED}'Stepladder_tournament.sh' not found or is not executable. [ERROR]${NC}"
    exit 1
  fi
else
  echo -e "${RED}Unknown type '$TYPE'. [ERROR]${NC}"
  exit 0
fi

