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
	KEYSPACE=$(( $upper - $lower + 1))
	n_random_bytes=$3
	if (( $max_random % $upper + 1 == 0 )); then
		random_number=$(od -N${n_random_bytes} -An -i /dev/urandom)
		random_number=$(( $random_number % ${KEYSPACE} + $lower ))
	else
		excess=$(( ($max_random + 1) % ($upper + 1) ))
		max_allowed=$(( $max_random - $excess ))
#		echo "n_random_bytes = $n_random_bytes"
#		echo "max_random = $max_random"
#		echo "excess = $excess"
#		echo "max_allowed = $max_allowed"
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
count6=0
count5=0
count4=0
count3=0
count2=0
count1=0
for i in {1..60000}; do
	random_in_range $lower $upper $n_random_bytes
#	echo "random_number = $random_number"
	[[ $random_number == 6 ]] && let "count6 = count6 + 1"
	[[ $random_number == 5 ]] && let "count5 = count5 + 1"
	[[ $random_number == 4 ]] && let "count4 = count4 + 1"
	[[ $random_number == 3 ]] && let "count3 = count3 + 1"
	[[ $random_number == 2 ]] && let "count2 = count2 + 1"
	[[ $random_number == 1 ]] && let "count1 = count1 + 1"
done

echo "count 6: $count6"
echo "count 5: $count5"
echo "count 4: $count4"
echo "count 3: $count3"
echo "count 2: $count2"
echo "count 1: $count1"
