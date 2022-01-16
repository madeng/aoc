#!/bin/sh
#DEBUG=1
MOD_FOLDER='build'

if [ -z $DEBUG ]; then
	exec 3>&1 4>&2 >.run.log 2>&1
fi

die() {
	echo $@ >&2
	exit 1
}

[ $# -ge 1 ] || die "Missing folder to execute!"
[ -f $1/main.py ] || die 'There is no main.py in folder: '$1

cp $1/main.py $1/.main.pyx

[ -d $MOD_FOLDER ] || mkdir $MOD_FOLDER

cat >.setup.py <<EOF
from setuptools import setup, Extension
setup(name='$1', ext_modules=[Extension('$MOD_FOLDER.c$1', sources=['$1/.main.pyx'])])
EOF

. venv/bin/activate
python .setup.py build_ext --inplace

RUN_FILE='.run_'$1'.py'
cat >$RUN_FILE <<EOF
import $MOD_FOLDER.$1
EOF

FULL_RUN_FILE_PATH=$(realpath $RUN_FILE)
cd $1
if [ -z $DEBUG ]; then
	# Restore the redirection before executing the python script
	exec >&3 2>&4
fi
python $FULL_RUN_FILE_PATH

