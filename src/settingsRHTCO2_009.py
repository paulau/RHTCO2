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

SignalControlPin = 18 
CO2Limit = 1000

VentControlPin = 21 # Additionnally to signal (red ligt), the switch on off
                    # of a ventillator is added



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

