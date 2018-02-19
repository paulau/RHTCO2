#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import MySQLdb
import sys
import time, datetime

def SQLsendFName(SQLServer, SQLUser, SQLPasswd, Tabelle, FullFileNameToUpload, FTPUser, FTPPassword,  FTPFolderToUpload):
	
	con = MySQLdb.connect(SQLServer,SQLUser,SQLPasswd,"Datenerfassung")
	with con:
		cur = con.cursor()

		command = "INSERT INTO %s (FullFileNameToUpload, FTPUser, FTPPassword,  FTPFolderToUpload) VALUES ('%s','%s','%s','%s')"% (Tabelle, FullFileNameToUpload, FTPUser, FTPPassword,  FTPFolderToUpload)
		#print command
		cur.execute(command)		
		cur.close()
		con.commit()
