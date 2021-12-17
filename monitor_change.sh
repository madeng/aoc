#!/bin/sh

# Args: 1- the file to monitor
#		2 and + - arguments for the python program to execute

die() {
	echo "$@" >&2
	exit 1
}

get_modified_time() {
	stat "$@" 2>/dev/null | /bin/grep -i modify 2>/dev/null || {
		# Retry once
		sleep 0.5
		stat "$@" 2>/dev/null | /bin/grep -i modify 2>/dev/null
	}
}

[ $# -ge 1 ] || die 'Missing the file to monitor!'

modified_time=$(get_modified_time $1)
last_modified_time="$modified_time"
while :; do
#	echo modified_time="$modified_time"
#	echo last_modified_time="$last_modified_time"
	while [ "$last_modified_time" = "$modified_time" ]; do
		sleep 0.5
		modified_time=$(get_modified_time $1)
	done
	sleep 0.5
	printf '\n\n\n\n\n\n'
	timeout 30 python3 $@
	last_modified_time=$modified_time
done

echo Success!
