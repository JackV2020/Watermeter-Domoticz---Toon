This watermeter plugin was developed on Raspberry Pi Buster and may work on other platforms also.

The sensor I use costed me about 6 euro's and is an 'inductive proximity sensor LJ12A3-4-Z/BX' and sits on top of my watermeter. ( more info below )

The plugin creates 4 Monitors :

 - 1 for your water meter showing your meter value
 - 1 for a date like Januari 1st showing the usage since that date
 - 1 for a date like last payment showing the usage since that date
 - 1 for the current usage in l/m

The main page of the plugin is used to

 - select the GPIO of the sensor
 - setup the name and start value of the main meter monitors
 - setup the names and values of the 2 'usage since' monitors
 - optionally change the dates and values of the 2 'usage since' monitors
 - help info on what to do when you replace your water meter ( which starts with a new value like 0 )

No polling is done by the plugin because updates are done by an interrupt routine in the plugin which is triggered by the sensor.
This interrupt routine is implemented in the script watermeter.sh which is startd by the plugin by calling spawn_bash.sh

Below you find info on :

 - how to install the sensor
 - how to install the plugin on your Domoticz
 - and if you like how to get data on your legally rooted Eneco Toon 1 / Toon 2 by installing an app on your Toon

The sensor I use is an LJ12A3-4-Z/BX which is specified to work between 6 and 36 volts DC but works with the 5 volts of a Raspberry Pi for undocumented reasons. 
You have to mount it on top of the watermeter so it 'looks' at the little arrow which turns around for every litre.
( look in the pictures folder to see sensor.png and a picture of my water meter with the sensor )

The sensor has 3 wires :

 - brown + 5V
 - blue  - 
 - black GPIO ( my default is 27 because 3^3=27, or maybe because 27 was free 8-) )

It needs no additional hardware but for safety I put a 10K resistor between the sensor (black wire) and my GPIO.

To install the plugin you need to get the contents in your plugin folder :

On a Raspberry Pi you could :

Start a terminal and go to your plugins folder and the next will get it for you into a watermeter folder : 

 ....../plugins$ git clone https://github.com/JackV2020/Watermeter-Domoticz---Toon.git watermeter

To get it into Domoticz restart your domoticz like :

    sudo systemctl restart domoticz

After this you can add a device of the Type 'Jacks Water Meter'.

To get your water meter and other data on a rooted Toon 1 or Toon 2 you may use my Toon APP 'Domoticz Monitor'  https://github.com/JackV2020/domoMon  

There is also a very nice app available in the Toon store : ToonWater by oepi-loepi.

Thanks for reading and enjoy.
