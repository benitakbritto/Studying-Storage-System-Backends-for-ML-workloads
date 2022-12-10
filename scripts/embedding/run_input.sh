#!/bin/sh
BLUE='\033[0;44m'
NOCOLOR='\033[0m'

echo "${BLUE} Text[zipf] ${NOCOLOR}"
chmod 777 make_output_folders.sh
./make_output_folders.sh
echo "${BLUE} Completed ${NOCOLOR}"

echo "${BLUE} Text[zipf] ${NOCOLOR}"
chmod 777 text.sh
./text.sh
echo "${BLUE} Completed ${NOCOLOR}"

echo "${BLUE} Graph[power] ${NOCOLOR}"
chmod 777 graph.sh
./graph.sh
echo "${BLUE} Completed ${NOCOLOR}"