#!/bin/bash

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
}

function random_in_range {
	lower=$1
	upper=$2
	KEYSPACE=$(( $upper - $lower - 1))
	n_random_bytes=$3
	if (( $max_random % $upper + 1 == 0 )); then
		random_number=$(od -N${n_random_bytes} -An -i /dev/urandom)
		random_number=$(( $random_number % ${KEYSPACE} + $lower ))
	else
		excess=$(( ($max_random + 1) % ($upper + 1) ))
		max_allowed=$(( $max_random - $excess ))
		echo "n_random_bytes = $n_random_bytes"
		echo "max_random = $max_random"
		echo "excess = $excess"
		echo "max_allowed = $max_allowed"
		while (( 1 )); do
			random_number=$(od -N${n_random_bytes} -An -i /dev/urandom)
			if (( $random_number < $max_allowed )); then
				break
			fi
		done
		random_number=$(( $random_number % ${KEYSPACE} + $lower ))
	fi
}

echo "Enter lower (inclusive) bound:"
read lower
echo "Enter upper (inclusive) bound:"
read upper

echo "The objective is to output pseudorandom numbers in the range ${lower} to ${upper}."
echo "Corrected for modulo bias."

set_n_bytes $lower $upper
random_in_range $lower $upper $n_random_bytes
echo "random_number = $random_number"
