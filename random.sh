#!/bin/bash
#
# Copyright 2020 David Egan
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
# http:#www.apache.org/licenses/LICENSE-2.0
#
# Random Number Within a Specific Range
# -------------------------------------
# To obtain a random number within a particular (inclusive) range within a Bash script:
# * Source this file
# * Run `random_number_in_range <lower bound> <upper bound>`
# * The `$random_number` variable in your calling script will have an appropriate random number
#
# If you run `random_number_in_range` with no parameters, you will be prompted to enter a lower and upper
# value.

# The source of randomness is `/dev/urandom`.
# You can change $RANDOM_SOURCE if necessary.
#
# -----------------------------------------------------------------------------------------------------------
RANDOM_SOURCE="/dev/urandom"

function set_n_bytes {
	lower=$1
	upper=$2
	m=$(($upper - $lower + 1))
	if (( $m < 255 )); then
		n_random_bytes=1
		max_random=255
	elif (( $m > 255 && $m < 65535 )); then
		n_random_bytes=2
		max_random=65535
	elif (( $m > 65535 && $m < 16777215 )); then
		n_random_bytes=3
		max_random=16777215
	elif (( $m >= 16777215 )); then
		echo "Too big for this script"
		exit 1
	fi

	mod=$(( $upper - $lower + 1))
	excess=$(( ($max_random % $mod) + 1 ))
	max_allowed=$(( $max_random - $excess ))
}

function random_in_range {
	if [[ $excess != 0 ]]; then
		while (( 1 )); do
			random_number=$(od -N${n_random_bytes} -An -i ${RANDOM_SOURCE})
			if (( $random_number <= $max_allowed )); then
				break
			fi
		done
	else
		random_number=$(od -N${n_random_bytes} -An -i ${RANDOM_SOURCE})
	fi
	random_number=$(( ($random_number % $mod) + $lower ))
}

function set_inputs {
	if [[ $# -eq 0 ]]; then
		echo "Enter lower (inclusive) bound:"
		read lower
		echo "Enter upper (inclusive) bound:"
		read upper
	else
		lower=$1
		upper=$2
	fi
	set_n_bytes $lower $upper
}


function random_number_in_range {
	set_inputs $1 $2
	random_in_range
}

function test_run {
	. tests
	set_inputs 1 6
	test_diceroll
	set_inputs 1 4
	test_4_sided_diceroll
}

[[ $1 == "test" ]] && test_run
