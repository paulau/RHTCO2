RHTCO2

This project is implemented to 
* read the data of temperature, humidity and CO2 sensors  (DHT22, K-30 - CO2, HYT271)
* to store the sata as set of text files with columns (date time RH T CO2)
  and in MySQL database Datenerfassung in table RHTCO2
* to send data as separate files via ftp to some central server 
* to make available the fast data in table Datebnerfassung.FAST 
  (also available via php wrapper: sqlwrapper.php ana Apache Web Server)
* To control LED: switch on, if CO2 -concentration too high is. 


Raspberry should have following packages:
apt-get install apache2 php5-common libapache2-mod-php5 php5-cli phpmyadmin
