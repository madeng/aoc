#!/bin/sh -u
#
# Args: 1- the python script file to monitor. If a folder is received, this
# script will look for all .py file in the folder and execute them all.
#

get_folder_of() {
	file_path=$1
	# File path
	fn=${fn:-$(readlink -f "$file_path" 2>/dev/null)}
	# Dir name
	echo ${fn%/*}
}

die() {
	echo "$@" >&2
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

[ $# -ge 1 ] || die 'Missing the file to monitor!'

script_file_list=$1
if [ -d $script_file_list ]; then
	script_folder=${script_file_list%/}
	script_file_list=$(echo $script_file_list/*.py)
elif [ -f $script_file_list ]; then
	script_folder=$(get_folder_of $script_file_list)
	script_file_list=${script_file_list##*/}
fi
shift

#echo current script path: $script_file_list
#echo current script folder: $script_folder

cd $script_folder

input_file_list="$(echo testinput* tin*)"
[ $test_only = true ] || input_file_list="input in $input_file_list"

stop_it=false
for script_file in $script_file_list; do
	for input_file in $input_file_list; do
		[ -f $input_file ] || continue
		input_file_name=$(echo $input_file|rev|cut -d'/' -f-3 |rev)
		script_file_name=${script_file#$script_folder/}
		printf "\n---py3 $script_file_name ($input_file_name)---\n"
		python3 $script_file_name $input_file || {
			stop_it=true
		}
		[ $stop_it = false ] || break
	done
	[ $stop_it = false ] || break
done

