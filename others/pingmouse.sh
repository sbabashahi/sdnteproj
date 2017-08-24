#!/bin/bash
# Author : Saeed 
# generating random traffic
#
IP="10.0.0."
while true
do 
    sleep_time=`echo $RANDOM | cut -c1`
    for  i in {1..9}
    do
	    rand=`echo $RANDOM | cut -c1,2,3`
	    data=`echo $RANDOM | cut -c1,2,3,3,3` 
	    end=`echo $RANDOM | cut -c1` 
	    result=`echo "$end%2" | bc `
	    if [ $result -eq 0 ] ; then 
		   sudo hping3 -c $rand --faster -d $data  $IP$i & #  | grep "bytes from" | sed 's@:@@' | awk '{print $4,$7}' & 
	    else 
		    continue
	    fi
    done
    echo "Sleep Time is $sleep_time"
    sleep $sleep_time
done


