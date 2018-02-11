RHTCO2

This project is implemented to 
* read the data of temperature, humidity and CO2 sensors  (DHT22, K-30 - CO2, HYT271)
* to store the sata as set of text files with columns (date time RH T CO2)
  and in MySQL database Datenerfassung in table RHTCO2
* to send data as separate files via ftp to some central server 
* to make available the fast data in table Datebnerfassung.FAST 
  (also available via php wrapper: sqlwrapper.php ana Apache Web Server)
* To control LED(automatically): switch on, if CO2 -concentration too high is. 


Raspberry should have following packages:
apt-get install  mysql-server mysql-client apache2 php5-common libapache2-mod-php5 php5-cli phpmyadmin

The usual configurations of i2c must be done.


Additional notices:

The used notsmb library is not supported to work properly with jessie and raspberry pi 3,
therefore the wheezie system must be used to run this software with notsmb library. 
Wheezie can be updated and upgrated on raspberry pi 2 and afterwards used 
on Raspberry Pi 3.  (apt-get install --only-upgrade raspberry-bootloader could do. not tested)
In plan is to publish here or somewhere the MicroSD images with full configured 
System.

Network configuration must be done. (hotspot or operation in a given 
WiFi Network, or in Ethernet Network) 

Although it takes normally less than 1 sec, to get data of both K-30 and DHT-22 
sensors, sometimes, sensors want to have more time to give values around 2s.
Therefore it is not "homogeneous" points distribution on the graphical representation.

Wiring:
Clock-Modul: - i2c  addr 0x68
CO2-Sensor:  - i2c  addr 0x60
DHT-22:      - GND, VCC3.3V, DataPin(configure in settings*.py) with 10kOhm pull up resistor
(it works also without, but seems with resistor - faster)
TransistorPlatine (or relay) with 5V LED stripe: GND, VCC5V, ControlPin (configured in settings*.py)
Edimax-WiFiStick : USB.
TransistorPlatine (or relay) with 5V LED stripe: GND, VCC5V, pin 21 for TangoDevice Button


THIS project is actually learn project to get familiar with a number of subjects.
one of subjects is tango server. The only purpose of the button is to be functional 
within tango framework


