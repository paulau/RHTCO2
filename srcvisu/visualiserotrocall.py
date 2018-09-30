#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
Python script to call  VisualiseRotroFile
See comment-description in the beginning of corresponding python file

python /home/pi/web/visualiserotrocall.py /home/pi/web/ /home/pi/web/AmZollbaum10OldenburgEGrechtsrechtsSchlaffZimmerKleinP.png 744

visualiserotrocall.py c:/work/DatenErfassung/users/Physiklabor/Wilhelm13/Messdaten/backup_2017_02_2017_01_wilhelm13_all.txt
"""

import sys, os # to deal with command line arguments 
import imp # to load settinxs***.py 
from visualiseRotro import VisualiseRotroFile # to visualise data
from GetRecent import GetRecent

settingsfname = "settingsRHTCO2_009.py"


if (len(sys.argv)==2):
	# This mode (just one input argument) is defined for work on local 
	# maschine, to visualise data for report. 
	ifile = str(sys.argv[1])
	ofile =ifile[0:-3]
	ofile = ofile + "png"
	ipath = os.getcwd() + "\\"
	print (ifile + " " + ofile)
	settingsfname = ipath + settingsfname
	P = imp.load_source('settings', settingsfname) # read Parameters
	if (not hasattr(P, 'VisualisationInterval')):
		VisualisationInterval = -1
	else:
		VisualisationInterval = P.VisualisationInterval

	if (not hasattr(P, 'tex')):
		tex = False #True # with tex
	else:
		tex = P.tex

	
	dpivalue = 300
	window = True

	
elif (len(sys.argv)==4): # 1) path to data and  2) name of output file	3 amount of hours to plot
	# this mode is for visualisation for web
	ipath  = sys.argv[1]
	ofile = sys.argv[2]
	VisualisationInterval = int(sys.argv[3])
	# import settings: 
	settingsfname = ipath + settingsfname
	P = imp.load_source('settings', settingsfname) # Parameters
	tex = False # first without tex
	window = False
	dpivalue = 150
	GetRecent(ipath, P.fileprefix, VisualisationInterval) 
	ifile = ipath + 'out.txt'

elif (len(sys.argv)==5): # 1) path to data and  2) name of output file	3 amount of hours to plot
	
	#last fourth argument specify to visualise only current file:
	# this mode is for visualisation for web
	ipath  = sys.argv[1]
	ofile = sys.argv[2]
	VisualisationInterval = int(sys.argv[3])
	# import settings: 
	settingsfname = ipath + settingsfname
	P = imp.load_source('settings', settingsfname) # Parameters
	tex = False # first without tex
	window = False
	dpivalue = 150
	if (int(sys.argv[4])==1):
		VisualisationInterval = 48 # redefine interval to get all data of at least one day
		GetRecent(ipath, "current_" + P.fileprefix, VisualisationInterval) 
		VisualisationInterval = -1 # redefine interval to set xlim to all datarange
		
	else: # just normal:
		GetRecent(ipath, P.fileprefix, VisualisationInterval) 
	ifile = ipath + 'out.txt'
		

else:
	print("Usage. Start cmd. cd to folder with data.")
	print("Must be started with one argument inputfilename")


HYT = hasattr(P, 'HYT271address')

print(VisualisationInterval)
# main call:
VisualiseRotroFile(ifile, P, window, ofile, VisualisationInterval, dpivalue, P.description, tex, HYT) 
