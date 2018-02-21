#!/usr/bin/env python  
# -*- coding: UTF-8 -*-

# Script to set time from rtc modul 
# it is here because  rtc with hwcloch fails sometimes

import os, time

for i in range(1,5): # try 5 times
	try:
		cmdtodo = "sudo hwclock -s"
		os.system(cmdtodo)
		time.sleep(3) # 3 sec delay
	except:
		pass # just go forward and try again

#_______________________________________________________________________
