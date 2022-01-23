#!/bin/sh -e
#DEBUG=1
MOD_FOLDER='build'

redirect() {
	if [ -z $DEBUG ]; then
		exec 3>&1 4>&2 >.run.log 2>&1
	fi
}

# Return 0 if there was redirection, 1 otherwise
stop_redirect() {
	if [ -z $DEBUG ]; then
		# Restore the redirection before executing the python script
		exec >&3 2>&4
		return 0
	fi
	return 1
}

compile() {
	MAIN_PYX=$1/.main.pyx
	cp $1/main.py $MAIN_PYX

	sed -i '1 s/^/# cython: language_level=3\n/' $MAIN_PYX

	[ -d $MOD_FOLDER ] || mkdir $MOD_FOLDER

	cat >.setup.py <<-EOF
	from setuptools import setup, Extension
	setup(name='$1', ext_modules=[Extension('$MOD_FOLDER.c$1', sources=['$MAIN_PYX'])])
	EOF

	. venv/bin/activate
	python .setup.py build_ext --inplace || return 1

	RUN_FILE='.run_'$1'.py'
	cat >$RUN_FILE <<-EOF
	import $MOD_FOLDER.c$1
	EOF

	RUN_FILE_PATH=$(realpath $RUN_FILE)
}

die() {
	echo $@ >&2
	exit 1
}

[ -f $1/main.py ] || die 'There is no main.py in folder: '$1

redirect

compile $1 || {
	echo stopping redirect..
	stop_redirect && python .setup.py build_ext --inplace
}

stop_redirect

# Pass all the other arguments of the script to the actual python script
shift
python $RUN_FILE_PATH $@

