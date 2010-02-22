#!/usr/bin/python

#	before running this program you must configured gnokii-smsd and it must be up and running
# 	@Author:	Karthik selvakumar
#	Name : 	Battery Status Messager

# install python-MySQLdb  before importing this module

import MySQLdb

# imported inorder to perform shell operations

import os

# imported inorder make delay between SMS

import time

# Get Configuration



print " Enter the Phone Number to alert :"
	
number=raw_input()

print " Enter delay of alerts :"

delay=float(raw_input())



# run as a daemon and never exit this thread 

while(True):

#defines the database parameter change according to your configuration

	host="localhost"

	user="root"

	passwd="cse25"

	db="smsgw"

# Optionally get input from user

#	print " Enter Host :" 

#	host=raw_input()

#	print " Enter Password :"

#	passwd=raw_input()

#	print " Enter database :"

#	db=raw_input()


	


#creates a database object for corresponding config

	db=MySQLdb.connect(host,user,passwd,db)

	cursor=db.cursor()
	
	up="acpi > acpi.log"

# run the command in shell and write it to file named meaning.txt

	os.system(up)

# open the file in read only mode

	filehandle=open('acpi.log','r')

# load the meaning in the string text

	dummy=filehandle.readline()
	text=dummy
		
	print " text is "+text;

# we no more need this 

	filehandle.close()

	cursor.execute("insert into outbox(number,text) values(%s,%s)",(number,text))

	
# Delay between next ALERT

	time.sleep(delay)

	
# close all active connections :)

	cursor.close()

	db.close()

#thank you !

