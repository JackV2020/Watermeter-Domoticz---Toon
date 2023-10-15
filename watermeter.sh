#!/bin/bash

#https://raspberrypi.stackexchange.com/questions/89072/is-there-a-way-to-use-interrupt-driven-gpio-input-through-the-sysfs-interface-wi
#https://www.linuxtut.com/en/bc9c8941dc28c263a969/
#https://www.howtogeek.com/814925/linux-signals-bash/

# sudo apt-get install inotify-tools  -y

# load a sane environment
. /etc/profile

debug=false

BASE_GPIO_PATH="/sys/class/gpio"
GPIO=$1
WaterIdx1=$2
WaterIdx2=$3
WaterIdx3=$4
WaterIdx4=$5

# myLocation=$(dirname -- "$(readlink -f "${BASH_SOURCE}")")

if [ "x$6" != "x" ]
then
    debug=true
fi

graceful_shutdown()
{
  echo -e "\nUnexporting : " $GPIO
  unexportPin $GPIO
  exit
}

trap - SIGINT
trap - SIGQUIT
trap - SIGTERM

trap graceful_shutdown SIGINT SIGQUIT SIGTERM SIGKILL

exportCheck()
{
  if [ -e $BASE_GPIO_PATH/gpio$1 ]; then
    echo "1"
  else
    echo "0"
  fi
}

exportPin()
{
  if [ ! -e $BASE_GPIO_PATH/gpio$1 ]; then
    echo "$1" > $BASE_GPIO_PATH/export
  fi
}

unexportPin()
{
  if [ -e $BASE_GPIO_PATH/gpio$1 ]; then
    echo "$1" > $BASE_GPIO_PATH/unexport
  fi
}

setOutput()
{
  echo "out" > $BASE_GPIO_PATH/gpio$1/direction
}

setInput()
{
  echo "in" > $BASE_GPIO_PATH/gpio$1/direction
}

setMode()
{
# edge : both | falling | raising
  if [ -e $BASE_GPIO_PATH/gpio$1 ]; then
    case "$2" in
    "both"|"falling"|"raising")
        sudo echo $2 > $BASE_GPIO_PATH/gpio$1/edge
        ;;
    *)
        echo error
        ;;
    esac
  fi
}

readPin()
{
  if [ -e $BASE_GPIO_PATH/gpio$1 ]; then
    cat $BASE_GPIO_PATH/gpio$1/value
  else
    echo "-1"
  fi
}

writePin()
{
  if [ -e $BASE_GPIO_PATH/gpio$1 ]; then
    echo "$2">$BASE_GPIO_PATH/gpio$1/value
  fi
}

readDomoticz()
{
#   echo  $( curl -s "http://localhost:8080/json.htm?type=devices&rid=$1"  | grep Data | cut -d "\"" -f 4 | cut -d " " -f 1)
   echo  $( curl -s "http://localhost:8080/json.htm?type=command&param=getdevices&rid=$1"  | grep Data | cut -d "\"" -f 4 | cut -d " " -f 1)
}

readDomoticzName()
{
#   echo  $( curl -s "http://localhost:8080/json.htm?type=devices&rid=$1"  | grep '"Name"' | cut -d "\"" -f 4 )
   echo  $( curl -s "http://localhost:8080/json.htm?type=command&param=getdevices&rid=$1"  | grep '"Name"' | cut -d "\"" -f 4 )
}

updateDomoticz()
{
    $debug && echo Update idx $1 value $2
    status=$(curl -s  "http://localhost:8080/json.htm?type=command&param=udevice&idx=$1&nvalue=0&svalue=$2" | grep status | cut -d "\"" -f 4 | cut -d " " -f 1)
}


thePPID=$(ps -ef | grep /sys/class/gpio/gpio$GPIO/value | grep -v grep | tr -s " " | cut -d " " -f 3)

if [ "x$thePPID" == "x" ]
then
    $debug && echo We have a clean start
else
    $debug && ps -ef | grep /sys/class/gpio/gpio
    thePID=$(ps -ef | grep /sys/class/gpio/gpio$GPIO/value | grep -v grep | tr -s " " | cut -d " " -f 2)
    $debug && echo We have to kill some $thePPID $thePID
    kill -SIGTERM $thePPID
    kill -SIGTERM $thePID
    $debug && echo Wait 3 seconds for cleanup
    sleep 3
fi

if [ 1 == 1 ]
then
    exportPin $GPIO
    setMode $GPIO falling
# Get initial WaterValue1
#    $debug && echo Reading initial data
#    WaterValue1=$(readDomoticz $WaterIdx1)

    lasttime=$(date +%s%3N)
    
    (trap exit SIGTERM ; sleep 60 ; updateDomoticz $WaterIdx4 0) &
    lastproc=$!
    sleeppid=$(ps -ef | grep "sleep" |  grep $lastproc | grep -v grep | tr -s " " | cut -d " " -f 2)

    while [ true ]
    do
        $debug && echo Waiting
        inotifywait -e modify /sys/class/gpio/gpio$GPIO/value >/dev/null 2>&1
        kill -9 $sleeppid

        time=$(date +%s%3N)
        difftime=$(echo $time - $lasttime | bc)
        lasttime=$time

        $debug && echo Reading last data
        WaterValue1=$(readDomoticz $WaterIdx1)
#        WaterValue2=$(readDomoticz $WaterIdx2) handled in Heartbeat
#        WaterValue3=$(readDomoticz $WaterIdx3) handled in Heartbeat
        $debug && echo Calculating
        WaterValue1=$( echo $WaterValue1 + 0.001 | bc )
        WaterValue4=$( echo "scale=7; 1 * 1000 * 60 / $difftime" | bc)
        $debug && echo Updating
        updateDomoticz $WaterIdx1 $WaterValue1
#        updateDomoticz $WaterIdx2 $WaterValue2 handled in Heartbeat
#        updateDomoticz $WaterIdx3 $WaterValue3 handled in Heartbeat
        updateDomoticz $WaterIdx4 $WaterValue4

        (trap exit SIGTERM ; sleep 300 ; echo "updater" ; updateDomoticz $WaterIdx4 0) &
        lastproc=$!
        sleeppid=$(ps -ef | grep "sleep" |  grep $lastproc | grep -v grep | tr -s " " | cut -d " " -f 2)

    done
    state=$(readPin $GPIO)
    echo $state
    unexportPin $GPIO
fi
