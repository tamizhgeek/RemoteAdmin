#!/bin/bash

if [ -z $1 ];
then
	echo "Usage - ./start.sh sms (or) ./start.sh twitter"
else
	python $1/console.py
fi
