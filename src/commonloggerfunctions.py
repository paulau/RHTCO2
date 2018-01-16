#!/usr/bin/env python
# -*- coding: UTF-8 -*-


# ======================================================================
# This function is common for all loggers. It is therefore defined in:
# commonloggerfunctions.py

# It is possible, that Device was restarted. Also using power off-on. 
# Then old files with prefix current_ could be there we make first rename of all existing
# current_ files into files without current preffix:

# before to open new current file try to
# rename possibly earlier stored current files:
# this can be called independant of use of SQL uploadstable 

import os

# needded argument - path to folder with files (with / in the end)
def renamecurrents(opath):
	try: 

		# Get list of files to upload:
		li=os.listdir(opath + ".")
		currfileprefix = "current_"
		for fname in li:
			if (fname.find(currfileprefix)==0): # if there are names starting from currfileprefix  then:
				try:  # try to:
					# and rename the file into  file without prefix "current_"
					newfname = fname
					newfname = newfname.replace(currfileprefix, '') 
					commandtodo = "mv " + opath + fname + " " + opath + newfname
					#print(commandtodo)
					os.system(commandtodo)
				except:
					print(fname)
					pass
	except:
		pass

