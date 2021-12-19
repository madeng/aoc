#!/bin/sh
# $1: the file or folder to monitor
# $2: the script to execute when the file/folder changes
#
# If only one argument is received, it will be used as the script to execute and
# the folder in which the script is located will be monitored

get_folder_of() {
	file_path=$1
	# File path
	fn=${fn:-$(readlink -f "$file_path" 2>/dev/null)}
	# Dir name
	echo ${fn%/*}
}

die() {
	echo $@ >&2
	exit 1
}

test_only=false
end_of_opts=false
while [ $end_of_opts = false ]; do
	case $1 in
		-t|--test)
			test_only=true
			shift
			;;
		--)
			end_of_opts=true
			shift
			;;
		-*)
			die 'Unknown option: '$1
			;;
		*)
			end_of_opts=true
			;;
	esac
done

[ $# -ne 0 ] || die "Not enough args!"

mon_files=
script=
if [ $# -eq 1 ]; then
	if [ -d $1 ]; then
		mon_files=$1/*
	elif [ -f $1 ]; then
		mon_files=${1%/*}/*
	fi
	script=$1
elif [ $# -eq 2 ]; then
	if [ -f $1 ]; then
		mon_files=$1
	elif [ -d $1 ]; then
		mon_files=$1/*
	fi
	script=$2
else
	die 'Too many args. Expected max 2.'
fi
[ -n "$mon_files" ] || die 'Error: no files to monitor.'

[ $test_only = false ] || runpy_opts="${runpy_opts:+$runpy_opts }-t"

# Keep monitoring the files until end of world or until a signal is received
echo $mon_files | tr ' ' '\n' | entr -c $(get_folder_of $0)/runpy.sh $runpy_opts $script
