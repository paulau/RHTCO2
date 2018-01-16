#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# logger (controller) class for RT T CO2 logging CO2 Ampel controlling
# K-30, DHT22 or HYT sensors are available


import imp, sys, os, time, datetime
from notsmb import notSMB
import Adafruit_DHT as dht

import RPi.GPIO as GPIO

from commonloggerfunctions import renamecurrents  # common logger functions

# import only if SQL variables are defined.
#if (hasattr(self.P, 'SQLuser')):
from SQLsend import SQLsend
# attention! must be installed!!!
# apt-get install python-mysqldb
from SQLsendFName import SQLsendFName
import MySQLdb

class RHTCO2():
    # constructor. Initialise things  (allocate memory)
    def __init__(self): 
        if (len(sys.argv)==2):
            self.opath  = sys.argv[1]	
        else:
            self.opath = os.getcwd() + "/"

        
        renamecurrents(self.opath)  # rename possibly earlier stored current files. 
                    
        settingsfname = "settingsRHTCO2_009.py"
        settingsfname = self.opath + settingsfname 
        self.P = imp.load_source('settings', settingsfname) # read Parameters


        self.fileextension = ".std" # ".txt" # std (sensor text data) 10.01.2018

        self.StartTime = datetime.datetime.today() # need ot only once 
        self.fname  = self.P.fileprefix + self.StartTime.strftime("%Y_%m_%d_%H_%M") + self.fileextension 
        print (self.fname)
	
        if (hasattr(self.P, 'CO2_ADDR')):
            self.CO2_ADDR = self.P.CO2_ADDR
        else:
            self.CO2_ADDR = 0x68
        
        self.bus = notSMB(1) # 1 for standard i2c bus of raspberry pi B         
        
        # This is actually part needed to control initialisation:
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        
        # switch on Voltage:
        GPIO.setup(self.P.GPIOVoltagePin, GPIO.OUT, pull_up_down=GPIO.PUD_OFF)
        GPIO.output(self.P.GPIOVoltagePin, GPIO.HIGH) # switch on sensor

        # ------------- if control setting is defined in settings file, --------
        # ------------------------- then use it! -------------------------------
        if (hasattr(self.P, 'SignalControlPin')):
            #print("SignalControlPin is initialized")
            GPIO.setup(self.P.SignalControlPin, GPIO.OUT, pull_up_down=GPIO.PUD_OFF)
            if (not hasattr(self.P, 'CO2Limit')):
                self.CO2Limit = 1200
            else: 
                self.CO2Limit = self.P.CO2Limit	

# note, that SQLuser must be defined here
        # Fast Output 
        if (hasattr(self.P, 'FAST')):            
            self.FAST = self.P.FAST             
        else:
            self.FAST = False 

        # enough to do once:
        if (hasattr(self.P, 'SaveInterval')):
            self.SwitchOutputFileInterval = self.P.SaveInterval   #%M  %H
        else: # save each Hour if nothing is specified.
            self.SwitchOutputFileInterval = "%H"   #%M  %H



        if (self.FAST): # do it only for not FAST regime
            
            self.SQLFASTini()
        else: 
            if (hasattr(self.P, 'uploadstable')): # if defined uploadstable, the use it instead of 
                							 # prefixes of files to set information about files
                # import necessary function, if parameter is defined                
                self.f = open(self.opath + self.fname, 'a')
            else:
                self.f = open(self.opath + "current_" + self.fname, 'a')


    def GetData(self): 
        # ================================================================
        ## get value of CO2. First do it as direct code here. 
        ## later one can organize it as function or method of class.
        
        self.co2Val = None  # before start getting this variable clean it
        self.h = None  # before start getting this variable clean it
        self.t = None  # before start getting this variable clean it
        
        while ((self.co2Val==None)|(self.h==None)|(self.t==None)): # try to get it until success
            try:
		    	# several attempts may be needed to read this sensor 
		    	# TRICKY SENSOR
                sum=-1 #Checksum
                while (sum!=0):
                    resp = self.bus.i2c(self.CO2_ADDR,[0x22,0x00,0x08,0x2A],4) 
                    time.sleep(0.1) # important to reduce frequency of error in checksum
                    a = resp[0] + resp[1] + resp[2]
                    if (a>255):
		        	    a = a - 256
                    # while resp[3] is not more than byte
                    # one needs to check chechsumm within one byte range
                    sum=a-resp[3]  # check summ must be zero

                #checksum simply MUST be zero here!
                #Checksum failure can be due to a number of factors,
                #fuzzy electrons, sensor busy, etc.

                self.co2Val = (resp[1]*256) + resp[2]                    
                
                self.h, self.t = dht.read_retry(dht.DHT22, self.P.DHTDataPin)
                # can be rather slow !!! use HYT!!!
                #self.h = 0.0
                #self.t = 0.0
                
                # ================================================================
       
        
#        		# ================================================================
#        		# if fedined address of HYT sensor then read it!!! 
#        		# if it is supposed to operate withut HYT, then comment it in 
#        		# settingsRHTCO2.py file
#        
##                if (hasattr(self.P, 'HYT271address')):
##                    resp = self.bus.i2c(self.P.HYT271address,[],0) # Init HYT 221 for reading, ignore answer
##                    resp = self.bus.i2c(self.P.HYT271address,[] , 4) # # Read 4 bytes (even more) of data from HYT221
##                    # Now we have all data from sensor in the first 4 bytes of 'resp' Look for 
##                    # HYT221 doc to see how to extract temperature and humidity from bytes
##                    
##                    ##Calc humidity in rel.%
##                    hum = resp[0]<<8 | resp[1]
##                    hum = hum & 0x3FFF
##                    self.H = 100.0*hum/(2**14)
##                    
##                    # Calc temperature in °C
##                    resp[3] = resp[3] & 0x3F
##                    temp = resp[2] << 6 | resp[3]
##                    self.T = 165.0*temp/(2**14)-40
##
                self.ReadTime = datetime.datetime.today()    
#                print(self.co2Val, " ", self.ReadTime)
            except:
                self.co2Val = None  # in case of exception clean it 
                self.h = None
                self.t = None                
                #self.H = None
                #self.T = None                
                pass

        
    
# ATTENTION !!! IT MUST BE CALLED ONLY AFTER GET DATA!!!!
    # SaveData function. 
    def SaveData(self): 
        if (self.FAST):
            SQLsend(self.P.SQLserver, self.P.SQLuser, self.P.SQLpw, "FAST", self.ReadTime, self.h, self.t, self.co2Val)
            # self.SQLcleanFAST() to finish # must check table size
            
            
        else:	
            #  try to add data to mySQL server. if not do logging further.
            try:
                if (hasattr(self.P, 'SQLuser')):
                    SQLsend(self.P.SQLserver, self.P.SQLuser, self.P.SQLpw, self.P.tabelle, self.ReadTime, self.h, self.t, self.co2Val)
            except:
                pass
		    
            # compose string to output into file
            OString = self.ReadTime.strftime("%d.%m.%Y %H:%M:%S") 
            OString = OString + "	" + "{:.2f}".format(self.h) + "	" + "{:.2f}".format(self.t)  
            OString = OString + "	" + str(self.co2Val)
            #if (hasattr(self.P, 'HYT271address')):
            #    OString = OString + "	" + "{:.2f}".format(H) + "	" + "{:.2f}".format(T)
		    
            # ================================================================
            OString = OString + "\n"
            self.f.write(OString)
            self.f.flush()
        
    # we save data to new file each day, hour ... depending on parameter 
    # P.SaveInterval or  SwitchOutputFileInterval   
    #%M  %H
    def SwitchOutputFile(self):
        if (not self.FAST): # do it only for not FAST regime
            self.f.close()
            time.sleep(3) 
            # 3.05.2016
            # close function needs time apparently, so that next operation
            # mv does not succeed sometimes. apparently if many files are already stored in directory
            # we make therefore couple of seconds delay after close(). once for each saved file (normally each hour)
            
            
            # 07.01.2018:
            if (hasattr(self.P, 'uploadstable')):# if defined uploadstable, the use it instead of 
    											 # prefixes of files to set information about files
    				
                # just create new file without any current_ prefixes
                # instead send record with filename into uploadstable
                
                try:
                    SQLsendFName(self.P.SQLserver, self.P.SQLuser, self.P.SQLpw, 'uploads', self.opath + self.fname, self.P.ftpbenutzer, self.P.ftppasswort, self.P.FTPfolder)
                except:
                    pass
    
                self.fname  = self.P.fileprefix + self.ReadTime.strftime("%Y_%m_%d_%H_%M") + self.fileextension
                self.f = open(self.opath + self.fname, 'w')								 
    
            else:
                # we need to handle files if uploadstable is not defined
                # here fname is just fname of just closed file
                commandtodo = "mv " + self.opath + "current_" + self.fname + " " + self.opath + self.fname
                os.system(commandtodo)
                
                
                # 20.01.2017
                # delay does not help, current_ files are not renamed after some time anymore again
                # to recover, we insert:
                #renamecurrents(self.opath) # rename possibly earlier stored current files. 
                # 10.01.2018 commented, since it does not help
                # does it help?
                #------------------------------------------------------------
                self.fname  = self.P.fileprefix + self.ReadTime.strftime("%Y_%m_%d_%H_%M") + self.fileextension # _%M
                self.f = open(self.opath + "current_" + self.fname, 'w')

# ATTENTION !!! IT MUST BE CALLED ONLY AFTER GET DATA!!!!
    def Control(self):
        if (hasattr(self.P, 'SignalControlPin')):
            if (self.co2Val>self.CO2Limit): 
                GPIO.output(self.P.SignalControlPin, GPIO.HIGH) 
            else:
                GPIO.output(self.P.SignalControlPin, GPIO.LOW)  # test, how it works

    # The FAST table will be refreshed after each start of script
    def SQLFASTini(self):
        try :
            con = MySQLdb.connect(self.P.SQLserver,self.P.SQLuser,self.P.SQLpw,"Datenerfassung")			
            cur = con.cursor()
            command = "DROP TABLE IF EXISTS Datenerfassung.FAST;"
            cur.execute(command)		
            cur.close()
            con.commit()
        except:
            pass    
        try :			
            con = MySQLdb.connect(self.P.SQLserver,self.P.SQLuser,self.P.SQLpw,"Datenerfassung")    
            cur = con.cursor()
            command = "CREATE TABLE IF NOT EXISTS Datenerfassung.FAST(Id INT PRIMARY KEY AUTO_INCREMENT, Datum date, Zeit time, RH float, T float, CO2 smallint);"
            cur.execute(command)		
            cur.close()
            con.commit()
        except:
            pass    

    def SQLcleanFAST(self):
        con = MySQLdb.connect(self.P.SQLserver,self.P.SQLuser,self.P.SQLpw,"Datenerfassung")
        cur = con.cursor()
        command = "DELETE FROM Datenerfassung.FAST LIMIT 1;"
        cur.execute(command)		
        cur.close()
        con.commit()
		


    def CleanandExit(self):
        if (not self.FAST): # do it only for not FAST regime
            self.f.close()
            print("file closed")

            # also last file must be send to main server. 
            # 07.01.2018:
            if (hasattr(self.P, 'uploadstable')):# if defined uploadstable, the use it instead of 
            								 # prefixes of files to set information about files
                try:
                    SQLsendFName(self.P.SQLserver, self.P.SQLuser, self.P.SQLpw, 'uploads', self.opath + self.fname, self.P.ftpbenutzer, self.P.ftppasswort, self.P.FTPfolder)
                except:
                    pass
            else:
                commandtodo = "mv " + "current_" + self.fname + " " + self.fname
                ###print(commandtodo)
                os.system(commandtodo)
            	
            print("file moved or data saved to sql uploads")	
        # switch off Voltage:
        #GPIO.output(GPIOVoltagePin, GPIO.LOW) # default satte of power is off
        renamecurrents(self.opath)
        print("rename currents done")	
        GPIO.cleanup()
        print("GPIO cleanup")	
        sys.stdout.flush()
        print("sys flush")	
        os._exit(0)

# Ready
# =======================================================================================
