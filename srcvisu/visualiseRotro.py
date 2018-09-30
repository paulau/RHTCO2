#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
Python script um Daten mit spalten: Datum Zeit RH T CO2  zu visualisieren.
Wie von Rotronic oder von K-30 und DHT generiert

This program visualizes data with following format: 
Datum leerzeichet Zeit Tab Relative Humidity tab Temperatur Tab CO2conzentration. e.g.:
04.02.2016 11:17:49    30.40    26.00    979

Written by Pavel Paulau 

in case if  HYT==True, daten format is:  
Datum Leerzeichen Zeit Tab Relative Humidity Tab Temperatur Tab CO2conzentration  Tab Relative Humidity2 Tab Temperatur2 e.g.:
04.02.2016 11:17:49    30.40    26.00    979    60.40    25.00

HYT will be set to true if  HYT271address is defined in settingsRHTCO2. 
In case if yes, then plot 
additional data from HYT sensor. 
 

"""



fa = 5
import datetime  
from datetime import timedelta

from CleanRHTCO2Data import CleanRHTCO2reihe
from CleanRHTCO2Data import CleanRHTCO2Format
from CleanRHTCO2Data import CleanRHTCO2HYTreihe
import sys


def ReadRotroFile(ifile, HYT=False):
    
    print("hallo")
    with open(ifile) as f:
        data = f.read()
    
    data = data.replace(',','.') # 
    
    data = data.split("\n")
    data.pop(0) # remove first
    data.pop() # remove last
    #for stri in data:
    #    print(stri)
    
    

    # ------------------------------------------------------------------
    # remove records with bad format 
    if (HYT):
        CleanRHTCO2Format(data, True)
    else:
        CleanRHTCO2Format(data)

    
    DateTimeM = [row.split('\t')[0] for row in data]
    RH = [row.split('\t')[1] for row in data]    
    Temp = [row.split('\t')[2] for row in data]
    CO2 = [row.split('\t')[3] for row in data]
    
    print(CO2)
    if (HYT):
        HYTRH = [row.split('\t')[4] for row in data]
        HYTT = [row.split('\t')[5] for row in data]


    
    #-------------------------------------------------------------------
    if (HYT):
        CleanRHTCO2HYTreihe(DateTimeM, RH, Temp, CO2, HYTRH, HYTT) # remove points which do not belong to continuous curve.
    else:
        CleanRHTCO2reihe(DateTimeM, RH, Temp, CO2) # remove points which do not belong to continuous curve.


    #print(DateTimeM)
    t = []
    for i in range(len(DateTimeM)):
        #try:
        dd = datetime.datetime.strptime(DateTimeM[i], '%d.%m.%Y %H:%M:%S') # 
        t.append(dd)    
        #except:
        #    t.append(Now)    # if format is wrong then add just some date
    
    if (HYT):
        return t, RH, Temp, CO2, HYTRH, HYTT 
    else: 
        return t, RH, Temp, CO2
#=======================================================================

# Fourth obligatory argument is added. It is structure, which may contain or may not contain 
# various parameters. Optionally, other parameters, may be given as other arguments of 
# this function

def VisualiseRotroFile(ifile, P, window=False, outfile="RotroH.png", VisualisationInterval=10, dpivalue = 150, Description=" ", tex = False, HYT = False):

    ts = 12 # tex font size
    
    import matplotlib as mpl
    if (not window):
        mpl.use('Agg')

    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt


    print(ifile)


    #_______________________________________________________________________
    if (not hasattr(P, 'myFmt')):
        myFmt = mdates.DateFormatter('%d.%m %H:%M')   # '%d.%m.%Y %H:%M'  
    else:
        myFmt = P.myFmt


        
        
    # ======================================================================
    # defaults definition:
    if (not hasattr(P, 'y1max')):
        y1max = 80
    else:
        y1max = P.y1max
    #_______________________________________________________________________
    if (not hasattr(P, 'y1min')):
        y1min = 10
    else:
        y1min = P.y1min
    #_______________________________________________________________________
    if (not hasattr(P, 'y2max')):
        y2max = 3500
    else:
        y2max = P.y2max
            
    #_______________________________________________________________________
    if (not hasattr(P, 'y2max')):
        y2min = 350
    else:
        y2min = P.y2min
    
    
    Now = datetime.datetime.today()

    if (tex):
        plt.rc('text', usetex=True)
        plt.rc('font', family='serif')

    if (HYT): 
        t, RH, Temp, CO2, HYTRH, HYTT = ReadRotroFile(ifile, True)
    else:    
        t, RH, Temp, CO2 = ReadRotroFile(ifile)
    
     
    fig = plt.figure() #,  dpi=300 1
    # "Temperatur Und Feuchtigkeit")
    
    ax1 = fig.add_subplot(111) # 211
    ax1.set_xlabel('t')
    if (tex):
        ax1.set_ylabel(r'T, $^o$C, oder $\phi$, \%', fontsize=ts)
    else:
        ax1.set_ylabel(u'T, °C, oder RH, %') # 
    #ax1.set_title('a) - Fühler 1')    
    
    if (tex):
        legends = [r'$T$ - Temperatur', r'$\phi$ - relative Feuchtigkeit', r'$C_{CO_2}$-Konzentration']
    else:
        legends = ['Temperatur', 'relative Feuchtigkeit', 'CO2-Konzentration']
        
    
    if (not hasattr(P, 'RHswitch')):
        RHswitch = 1
    else: 
        RHswitch = P.RHswitch    
    
    if (not hasattr(P, 'Tswitch')):
        Tswitch = 1
    else: 
        Tswitch = P.Tswitch    
    
    if Tswitch:         
        line1 = ax1.plot(t, Temp, '.', color='#FF0000', label=legends[0])
     
    if RHswitch: 
        line2 = ax1.plot(t, RH, '.', color='#0000FF', label=legends[1])

    if (HYT):
        line11 = ax1.plot(t, HYTT, '.', color='#A52A2A', markersize = 3, label='Temperatur, HYT') 
        line21 = ax1.plot(t, HYTRH, '.', color='#00FFFF', markersize = 3,  label='Feuchtigkeit, HYT')
    
    ax1.set_ylim([y1min, y1max])    
    plt.grid()    
    fig.autofmt_xdate()
    ax1.xaxis.set_major_formatter(myFmt)


    ax1r = ax1.twinx()    
    line3 = ax1r.plot(t, CO2, '.', color='#00FF00', label=legends[2])
    
    CleanLevel = 400
    Clean = CO2 # just allocate array of the same size
    Clean[:] = [CleanLevel  for x in CO2]
    line3a = ax1r.plot(t, Clean, '-', linewidth=3, color='#119911', label='Clean air level')


    DirtyLevel = 1000.0
    Dirty = CO2 # just allocate array of the same size
    Dirty[:] = [DirtyLevel  for x in CO2]
    line3b = ax1r.plot(t, Dirty, '-', linewidth=3, color='#FF9900', label='Dirty air threshold')

    
    
    #line3 = ax1r.semilogy(t, CO2, '.', color='#00FF00', label='CO2')
    if (tex):
        ax1r.set_ylabel(r'$C_{CO_2}, ppm')
    else:
        ax1r.set_ylabel('CO2, ppm')

    #_______________________________________________________________________
    if (hasattr(P, 'd1')):
        d1 = P.d1
        d2 = P.d2
    else:
        #ax1r.set_ylim([0, 1000])
        if (VisualisationInterval>0):
            d2 = Now # t[-1]
            d1 = d2 - timedelta(hours=VisualisationInterval)
        else:
            d2 = t[-1]
            d1 = t[0]
        
    ax1r.set_xlim([d1, d2])    
    ax1r.set_ylim([y2min, y2max])    
    
    if (HYT):
        lns = line3
        if RHswitch:
            lns = lns +    line1 
        if RHswitch:
            lns = lns +    line2 
        lns = lns +  line11 + line21 + line3a + line3b
        labs = [l.get_label() for l in lns]
        ax1.legend(lns, labs, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, prop={'size':7},  markerscale=2)         #fontsize=12,
    else:    
        lns = line3 
        if RHswitch:
            lns = lns +    line1
        if RHswitch:
            lns = lns +    line2
        lns = lns + line3a + line3b
        labs = [l.get_label() for l in lns]
        ax1.legend(lns, labs, loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=5, prop={'size':10},  markerscale=2)         #fontsize=12,
    
    
    
    
    #ax1.legend(lns, labs, loc='upper center', bbox_to_anchor=(0.5, -0.6), ncol=5, prop={'size':10}, markerscale=2)        
    #ax1.legend(lns, labs, loc=2, prop={'size':10}, fontsize=12, markerscale=2)        
    #plt.gcf().autofmt_xdate()


    #_______________________________________________________________________
    if (hasattr(P, 'DescriptionArr')):
        DescriptionArr = P.DescriptionArr
    else:
        DescriptionArr = [" "," "]

                
    print(DescriptionArr)
    
    h = 0.94
    shift = 0.03
    
    leftmargin = 0.13

    for descrstr in DescriptionArr:
        plt.figtext(leftmargin, h, descrstr)
        h = h - shift
    
    plt.figtext(leftmargin, h, "Erstellungsdatum: "  + Now.strftime("%d.%m.%Y %H:%M:%S") )
    h = h - shift

        
    descrmonat = plt.figtext(leftmargin, h, '| Jahr: ' + d1.strftime("%Y")  + ' Monat: ' + d1.strftime("%m"))
    h = h - shift
    
    
    plt.savefig(outfile, dpi=dpivalue) # save temperatures  


    
    if (not window): # do it only for visualisierung without Window. for internet page
        # =======================================================================
        # Save file with Data of last week
        d1 = d2 - timedelta(hours=168) # Eine Woche
        ax1r.set_xlim([d1, d2])        
        fig.texts.remove(descrmonat); #draw()  # remove previous text Monat
        descrwoche = plt.figtext(leftmargin, 0.92, Description + ' Woche.')
        outfWoche = outfile[:len(outfile)-4]+"woche"+outfile[len(outfile)-4:] # add suffix Woche
        plt.savefig(outfWoche, dpi=dpivalue) # save temperatures  
        
        # =======================================================================
        # Save file with data of today
        d2 = d2 - timedelta(hours = 1, minutes = d1.minute, seconds = d1.second)
        d1 = d2 - timedelta(hours = d1.hour, minutes = d1.minute, seconds = d1.second)
        ax1r.set_xlim([d1, d2])        
        fig.texts.remove(descrwoche); #draw()  # remove previous text Monat
        descrwoche = plt.figtext(leftmargin, 0.92, Description + ' Heute.')
        outfTag = outfile[:len(outfile)-4]+"tag"+outfile[len(outfile)-4:] # add suffix  Tag
        plt.savefig(outfTag, dpi=dpivalue) # save temperatures  

    
    if (window):
        plt.show()
    else:
        plt.close()

# the file which was outputfile for reading method is now input file for 
# processing method

