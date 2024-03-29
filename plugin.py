#
# Changelog:
#
# version 2.0.0 : Changed for new Domoticz API
# version 1.0.0 : initial version
#
# 
#    3V3  (1) (2)  5V    
#  GPIO2  (3) (4)  5V    
#  GPIO3  (5) (6)  GND   
#  GPIO4  (7) (8)  GPIO14
#    GND  (9) (10) GPIO15
# GPIO17 (11) (12) GPIO18
# GPIO27 (13) (14) GND          <-- my default is GPIO27   
# GPIO22 (15) (16) GPIO23
#    3V3 (17) (18) GPIO24
# GPIO10 (19) (20) GND   
#  GPIO9 (21) (22) GPIO25
# GPIO11 (23) (24) GPIO8 
#    GND (25) (26) GPIO7 
#  GPIO0 (27) (28) GPIO1 
#  GPIO5 (29) (30) GND   
#  GPIO6 (31) (32) GPIO12
# GPIO13 (33) (34) GND   
# GPIO19 (35) (36) GPIO16
# GPIO26 (37) (38) GPIO20
#    GND (39) (40) GPIO21
#

"""
<plugin key="JacksWaterMeter" name="Jacks Water Meter" author="Jack Veraart" version="2.0.0">
    <description>
        <font size="4" color="white">Water Meter</font><font color="white">...Notes...</font>
        <ul style="list-style-type:square">
            <li><font color="yellow">You can specify names for 3 Monitors and 3 Values in m³.</font></li>
            <li><font color="yellow">The Meter Value is used during the creation of your hardware and is the value on your water meter.</font></li>
            <li><font color="yellow">The other two need to be the water meter values as they were on the dates specified. Domoticz needs this to calculate the usage since these dates.</font></li>
            <li><font color="yellow">When you have a Password on your domoticz, enter Username and Password below, not your admin account <font size="4" color="white"><b>:-(</b></font> create a read only user <font size="4" color="white"><b>;-)</b></font> </font></li>
            <li><font color="yellow">Do you want to correct values because you missed ticks while your Domoticz was not running ? </font></li>
            <ul style="list-style-type:square">
                <li><font color="yellow">Enter the Meter Value which is on your physical water meter, Force Monitor Value : True, Do not change the other 2 Monitors.</font></li>
                <li><font color="yellow">Click Update above and<font color="cyan">...Do Not Forget : change Force Meter Value : <font color="white"><b>.False.</b></font> and click Update again.</font></font></li>
            </ul>
            <li><font color="yellow">New dates or values for Date 1 / Date 2 monitor ?</font></li>
            <ul style="list-style-type:square">
                <li><font color="yellow">Enter the Date 1 / Date 2 dates and values, Force Meter Value : <font color="white"><b>.False.</b></font></font></li>
                <li><font color="yellow">Click Update above. </font></li>
            </ul>
            <li><font color="yellow">New watermeter ? </font></li>
            <ul style="list-style-type:square">
                <li><font color="yellow">Enter the new value which may be 0 .</font></li>
                <li><font color="yellow">Force Meter Value : True.</font></li>
                <li><font color="yellow">--> Calculate new values for the other 2 Monitors : New value = Meter new - Meter old + Monitor old . ( New value is probably a negative value, just put it in. ) </font></li>
                <li><font color="yellow">Click Update above and<font color="cyan">...Do Not Forget : change Force Meter Value : <font color="white"><b>.False.</b></font> and click Update again.</font></font></li>
            </ul>
            <li><font color="yellow">To develop your own plugin...check this web site... <a href="https://www.domoticz.com/wiki/Developing_a_Python_plugin" ><font color="cyan">Developing_a_Python_plugin</font></a></font></li>
        </ul>
    </description>
    <params>
    
        <param field="Port" label="GPIO pin."   width="120px">
            <options>
                <option label="GPIO1"   value=1/>
                <option label="GPIO2"   value=2/>
                <option label="GPIO3"   value=3/>
                <option label="GPIO4"   value=4/>
                <option label="GPIO5"   value=5/>
                <option label="GPIO6"   value=6/>
                <option label="GPIO7"   value=7/>
                <option label="GPIO8"   value=8/>
                <option label="GPIO9"   value=9/>
                <option label="GPIO10"  value=10/>
                <option label="GPIO11"  value=11/>
                <option label="GPIO12"  value=12/>
                <option label="GPIO13"  value=13/>
                <option label="GPIO14"  value=14/>
                <option label="GPIO15"  value=15/>
                <option label="GPIO16"  value=16/>
                <option label="GPIO17"  value=17/>
                <option label="GPIO18"  value=18/>
                <option label="GPIO19"  value=19/>
                <option label="GPIO20"  value=20/>
                <option label="GPIO21"  value=21/>
                <option label="GPIO22"  value=22/>
                <option label="GPIO23"  value=23/>
                <option label="GPIO24"  value=24/>
                <option label="GPIO25"  value=25/>
                <option label="GPIO26"  value=26/>
                <option label="GPIO27"  value=27        default="true"/>
            </options>
        </param>

        <param field="Mode1" label="Water Monitor."     width="120px" default="Water>Total"/>

        <param field="Address" label="Meter Value m³." width="120px" default="4.567"/>

        <param field="SerialPort" label="Force Meter Value."             width="75px">
            <options>
                <option label="True"  value="ForceMeterValue"/>
                <option label="False" value="SkipForce"      default="true"/>
            </options>
        </param>

        <param field="Mode2" label="Date 1 Monitor."    width="120px" default="Water> 1 jan 2020"/>

        <param field="Mode3" label="Date 1 m³."         width="120px" default="2.468"/>

        <param field="Mode4" label="Date 2 Monitor."    width="120px" default="Water> 17 mrt 2020"/>

        <param field="Mode5" label="Date 2 m³."         width="120px" default="1.234"/>

        <param field="Username" label="Username."       width="120px" default="admin"/>

        <param field="Password" label="Password."       width="120px" default="domoticz" password="true"/>

        <param field="Mode6" label="Debug."             width="75px">
            <options>
                <option label="True"  value="Debug"/>
                <option label="False" value="Normal"    default="true"/>
            </options>
        </param>
    </params>
</plugin>
"""
import Domoticz
import datetime

# Prepare some global variables

StartupOK=0
HomeFolder=''

ImageDictionary={}

HeartbeatInterval= 10   # 10 seconds
#HeartbeatCountMax= 30   # 30 * Heartbeat = 300 seconds is 5 minutes, not too low to refresh Monitors with own values to avoid time outs and keep nice graphs
HeartbeatCountMax= 2   # 2 * Heartbeat = 20, not too low to refresh Monitors with own values to avoid time outs and keep nice graphs
HeartbeatCounter =  1   # counts down from Max to 1 before actual refresh; start with 1 which forces an immediate refresh after startup

# lock mechanism parameters onHeartbeat and WaterTrigger ( they are not allowed to update monitors at same time ;-)

onHeartbeatLock=0
WaterTriggerLock=0

IPPort=0        # plugin finds right value

GPIOpin=0       # plugin finds right value
LocalHostInfo=''

Water_id=1

WaterDate1_id=2
WaterDate1Value=0.0 # plugin finds right value

WaterDate2_id=3
WaterDate2Value=0.0 # plugin finds right value

WaterUsage_id=4

StartTime = datetime.datetime.now()

class BasePlugin:
    enabled = False
    def __init__(self):
        #self.var = 123
        return

# --------------------------------------------------------------------------------------------------------------------------------------------------------

    def onStart(self):

        global StartupOK
        
        global HeartbeatInterval
        global HomeFolder
        global GPIOpin
        global WaterDate1Value
        global WaterDate2Value

        global LocalHostInfo

        self.pollinterval = HeartbeatInterval  #Time in seconds between two polls

        if Parameters["Mode6"] == 'Debug':
            self.debug = True
            Domoticz.Debugging(1)
            DumpConfigToLog()
        else:
            Domoticz.Debugging(0)

        Domoticz.Log("onStart called")
        
        try:
#
# Set some globals variables to right values
#            
            RoomName        =str(Parameters['Name'])
            HomeFolder      =str(Parameters["HomeFolder"])
            Username        =str(Parameters["Username"])
            Password        =str(Parameters["Password"])
            GPIOpin         =int(Parameters["Port"])
            CreateValue     =float(Parameters["Address"])
            WaterName       =str(Parameters["Mode1"])
            WaterDate1Name  =str(Parameters["Mode2"])
            WaterDate1Value =float(Parameters["Mode3"])
            WaterDate2Name  =str(Parameters["Mode4"])
            WaterDate2Value =float(Parameters["Mode5"])

            LocalHostInfo     = "https://"+Username+":"+Password+"@"+GetDomoticzIP()+":"+GetDomoticzHTTPSPort()

            StartupOK = ImportImages()

            if StartupOK == 1:


# Create Monitors / Update Monitor Names

                CreateDevice(Water_id,WaterName,"Custom",'Water','Water Meter Start : '+str(CreateValue)+' m³','m³',CreateValue)

                if Parameters["SerialPort"] == "ForceMeterValue" :
                    Domoticz.Log("Force Meter Value to : " + str(CreateValue) )
                    Devices[Water_id].Update( nValue=0, sValue=str(CreateValue) )
                    

                CreateDevice(WaterDate1_id,WaterDate1Name,"Custom",'Water','Water Meter : '+str(WaterDate1Value)+' m³','m³',CreateValue-WaterDate1Value)

                CreateDevice(WaterDate2_id,WaterDate2Name,"Custom",'Water','Water Meter : '+str(WaterDate2Value)+' m³','m³',CreateValue-WaterDate2Value)

#def CreateDevice(deviceunit,devicename,devicetype,devicelogo="",devicedescription="",sAxis="",InitialValue=0.0):

                CreateDevice(WaterUsage_id,"Water","Custom",'Water','Water Meter Liters / minute','l/min',0.0)
#
# (Re-)Create Room
#
                Recreate=False
                RoomIdx=CreateRoom( RoomName, Recreate)
                if (RoomIdx == 0):
                    StartupOK = 0
#
# Add all items from configuration file to Room if not already in
#
# Note that the order in the config file determines the order in the room
#
                if (StartupOK == 1):

                    Domoticz.Log('CreateDevices put devices in room')

                    Addition = AddToRoom(RoomIdx,Devices[Water_id].ID)
                    if (Addition == 0):
                        StartupOK = 0
                    Addition = AddToRoom(RoomIdx,Devices[WaterDate1_id].ID)
                    if (Addition == 0):
                        StartupOK = 0
                    Addition = AddToRoom(RoomIdx,Devices[WaterDate2_id].ID)
                    if (Addition == 0):
                        StartupOK = 0
                    Addition = AddToRoom(RoomIdx,Devices[WaterUsage_id].ID)
                    if (Addition == 0):
                        StartupOK = 0
                
                if (StartupOK == 1):
# Setup GPIO

#            GPIOSetupStatus = GPIOSetup('Start')
                    StartShellProcess()
                    GPIOSetupStatus = 1

                    if GPIOSetupStatus == 1:

# Setup was fine so enable onHeartbeat function
                                
                        Domoticz.Heartbeat(HeartbeatInterval)

            if (StartupOK == 1):
                Domoticz.Debug('onStartup OK')
            else:
                Domoticz.Log('ERROR starting up')
                
        except:

            StartupOK = 0

            Domoticz.Log('ERROR starting up')

# --------------------------------------------------------------------------------------------------------------------------------------------------------

    def onStop(self):
        Domoticz.Log("onStop called")

# Setup GPIO

#        GPIOSetupStatus = GPIOSetup('Stop')
        StopShellProcess()

# --------------------------------------------------------------------------------------------------------------------------------------------------------

    def onConnect(self, Connection, Status, Description):
        Domoticz.Log("onConnect called")

    def onMessage(self, Connection, Data):
        Domoticz.Log("onMessage called")

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Log("onCommand called")
                    
    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self, Connection):
        Domoticz.Log("onDisconnect called")

# --------------------------------------------------------------------------------------------------------------------------------------------------------
    
    def onHeartbeat(self):
        
        global HeartbeatCounter
        global WaterTriggerLock
        global onHeartbeatLock
        
        if StartupOK == 1:
            
#            Domoticz.Log("onHeartbeat called "+str(HeartbeatCounter))

            if HeartbeatCounter == 1:

                onHeartbeatLock = 1
            
                if WaterTriggerLock == 0: # WaterTrigger did not lock before onHeartbeat so update this time
                
                    Domoticz.Debug('Refresh Water Meter Monitors')

                    Devices[Water_id].Update(     nValue=0, sValue=Devices[Water_id].sValue)
                    Devices[WaterDate1_id].Update(nValue=0, sValue=str(    round(float(Devices[Water_id].sValue) - WaterDate1Value, 3)    ) )
                    Devices[WaterDate2_id].Update(nValue=0, sValue=str(    round(float(Devices[Water_id].sValue) - WaterDate2Value, 3)    ) )
                    Devices[WaterUsage_id].Update(nValue=0, sValue=Devices[WaterUsage_id].sValue)
#                    Devices[WaterUsage_id].Update(nValue=0, sValue='0.0'                                                                    )
            
                HeartbeatCounter = HeartbeatCountMax

                onHeartbeatLock = 0
            
            else:

                HeartbeatCounter = HeartbeatCounter - 1
            
# --------------------------------------------------------------------------------------------------------------------------------------------------------

global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

    # Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return
    
# --------------------------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------  Basic Management Routines  -----------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------------

def GetDomoticzIP():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

# --------------------------------------------------------------------------------------------------------------------------------------------------------

def GetDomoticzHTTPSPort():

    try:
        import subprocess
    except:
        Domoticz.Log("python3 is missing module subprocess")

    try:
        import time
    except:
        Domoticz.Log("python3 is missing module time")

    try:
        Domoticz.Debug('GetDomoticzHTTPSPort check startup file')
        pathpart=Parameters['HomeFolder'].split('/')[3]
        searchfile = open("/etc/init.d/"+pathpart+".sh", "r")
        for line in searchfile:
            if ("-sslwww" in line) and (line[0:11]=='DAEMON_ARGS'):
                HTTPSPort=str(line.split(' ')[2].split('"')[0])
                HTTPSPort = HTTPSPort.replace('\\n','') # remove EOL
        searchfile.close()
        Domoticz.Debug('GetDomoticzHTTPSPort looked in: '+"/etc/init.d/"+pathpart+".sh"+' and found port: '+HTTPSPort)
    except:
        Domoticz.Debug('GetDomoticzHTTPSPort check running process')
        command='ps -ef | grep domoticz | grep sslwww | grep -v grep | tr -s " "'
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

        timeouts=0

        result = ''
        while timeouts < 10:
            p_status = process.wait()
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                HTTPSPort=str(output)
                HTTPSPort = HTTPSPort[HTTPSPort.find('-sslwww'):]
                HTTPSPort = HTTPSPort[HTTPSPort.find(' ')+1:]
                HTTPSPort = HTTPSPort[:HTTPSPort.find(' ')]
                HTTPSPort = HTTPSPort.replace('\\n','') # remove EOL
            else:
                time.sleep(0.2)
                timeouts=timeouts+1
        Domoticz.Debug('GetDomoticzHTTPSPort looked at running process and found port: '+HTTPSPort)

    return HTTPSPort

# --------------------------------------------------------------------------------------------------------------------------------------------------------

def GetImageDictionary():

    import json
    import requests

    try:
        mydict={}

        url=LocalHostInfo+'/json.htm?type=command&param=custom_light_icons'

        response=requests.get(url, verify=False)
        data = json.loads(response.text)
        for Item in data['result']:
            mydict[str(Item['imageSrc'])]=int(Item['idx'])

    except:
        mydict={}

    return mydict

# --------------------------------------------------------------------------------------------------------------------------------------------------------

def ImportImages():
#
# Import ImagesToImport if not already loaded
#
    try :
        import glob
    except:
        Domoticz.Log("python3 is missing module glob")

    global ImageDictionary

    MyStatus=1

    ImageDictionary=GetImageDictionary()

    if ImageDictionary == {}:
        Domoticz.Log("Please modify your setup to have Admin access. (See Hardware setup page of this plugin.)")
        MyStatus = 0
    else:

        for zipfile in glob.glob(HomeFolder+"CustomIcons/*.zip"):
            importfile=zipfile.replace(HomeFolder,'')
            try:
                Domoticz.Image(importfile).Create()
                Domoticz.Debug("ImportImages Imported/Updated icons from "  + importfile)
            except:
                MyStatus = 0
                Domoticz.Log("ImportImages ERROR can not import icons from "  + importfile)

        if (MyStatus == 1) :
            ImageDictionary=GetImageDictionary()
            Domoticz.Debug('ImportImages Oke')

    return MyStatus

# --------------------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------  Device Creation Routines  ------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------------

def CreateDevice(deviceunit,devicename,devicetype,devicelogo="",devicedescription="",sAxis="",InitialValue=0.0):
    
    if deviceunit not in Devices:

        if ImageDictionary == {}:
            firstimage=0
            firstimagename='NoImage'
            Domoticz.Log("ERROR I can not access the image library. Please modify the hardware setup to have the right Username and Password.")      
        else:
            firstimage=int(str(ImageDictionary.values()).split()[0].split('[')[1][:-1])
            firstimagename=str(ImageDictionary.keys()).split()[0].split('[')[1][1:-2]
            Domoticz.Debug("First image id: " + str(firstimage) + " name: " + firstimagename)

        if firstimage != 0: # we have a dictionary with images and hopefully also the image for devicelogo

            try:

                deviceoptions={}
                deviceoptions['Custom']="1;"+sAxis
                Domoticz.Device(Name=devicename, Unit=deviceunit, TypeName=devicetype, Used=1, Image=ImageDictionary[devicelogo], Description=devicedescription).Create()
                Devices[deviceunit].Update(nValue=Devices[deviceunit].nValue, sValue=str(InitialValue))
                Domoticz.Log("Created device : " + devicename + " with '"+ devicelogo + "' icon and options "+str(deviceoptions)+' Value '+str(InitialValue))
            except:

# when devicelogo does not exist, use the first image found, (TypeName values Text and maybe some others will use standard images for that TypeName.)

                try:
                    Domoticz.Device(Name=devicename, Unit=deviceunit, TypeName=devicetype, Used=1, Image=firstimage, Description=devicedescription).Create()
                    Devices[deviceunit].Update(nValue=Devices[deviceunit].nValue, sValue=str(InitialValue))
                    Domoticz.Log("Created device : " + devicename+ " with '"+ firstimagename + "' icon and Value "+str(InitialValue))
                except:
                    Domoticz.Log("ERROR Could not create device : " + devicename)
#
# Devices are created with as prefix the name of the Hardware device as you named it during adding your hardware
# The next replaces that prefix, also after every restart so names are fixed
#
    try:

# Note that deviceoptions needs to be a python dictionary so first create a dictionary and fill it with 1 entry

        deviceoptions={}
        deviceoptions['Custom']="1;"+sAxis

        NewName = devicename
        Devices[deviceunit].Update(nValue=Devices[deviceunit].nValue, sValue=Devices[deviceunit].sValue, Name=NewName, Options=deviceoptions, Description=devicedescription)
    except:
        dummy=1
def CreateRoom(RoomName, Recreate):

    try:
        import json
    except:
        Domoticz.Log("python3 is missing module json")

    try:
        import requests
    except:
        Domoticz.Log("python3 is missing module requests")

    idx=0

    try:

        Domoticz.Debug('Check if Room Exists')

        url=LocalHostInfo+'/json.htm?type=command&param=getplans&order=name&used=true'
        Domoticz.Debug('Check Room '+url)
        response=requests.get(url, verify=False)
        data = json.loads(response.text)

        if 'result' in data.keys():
            for Item in data['result']:
                if str(Item['Name']) == RoomName:
                    idx=int(Item['idx'])
                    Domoticz.Debug('Found Room '+RoomName+' with idx '+str(idx))

        if (idx != 0) and Recreate :
            url=LocalHostInfo+'/json.htm?idx='+str(idx)+'&param=deleteplan&type=command'
            Domoticz.Log('Delete Room '+url)
            response=requests.get(url, verify=False)
            idx = 0

        if idx == 0 :
            url=LocalHostInfo+'/json.htm?name='+RoomName+'&param=addplan&type=command'
            Domoticz.Log('Create Room '+url)
            response=requests.get(url, verify=False)
            data = json.loads(response.text)
            Domoticz.Log('CreateRoom Created Room'+str(data))
            idx=int(data['idx'])
    except:
        Domoticz.Log('ERROR CreateRoom Failed')
        idx=0

    Domoticz.Debug('CreateRoom status should not be 0 : '+str(idx))

    return idx
# --------------------------------------------------------------------------------------------------------------------------------------------------------
def AddToRoom(RoomIDX,ItemIDX):

    try:
        import json
    except:
        Domoticz.Log("python3 is missing module json")

    try:
        import requests
    except:
        Domoticz.Log("python3 is missing module requests")

    status=1

    try:
        url=LocalHostInfo+'/json.htm?activeidx='+str(ItemIDX)+'&activetype=0&idx='+str(RoomIDX)+'&param=addplanactivedevice&type=command'
        Domoticz.Debug(url)
        response=requests.get(url, verify=False)
        data = json.loads(response.text)
    except:
        Domoticz.Log('ERROR AddRoom Failed')
        status=0

    Domoticz.Debug('AddToRoom status should not be 0 : '+str(status))

    return status
# --------------------------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------  Hardware Routines --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------------

def GPIOSetup(action):

# when a changing edge is detected on port GPIOpin, regardless of whatever
# else is happening in the program, the callback function WaterTrigger will be run

    global GPIOpin
    
    try:
        import RPi.GPIO as GPIO

        GPIO.setmode(GPIO.BCM)              # set up BCM GPIO numbering

        if action == 'Start':
            GPIO.setwarnings(False)         # No warnings
            GPIO.setup(GPIOpin, GPIO.IN)    # Read output from sensor
            GPIO.add_event_detect(GPIOpin, GPIO.BOTH, callback=WaterTrigger, bouncetime=200)
            Domoticz.Log('....GPIOSetup added event handler')
        else:
            GPIO.remove_event_detect(GPIOpin)
            Domoticz.Log('....GPIOSetup removed event handler')
        
        return 1
        
    except:
        
        Domoticz.Log('GPIOSetup can not '+action)
        
        return 0

# --------------------------------------------------------------------------------------------------------------------------------------------------------

def WaterTrigger(channel):

    global GPIOpin
    global WaterTriggerLock
    global onHeartbeatLock
    global StartTime

    import time
    import datetime

#    Domoticz.Debug('WaterTrigger called for channel '+str(channel))

    StopTime = datetime.datetime.now()
    
    Minutes = (StopTime-StartTime).total_seconds() / 60

    StartTime = StopTime

    LitresPerMinute = str( round(1 / Minutes,2) )
        
#    Domoticz.Log("Minutes : "+ str(round(Minutes , 2)) + " Litres / minute : "+LitresPerMinute)

    try:
        import RPi.GPIO as GPIO

        if GPIO.input(GPIOpin):     # if GPIOpin == 1
            
            WaterTriggerLock=1

            while onHeartbeatLock == 1:
                time.sleep(1/10)

#            Domoticz.Debug('Add 1 liter :-) from channel '+str(channel))

            Devices[Water_id].Update(     nValue=0, sValue=str(    round(float(Devices[Water_id].sValue) + 0.001,3)               ) )
            Devices[WaterDate1_id].Update(nValue=0, sValue=str(    round(float(Devices[Water_id].sValue) - WaterDate1Value, 3)    ) )
            Devices[WaterDate2_id].Update(nValue=0, sValue=str(    round(float(Devices[Water_id].sValue) - WaterDate2Value, 3)    ) )
            Devices[WaterUsage_id].Update(nValue=0, sValue=LitresPerMinute                                                          )

            WaterTriggerLock=0

    except:
        dummy = 1
#        Domoticz.Log('WaterTrigger can not update for channel '+str(channel))

# --------------------------------------------------------------------------------------------------------------------------------------------------------

def StartShellProcess():

#GPIOpin

#Water_id=1

#WaterDate1_id=2
#WaterDate1Value=0.0 # plugin finds right value

#WaterDate2_id=3
#WaterDate2Value=0.0 # plugin finds right value

#WaterUsage_id=4

    import subprocess
    import shlex
    import time

    command = HomeFolder + 'spawn_bash.sh watermeter.sh'
    command = command + ' '  + str(GPIOpin)
    command = command + ' '  + str(Devices[Water_id].ID)
    command = command + ' '  + str(Devices[WaterDate1_id].ID)
    command = command + ' '  + str(Devices[WaterDate2_id].ID)
    command = command + ' '  + str(Devices[WaterUsage_id].ID)

    Domoticz.Log(command)

    if 1 == 1 :
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

        timeouts=0

        result = ''
        while timeouts < 10:
            p_status = process.wait()
#            Domoticz.Log('Command: '+command)
            output = process.stdout.readline()
#            Domoticz.Log('Output: '+str(output))
            if output == '' and process.poll() is not None:
                break
            if output:
                result=str(output.strip())
                timeouts=10
            else:
                time.sleep(0.2)
                timeouts=timeouts+1

    return

# --------------------------------------------------------------------------------------------------------------------------------------------------------

def StopShellProcess():

#GPIOpin

#Water_id=1

#WaterDate1_id=2
#WaterDate1Value=0.0 # plugin finds right value

#WaterDate2_id=3
#WaterDate2Value=0.0 # plugin finds right value

#WaterUsage_id=4

    import subprocess
    import shlex
    import time

    command = '/usr/bin/killall -9 inotifywait ; sleep 2; /usr/bin/killall -9 watermeter.sh'

    Domoticz.Log(command)

    if 1 == 1 :
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

        timeouts=0

        result = ''
        while timeouts < 10:
            p_status = process.wait()
#            Domoticz.Log('Command: '+command)
            output = process.stdout.readline()
#            Domoticz.Log('Output: '+str(output))
            if output == '' and process.poll() is not None:
                break
            if output:
                result=str(output.strip())
                timeouts=10
            else:
                time.sleep(0.2)
                timeouts=timeouts+1

    return

# --------------------------------------------------------------------------------------------------------------------------------------------------------
