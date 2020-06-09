#!/bin/bash

THIS=$(readlink -f ${BASH_SOURCE[0]})
PROJECT_ROOT=$(dirname $THIS)
. "${PROJECT_ROOT}"/random.sh
. "${PROJECT_ROOT}"/tests

# Outputs pseudo random values in a user-selected range
function main {
	echo "How many variables to return?"
	read runs
	set_inputs
	manual_test
}

main
