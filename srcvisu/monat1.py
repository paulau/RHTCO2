#!/usr/bin/python
# -*- coding: UTF-8 -*-

# usage: 
# monat1.py settingsRHTCO2.py

# change starting date and number of monthes to process.
# works on windows

# measurements are stored normally every hour or day in separate file. 
# time is encoded in filename. 
# all files of the same measurement-point have the same fileprefix. 
# fileprefix is defined in settings file eg settingsRHTCO2*.py

# This script concatinates measurementfiles of each month in separate file.
# accordingly prefix out_ is added. 
# files of each hour are removed

# Written by Pavel Paulau.
 
import sys, os, imp # imp - to load settinxs***.py 
from GetRecent import GetMonat
import datetime   # to handle date
from datetime import timedelta # to increment on 1 Month


if (len(sys.argv)==2):
#	ipath  = sys.argv[1]
	ipath = os.getcwd() + "\\"
	settingsfname = sys.argv[1]
else:
	print("usage, e.g.:")
	print("monat1.py settingsRHTCO2.py")
	quit()
	
settingsfname = ipath + settingsfname
print(settingsfname)
P = imp.load_source('settings', settingsfname) # read Parameters
fileprefix = P.fileprefix

# start  from this date:
d1 = datetime.datetime(2017, 1, 1, 0, 0) 

def IncMonth(d1):
	dmonths = 1
	Month = d1.month - 1 + dmonths
	Year = int(d1.year + Month / 12 )
	Month = Month % 12 + 1
	return datetime.date(Year,Month,1)

for j in range(0,40):
	d1 = IncMonth(d1)  
	#JahrMonat="2015_06_"
	JahrMonat = d1.strftime("%Y_%m_")
	try:
		print("processing of " + JahrMonat)
		GetMonat(ipath, fileprefix, JahrMonat, '%Y_%m_%d_%H_%M', '.std')
	except:
		print("There are apparently no data from " + JahrMonat)
		pass
