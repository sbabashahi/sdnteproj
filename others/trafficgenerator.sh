#!/bin/bash
# Author : Saeed
# generating random traffic
#

IP="10.0.0."    #IP Address of network
declare -r THRESHOLD=1000
while true
do
    dsthost=$(echo $RANDOM | cut -c1)  #dest Host
    dataVol=$(echo $RANDOM | cut -c1,2,3,4)  # Packet Volume
    if [ $dataVol -gt $THRESHOLD ]; then
        packet=$(echo $RANDOM | cut -c1)       #Number of packets elephent
    else
        packet=$(echo $RANDOM | cut -c1,2,3)  # Number of packets mouse
    fi
    sudo hping3 -c $packet -d $dataVol  $IP$dsthost #| grep "bytes from" | sed 's@:@@' | awk '{print $4,$7}' &
    sleep_time=$(echo $RANDOM | cut -c1)  # Sleep time between periods of sending
    sleep .$sleep_time #sleep until next period
done
