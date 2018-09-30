#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from os import listdir
from os.path import isfile, join
import datetime, calendar
from datetime import timedelta
import os, time


# ----------------------------------------------------------------------
# Diese Funktion lest alle Dateien von "mypath" mit "fileprefix", dessen Datum
# nicht älter als "VisualisationInterval" ist. Datum ist in Name von Dateien kodiert 
# mit Format "datetimeformat". Inhalt von alle Dateien wird in "outfile"
# gespeichert. 

def GetRecent(mypath, fileprefix, VisualisationInterval=10, datetimeformat='%Y_%m_%d_%H_%M', outfile='out.txt'):

	onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
	#print (onlyfiles)
	neededfiles = []
	Now = datetime.datetime.today()
	d1 = Now - timedelta(hours=VisualisationInterval)  #days
	print(d1)
	for fname  in onlyfiles:
		if (fname.find(fileprefix)==0):
			try: 
				dtm = datetime.datetime.strptime(fname, fileprefix + datetimeformat + '.txt')  # date of file
				if ((dtm > d1)&(VisualisationInterval>0)):  
					neededfiles.append(fname)

				if (VisualisationInterval<0):	
					neededfiles.append(fname)	
			except: 
				pass
			#MessungsAnfang = datetime.datetime.strptime('20.05.2015 15:06', '%d.%m.%Y %H:%M') 
	
	#print (neededfiles)
	print(len(neededfiles))
	print(VisualisationInterval)
	# open file for output:
	
	ofname = mypath + outfile #"out.txt" #"\\out.txt"
	fout = open(ofname, 'w')
	# read all needed files and save them into one:
	#print(ofname)
	for fname in neededfiles:
		#cmdtodo = cmdtodo + " " + mypath + fname #  
		input_file = mypath +  fname # "\\" +
		#print (input_file)
		with open(input_file) as f:
			data = f.read()    
		fout.write(data)
		f.close()
	fout.close()
		


# ----------------------------------------------------------------------
# Diese Funktion lest alle Dateien von "mypath" mit "fileprefix", dessen Monat und Jahr
# in "JahrMonat" gegeben sind. Datum ist in Name von Dateien kodiert 
# mit Format "datetimeformat". Inhalt von alle Dateien wird in file 
# out_nameoffirstfileinserietosave
# gespeichert.
# Daten von jede Stunde werden in Monats-Datei geschrieben.
# Dateien von Stunden werden entfernt. (Windows only)

# Z.B. JahrMonat="2015_07_" 

def GetMonat(mypath, fileprefix, JahrMonat, datetimeformat='%Y_%m_%d_%H_%M', extension='.txt'):

	onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
	#print (onlyfiles)
	neededfiles = []
	Now = datetime.datetime.today()
	
	datestartstr = JahrMonat + '01_00_00'	
	#print(datestartstr)
	d1 = datetime.datetime.strptime(datestartstr, datetimeformat)  # date of file	
	#print(d1)
	d2 = d1 + timedelta(days=calendar.monthrange(d1.year,d1.month)[1])  #days
	#print(d2)
	
	onlyfiles.sort()
	for fname  in onlyfiles:
		#print(fname)
		if (fname.find(fileprefix)==0):
			try: 
				dtm = datetime.datetime.strptime(fname, fileprefix + datetimeformat + extension)  # date of file
				if ((dtm >= d1)&(dtm<d2)):
					neededfiles.append(fname)
					
			except: 
				pass
			#MessungsAnfang = datetime.datetime.strptime('20.05.2015 15:06', '%d.%m.%Y %H:%M') 
	
	
	#print (neededfiles)
	print(len(neededfiles))
	# open file for output:
	outfile='out_' + neededfiles[0]  #
	 	
	ofname = mypath + outfile #"out.txt" #"\\out.txt"
	fout = open(ofname, 'w')
	# read all needed files and save them into one:
	print(ofname)
	for fname in neededfiles:		
		
		input_file = mypath +  fname # "\\" +		
		print (input_file)
		with open(input_file) as f:
			data = f.read()    
			
		#print(data)	
		fout.write(data)
		f.close()
		if (mypath=="./"):
			input_file = input_file.replace('./', '')
		# remove file after saving it:
		cmdtodo =  " del " + input_file  
		print(cmdtodo)
		os.system(cmdtodo)
		
	fout.close()
	
	cmdtodo =  "move " + outfile + " " + outfile.replace('out_', '')  
	print(cmdtodo)
	os.system(cmdtodo)
		


# _______________________________________________________________________



# ----------------------------------------------------------------------
# Diese Funktion lest alle Dateien von "mypath" mit "fileprefix". Datum ist in Name von Dateien kodiert 
# mit Format "datetimeformat". Inhalt von alle Dateien wird in file 
# out_nameoffirstfileinserietosave
# gespeichert.
# Die gesamte Daten werden in outfname geschrieben.
# Dateien von Stunden werden entfernt. (Windows only)


def GetAll(mypath, fileprefix, outfname, datetimeformat='%Y_%m_%d_%H_%M'):

	onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
	#print (onlyfiles)
	neededfiles = []

	onlyfiles.sort()
	for fname  in onlyfiles:
		#print(fname)
		if (fname.find(fileprefix)==0):
			neededfiles.append(fname)
	
	#print (neededfiles)
	print(len(neededfiles))
	# open file for output:
	outfile='out_' + neededfiles[0]  #
	 	
	ofname = mypath + outfname #"out.txt" #"\\out.txt"
	fout = open(ofname, 'w')
	# read all needed files and save them into one:
	print(ofname)
	for fname in neededfiles:		
		input_file = mypath +  fname # "\\" +		
		print (input_file)
		with open(input_file) as f:
			data = f.read()    
			
		#print(data)	
		fout.write(data)
		f.close()
		if (mypath=="./"):
			input_file = input_file.replace('./', '')
		# remove file after saving it:
		cmdtodo =  " del " + input_file  
		print(cmdtodo)
		os.system(cmdtodo)
		
	fout.close()
	
	cmdtodo =  "move " + outfile + " " + outfile.replace('out_', '')  
	print(cmdtodo)
	os.system(cmdtodo)
		


# _______________________________________________________________________


def GetRecentFile(mypath, fileprefix):
	datetimeformat='%Y_%m_%d_%H_%M'
	onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
	neededfiles = []
	for fname  in onlyfiles:
		if (fname.find(fileprefix)==0):
			try: 
				dtm = datetime.datetime.strptime(fname, fileprefix + datetimeformat + '.txt')  # date of file
				neededfiles.append(fname)
			except: 
				pass
	
	#print("____________")
	neededfiles.sort()
	
	#print (neededfiles)
	recentfname = mypath + neededfiles[-1]
	#print(recentfname)
	return recentfname
