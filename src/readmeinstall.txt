1) Install Win32DiscImager on Windows computer and run as administrator
2) Choose image of wheezy e.g. 2015-02-16-raspbian-wheezy.img and put it onto MicroSD
3) in the end of cmdline.txt add
ip=192.168.10.2 
and save
4) Configure TCP/IP on Windows Computer, eg:
IP 192.168.10.100
Mask: 255.255.255.0

5) Insert MicroSD into Raspberry Pi, connect Raspberry with Windows computer 
via Ethernet Patchkord. Attach power supply to Raspberry Pi e.g. via MicroUSB.

6) Install Putty on windows and connect to 192.168.10.2
User: pi 
Password: raspberry

7) Change Password: 
sudo -s
raspi-config
Change User Password

8) To copy files to Raspberry via scp, use eg Far Manager mit WinSCP Plugin. 

9) copy  interfaces und wpa_supplicant.conf from conf/
to /home/pi/

10). move files using putty 
sudo mv interfaces /etc/network/
sudo mv wpa_supplicant.conf /etc/wpa_supplicant/

11) nano /boot/cmdline.txt
remove ip=192.168.10.2

12) Insert USB WIFiStick
ifdown wlan0
ifup wlan0
check internet z.b.
ping google.de


13) sudo apt-get update

14) activate I2C.
raspi-config 
Advanced Options
I2C
Yes for all questions. Reboot. 

15)
connect using Putty again. In putty 
sudo -s 
apt-get update
apt-get install -y python-smbus
apt-get install -y i2c-tools

nano /etc/modules
add following if not added:
i2c-bcm2708 
i2c-dev

Depending on your distribution, you may also have a file called /etc/modprobe.d/raspi-blacklist.conf

If you do not have this file then there is nothing to do, however, 
if you do have this file, you need to edit it and comment out the lines below: 
1. blacklist spi-bcm2708
2. blacklist i2c-bcm2708

nano /boot/config.txt
Should be in file:
dtparam=i2c1=on
dtparam=i2c_arm=on

reboot

sudo i2cdetect -y 1


mkdir notsmb
cd notsmb
wget http://www.byvac.com/downloads/sws/notsmb_1_0.zip
unzip notsmb_1_0.zip
apt-get update
sudo apt-get install python-dev
python setup.py install


16) Switch off Raspberry and connect i2c Sensor to i2c pins of Raspberry. 
Switch on and connect to raspberry using putty:

sudo -s
copy test/CO2meter.py to /home/pi/ and test:

python CO2meter.py

17) Adafruit installieren:
copy folder 
DHT22/Adafruit_Python_DHT in /home/pi

in putty 
cd Adafruit_Python_DHT/
sudo apt-get update
sudo apt-get install build-essential python-dev
sudo python setup.py install
clear 
cd ..


18) test dht22: 
Connect DHT22 Sensor zu: GND VCC3.3V GPIO-8-Data.
copy 
python
import Adafruit_DHT as dht
import RPi.GPIO as GPIO  # to switch on voltage on certain channels
GPIO.setmode(GPIO.BCM)
GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_UP)
h,t = dht.read_retry(dht.DHT22, 8)	

Ok.

19) 
Datenbank einrichten:

apt-get update
#install mysql library for python 
sudo apt-get install -y python-mysqldb
sudo apt-get install -y mysql-server
specify root Pass:

nano /etc/mysql/my.cnf

bind-address= 0.0.0.0
/etc/init.d/mysql restart

#php apache installieren:
sudo apt-get install apache2 php5 libapache2-mod-php5


mysql -u root -p

mysql> show databases;
#Wenn Datenbank "Datenerfassung" nicht vorhanden ist, dann erzeugen:
mysql>CREATE DATABASE Datenerfassung;
#Check it:
mysql>show databases;
mysql>use Datenerfassung #Wählt die Datenbank "Datenerfassung" aus
#Create nonadministrative - logger user
mysql>CREATE USER 'logger' IDENTIFIED BY 'logger112358';
#Create Table(s) for Datenerfassung of CO2, RH, T Sensor.
mysql>CREATE TABLE RHTCO2(Id INT PRIMARY KEY AUTO_INCREMENT, Datum date, Zeit time, RH float, T float, CO2 smallint);

#Gibt dem MySQL User "logger" Rechte auf alle Tabellen in der Datenbank 
#"Datenerfassung" ('' muss auch im Code stehen)
mysql>GRANT ALL PRIVILEGES ON Datenerfassung.* TO 'logger'; 

Ctrl+C

select * from Datenerfassung.RHTCO2 order by id desc limit 100;



20) Create Folder RHTCO2
exit, wenn es root war.
mkdir RHTCO2


copy src files of RHTCO2 project into /home/pi/RHTCO2/


configure if necessary all settings in settingsRHTCO2_009.py

copy conf/rc.local and conf/sqlwrapper.php to /home/pi

sudo mv rc.local /etc/
sudo mv sqlwrapper.php /var/www/

apt-get install libapache2-mod-auth-mysql phpmyadmin

test: 

check wether it works:
ps -u root | grep "python"
check data: 
192.168.10.2/sqlwrapper.php?len=1


21) configure time sinchronization

sudo -s

nano /etc/ntp.conf

comment standard server
put instead:

#server time-ol.hs-woe.de iburst
#server time-whv.hs-woe.de iburst

in putty:

ntpd -q -g
sudo /etc/init.d/ntp stop
sudo /etc/init.d/ntp start

raspi-config 
internationalization Options
Time Zone
Europe Berlin


sudo reboot

Following steps configure optional uploader :
22) configure uploader:  
connect via putty and far

copy files: 
Datenerfassung/commonpy/uploader/uplo05.py
upload_my_data_04a.py 
to /home/pi/RHTCO2/
mv upload_my_data_04a.py /usr/lib/python3.2/

ps -u root | grep "python"
kill -15 processid
start again 

test: 
sudo python3 /home/pi/RHTCO2/uplo05.py   /home/pi/RHTCO2/  settingsRHTCO2.py 1> /home/pi/RHTCO2/tmp_uplo_out.txt 2> /home/pi/RHTCO2/tmp_uplo_err.txt &


23) 
configure 
autostart:
nano /etc/rc.local
sudo python /home/pi/RHTCO2/RHTCO2_009.py ...
sudo python3 /home/pi/RHTCO2/uplo05.py   /home/pi/RHTCO2/  settingsRHTCO2.py 1> /home/pi/RHTCO2/tmp_uplo_out.txt 2> /home/pi/RHTCO2/tmp_uplo_err.txt &

24) 
Check guteluft.jade-hs.de 
find data of correcponding toom. 


25) 
pusten in sensor check umschaltung rot-grün
