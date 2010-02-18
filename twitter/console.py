#!/usr/bin/env python
# twit-gateway.py
# This file can be run as a deamon, so that it listens to the commands sent as
# direct messages to the twitgateway account.
# It executes them, logs them and sends status to throught tweets.
# It can also execute super user commands.


# P.S:Full of crappy code - Feel free to comment and improve
import os
import twitter
import logging
import logging.handlers
import time

import authinfo

def init_log():
    """Method to initialise logger module - refer to python library for better
    explanation on logging module"""
    
    LOG_FILE_NAME = '/var/log/twit-gateway.log'

    logger = logging.getLogger("twit-gateway")
    logger.setLevel(logging.INFO)
    handler = logging.handlers.RotatingFileHandler(LOG_FILE_NAME, maxBytes = 2000)
    logger.addHandler(handler)
               
    return logger


def update_direct_messages(log):
    auth_details = authinfo.auth_dict
    #authenticate with twitter
    api = twitter.Api(username=auth_details['auth_dict']['user'], \
                      password=auth_details['auth_dict']['pass'])

    # get the last executed message_id
    last_exec_id = auth_details['last_exec_id'] 

    #get direct messages after that id

    msg_list = api.GetDirectMessages(since_id = last_exec_id)

    #reverse the list so that we can execute commands in the order they are
    #received

    msg_list.reverse()
    
    #Iterate thro the messages,check if super word is prefixed - if yes
    #check the sender_id if he is previliged to execute super user command.
    #If no super prefix, just parse the command.
    for msg in msg_list:

        if msg.text.startswith("super:"):

            if msg.sender_id == auth_details['auth_dict']['su-id']:

                command = msg.text.replace("super:", "").strip()

                passwd = auth_details['auth_dict']['su-pass']
                
                command_status = os.system("echo "+passwd+" | "+\
                                           "sudo -S "+command)
                # Change the last executed msg id to recently executed msg id
               
                if command_status is 0:
                    # log the executed command and also tweet the status
                    log.info(command+" Executed successfully!")
                    api.PostUpdate(command+" success!")
                else:
                    log.info(command+" Failed!")
                    api.PostUpdate(command+" fail!")
            else:

                print "No super user acess! Command ignored"
               

        else:

            command = msg.text.strip()
        
            command_status = os.system(command)
           

            if command_status is 0:
                api.PostUpdate(command+" success!")
                log.info(command+" Executed successfully!")
            else:
                api.PostUpdate(command+" fail!")
                log.info(command+" Failed!")

        last_exec_id = msg.id

    authinfo.auth_dict['last_exec_id'] = last_exec_id



        
if __name__ == "__main__":

    log = init_log()
    while(1):

       update_direct_messages(log)

       time.sleep(10)
        
