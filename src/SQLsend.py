#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import MySQLdb
import sys
import time, datetime

def SQLsend(SQLServer, SQLUser, SQLPasswd, Tabelle, Datetime, RH, T, CO2):
	Datum = "{:%Y%m%d}".format(Datetime)
	Zeit = "{:%H%M%S}".format(Datetime)
	con = MySQLdb.connect(SQLServer,SQLUser,SQLPasswd,"Datenerfassung")
	with con:
		cur = con.cursor()
		command = "INSERT INTO %s (Datum,Zeit,RH,T,CO2) VALUES (%s,%s,%s,%s,%s)"% (Tabelle, Datum, Zeit, float(RH), float(T), int(CO2))
		#print(command)
		cur.execute(command)		
		cur.close()
		con.commit()
