#!/usr/bin/python

#	before running this program you must configured gnokii-smsd and it must be up and running
# 	@Author:	Karthik selvakumar
#	Name : 	Dictionary Server

# install python-MySQLdb  before importing this module

import MySQLdb

# imported inorder to perform shell operations

import os

processed=1;
# run as a daemon and never exit this thread 
while(True):

#defines the database parameter change according to your configuration

	host="localhost"

	user="root"

	passwd="rajesh11"

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

#performs pruning of inbox table which may contain null entities

	cursor.execute("delete from inbox where text=\"\"")

#gets the latest entered SMS from Mysql server

	cursor.execute(" select number,text,id,processed from inbox where id=(select max(id) from inbox)")

	record=cursor.fetchall()

	for result in record:

# gets the word to find meaning

		word=result[1]

# get the number bcoz u have to reply the meaning to this number later ;)

		number=result[0]

		row=result[2]
		
		processed=result[3]


	if(processed==0):

# script to get meaning of a word from google server
		os.system(">meaning.txt")
		if(word=="lock"):
			up="gnome-screensaver-command --lock";
		elif(word=="unlock"):
			up="xset dpms force on && gnome-screensaver-command -d";

		elif(word.startswith("status:")):
			up=" purple-remote \"setstatus?status=available&message="+str(word.replace("status:",""))+"\"";
		elif(word.startswith("text:")):
			up="echo "+str(word.replace("text:",""))+" > text";

		else: 
			up=word+" >meaning.txt";

		print up;

#set the entity to be processed when taken out

		cursor.execute(" update inbox  set processed=1 where id="+str(row));

# run the command in shell and write it to file named meaning.txt

		os.system(up)

# open the file in read only mode

		filehandle=open('meaning.txt','r')

# load the meaning in the string text

		text=filehandle.read()


		print " text is "+text

# we no more need this 

		filehandle.close()


		if(text!=""):
			cursor.execute("insert into outbox(number,text) values(%s,%s)",(number,text))



# close all active connections :)

	cursor.close()

	db.close()

#thank you !


