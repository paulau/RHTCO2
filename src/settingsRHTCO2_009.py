#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Attention! Very specific setting for one or two reconfigured sensors.
CO2_ADDR = 0x60

DHTDataPin=8
GPIOVoltagePin=25

LoggingRate = 1
FTPfolder = "I23"
fileprefix = "messung001_"
ftpserveraddr="139.13.179.47"
ftpbenutzer="jadehs"
ftppasswort=""
UploadRate=86400
SaveInterval = "%M" #  "%d" # "%d" save every new day, "%H" save every new Hour

internettype = 2 # 1 - Ethernet 2 - WiFi 3 - MobileBroadband
description = "I23" #

# ifSQLuser is defined, then mySQL will be used
SQLuser = "logger"
SQLpw = "logger112358"
tabelle = "RHTCO2"
SQLserver = "localhost"

# uploadstable = "uploads"  # not configured for CO2-ampel home

FAST = True

SignalControlPin = 21 

# CO2 concentration in excess above the outdoor air:
# IDA1  <= 400    High Quality
# IDA2  400-600   Average Quality
# IDA3  600-1000  moderate quality
# IDA4  >1000     low quality
# __________________
# DIN EN 13779




#An average concentration of CO2 in outdoor air is 400ppm Year 2018.

CO2Limit = 1000 # 1000 ppm means IDA 3 Lower range of moderate quality

VentControlPin = 18 # Additionnally to signal (red ligt), the switch on off
                    # of a ventillator is added

CO2LimitOff = 800 # IDA 1 

# settings for visualisation:
window=False
outfile="RHTCO2.png"
VisualisationInterval=10
y1min=10
y1max=80
#y2min=0
#y2max=3000
dpivalue=96 #150
Description=" "
tex = False

