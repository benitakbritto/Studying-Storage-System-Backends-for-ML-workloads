#!/bin/sh
BLUE='\033[0;44m'
NOCOLOR='\033[0m'

echo "${BLUE} Text - Map Style ${NOCOLOR}"
text/map_style.sh
echo "${BLUE} Completed ${NOCOLOR}"

echo "${BLUE} Text - Iterable Style ${NOCOLOR}"
text/iterable_style.sh
echo "${BLUE} Completed ${NOCOLOR}"

echo "${BLUE} Image - Map Style ${NOCOLOR}"
image/map_style.sh
echo "${BLUE} Completed ${NOCOLOR}"

echo "${BLUE} Image - Iterable Style ${NOCOLOR}"
image/iterable_style.sh
echo "${BLUE} Completed ${NOCOLOR}"

echo "${BLUE} Graph - Map Style ${NOCOLOR}"
graph/map_style.sh
echo "${BLUE} Completed ${NOCOLOR}"

echo "${BLUE} Graph - Iterable Style ${NOCOLOR}"
graph/iterable_style.sh
echo "${BLUE} Completed ${NOCOLOR}"