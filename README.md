This plugin was developed on Raspberry Pi Buster and may work on other platforms.

Below you find info on :

 - how to install the sensor
 - what de plugin does
 - how to install the plugin on your Domoticz
 - and if you like how to get data on Toon 1 / Toon 2 by installing an app on Toon

I paid about 6 euro's for the sensor.
The sensor I use is an inductive proximity sensor LJ12A3-4-Z/BX which is specified to work between 6 and 36 volts DC but works with the 5 volts of a Raspberry Pi for undocumented reasons. You have to mount it on top of the watermeter so it 'looks' at the little arrow which turns around for every litre.
( look in the pictures folder to see sensor.png and a picture of my water meter with the sensor )

The sensor has 3 wires :

 - brown + 5V
 - blue  - 
 - black GPIO ( my default is 27 because 3^3=27, or maybe because it was free ;) )

It needs no additional hardware but for safety I put a 10K resistor between the sensor and my GPIO.

The plugin creates 3 Monitors :

 - 1 for your water meter showing your meter value
 - 1 for a date like Januari 1st showing the usage since that date
 - 1 for a date like last payment showing the usage since that date

The main page of the plugin is used to

 - select the GPIO of the sensor
 - setup the names of the 3 monitors
 - setup the initial values of the 3 monitors
 - change the dates and values of the 2 'usage since' monitors
 - help you when you replace your water meter ( starts with a new value like 0 )

Updates are done by a routine in the plugin itself which is triggered by the sensor.

To install or update the plugin you need to get the contents of the zip file watermeter.zip

On a Raspberry Pi you could :

Start a terminal and go to your plugins folder and the next wget command will download a zip file, unpack and remove the zipfile : 

 ....../plugins$ wget https://raw.githubusercontent.com/JackV2020/Watermeter-Domoticz---Toon/main/watermeter.zip -O watermeter.zip && unzip -o watermeter.zip && rm watermeter.zip

To activate the plugin in Domoticz you need to restart Domoticz and add a hardware item for the type 'Jacks Water Meter'.

When you do not like the Type name 'Jacks Water Meter' feel free to edit plugin.py and modify it before you actually add your hardware.

To get your water meter and other data on Toon 1 or Toon 2 you may use my app https://github.com/JackV2020/Toon-Domoticz-MonitorCS. 


Thanks for reading and enjoy.
