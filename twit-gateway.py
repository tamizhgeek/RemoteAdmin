import os
import twitter
import logging
import simplejson as json
import time

def init_log():
    
    LOG_FILE_NAME = '/var/log/twit-gateway.log'

    logger = logging.getLogger("twit-gateway")
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.xhandlers.RotatingFileHandler(LOG_FILE_NAME, maxBytes = 2000))
               
    return logger

def get_user_auth_details():

    f = open("authinfo.json")

    auth_dict = json.loads(f.read())

    return auth_dict

def update_auth_dict(auth_dict):

    f = open("authinfo.json","w")

    string = json.dumps(auth_dict)

    f.write(string, indent = 4)
    

def update_direct_messages(log):
    auth_details = get_user_auth_details()
    api = twitter.Api(username=auth_details['auth_dict']['user'], \
                      password=auth_details['auth_dict']['pass'])

    # update the last executed message_id
    last_exec_id = auth_details['last_exec_id'] 

    #get direct messages after that id

    msg_list = api.GetDirectMessages(since_id = int(last_exec_id))

    #reverse the list so that we can execute commands in the order they are received

    msg_list.reverse()
    
    #Iterate thro the messages,check if super word is prefixed - if yes
    #check the sender_id if he is previliged to execute super user command.
    #If no super prefix, just parse the command.
    for msg in msg_list:

        if msg.text.startswith("super:"):

            if msg.sender_id is auth_details['auth_dict']['su-id'] and \
                   msg.sender_screen_name is \
                   auth_details['auth_dict']['su-screen_name']:

                command = msg.text.replace("super:", "").strip()

                passwd = auth_details['auth_dict']['su-pass']

                command_status = os.system("echo "+passwd+" | "+\
                                           "sudo -S "+command)
                last_exec_id = msg.id
                if command_status is 0:
                
                    log.info(command+"Executed successfully!")
                else:

                    log.info(command+"Failed!")
            else:

                print "No super user acess! Command ignored"

        else:

            command = msg.text.strip()
        
            command_status = os.system(command)
            last_exec_id = msg.id
            if command_status is 0:
                
                log.info(command+"Executed successfully!")
            else:

                log.info(command+"Failed!")


    auth_details['last_exec_id'] = last_exec_id
    update_auth_dict(auth_details)



        
if __name__ == "__main__":

    log = init_log

    while(1):

        time.sleep(10)

        update_direct_messages(log)
