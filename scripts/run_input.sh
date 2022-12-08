#!/bin/sh
BLUE='\033[0;44m'
NOCOLOR='\033[0m'

echo "${BLUE} Text - Map Style ${NOCOLOR}"
chmod 777 text/map_style.sh
text/map_style.sh
echo "${BLUE} Completed ${NOCOLOR}"

echo "${BLUE} Text - Iterable Style ${NOCOLOR}"
chmod 777 text/iterable_style.sh
text/iterable_style.sh
echo "${BLUE} Completed ${NOCOLOR}"

echo "${BLUE} Image - Map Style ${NOCOLOR}"
chmod 777 image/map_style.sh
image/map_style.sh
echo "${BLUE} Completed ${NOCOLOR}"

echo "${BLUE} Image - Iterable Style ${NOCOLOR}"
chmod 777 image/iterable_style.sh
image/iterable_style.sh
echo "${BLUE} Completed ${NOCOLOR}"

echo "${BLUE} Graph - Map Style ${NOCOLOR}"
chmod 777 graph/map_style.sh
graph/map_style.sh
echo "${BLUE} Completed ${NOCOLOR}"

echo "${BLUE} Graph - Iterable Style ${NOCOLOR}"
chmod 777 graph/iterable_style.sh
graph/iterable_style.sh
echo "${BLUE} Completed ${NOCOLOR}"