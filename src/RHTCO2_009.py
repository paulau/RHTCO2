#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#ssid CO2-Ampel
#pass aaaaaaaa

#apt-get install libapache2-mod-auth-mysql phpmyadmin
# Request works:
# http://192.168.10.2/sqlwrapper.php?len=1


# Version 009 is remake of Version 008 with OOP approach to Logger Scripts. 

# additionally. extension txt -> std (sensor text data) replaced. to avoit too many txt files
# in system. readme.txt is also file. So let us use more specific type for the
# logging of data

# additionally, settingsRHTCO2_009.py is needed parameter FAST is added 
# if FAST then system will not Save into files or into usual Datenerfassung.RHTCO2
# it will store into FAST table instead. 


# HYT functionality commented - disabled

# Version 008  uses Datenbank um die Namen von Dateien zu speichern für upload script. 
# upload wird entsprechend die Dateien hochladen und die Name von Datenbank entfernen. 
# Dadurch fällt die notwendigkeit von current_ oder u_ prefixes.

# settings Datei ist umbenant mit suffix _008

# usage eg  from rc.local
# sudo python /home/pi/RHTCO2/RHTCO2_009.py /home/pi/RHTCO2/ 1>  /home/pi/RHTCO2/tmp_logger_out.txt 2> /home/pi/RHTCO2/tmp_logger_err.txt &


import time, sys, os, datetime
from classRHTCO2 import *  # RHTCO2 logger (controller) class

import signal # to process kill signal and exit correctly


logger = RHTCO2() # must be all initialized

# tricky. how to pass argument to termination handler? does global work?
def signal_term_handler(signal, frame):  # correct finish work after kill -15 or after ctrl+C
	print("got SIGTERM")
	logger.CleanandExit()

# catch sigterm (kill -15) to terminate process properly
signal.signal(signal.SIGTERM, signal_term_handler)

PrevSaveTime = logger.StartTime

while True:
    try:
        t1 = datetime.datetime.today()
        logger.GetData() 
        logger.SaveData()        
        logger.Control()
       
        Prevtm = int(PrevSaveTime.strftime(logger.SwitchOutputFileInterval))
        tm = int(logger.ReadTime.strftime(logger.SwitchOutputFileInterval))
        PrevSaveTime = logger.ReadTime
       
        if (Prevtm!=tm): # new file
            logger.SwitchOutputFile() 

        t2 = datetime.datetime.today()

        dt = t2 - t1
        fdt  = dt.seconds + dt.microseconds / 1000000.0
        waittime = logger.P.LoggingRate*1.0 - fdt
                
        if (waittime>0):
            time.sleep(waittime) # sleep always logging rate.

    except KeyboardInterrupt:
        print("Keyboard Interrapt main script")
        logger.CleanandExit()
#    except SystemExit:	 # what  is it seems needed for Ctrl+C
#        print("system exit main script")
#        logger.CleanandExit()
    except:		
        # if all other exception are thrown then just pass 				
        print("main code loop unknown exception")
        pass
		
##=======================================================================
