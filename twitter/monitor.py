# Very immature code - Nothing will work!

import twitter
import commands
import time
import os
import sys

import authinfo

def temp_monitor():
    """This method checks the CPU temp and tweets it periodically!"""

    hardware = 0

    if os.path.exists("/sys/devices/LNXSYSTM:00/LNXTHERM:00/LNXTHERM:01/thermal_zone/temp") == True:
        hardware = 4
		
    if os.path.exists("/proc/acpi/thermal_zone/THM0/temperature") == True:
        hardware = 1
    
    if os.path.exists("/proc/acpi/thermal_zone/THRM/temperature") == True:
        hardware = 2

    if os.path.exists("/proc/acpi/thermal_zone/THR1/temperature") == True:
        hardware = 3
        
    if hardware == 0 :
        print "Sorry, your hardware is not yet supported."
        sys.exit()

    while True:
        
        if hardware == 1 :
            temp = open("/proc/acpi/thermal_zone/THM0/temperature").read().strip().lstrip('temperature :').rstrip(' C')
        if hardware == 2 :
            temp = open("/proc/acpi/thermal_zone/THRM/temperature").read().strip().lstrip('temperature :').rstrip(' C')
        if hardware == 3 :
            temp = open("/proc/acpi/thermal_zone/THR1/temperature").read().strip().lstrip('temperature :').rstrip(' C')
        if hardware == 4 :
            temp = open("/sys/devices/LNXSYSTM:00/LNXTHERM:00/LNXTHERM:01/thermal_zone/temp").read().strip().rstrip('000')

        auth_info = authinfo.auth_dict

        api = twitter.Api(username=auth_info['auth_dict']['user'], \
                      password=auth_info['auth_dict']['pass'])

        
        api.PostUpdate("The CPU temperature is currently at "+temp +" Celsius")

        time.sleep(5000)




if __name__=="__main__":

    
    temp_monitor()
        
