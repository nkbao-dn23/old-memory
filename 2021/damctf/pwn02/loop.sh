#! /bin/bash

x=1
while [ 1 ]
do
	echo "Take $x times"
	x=$(( $x + 1 ))
	python3 solve.py | grep Congratulations
done