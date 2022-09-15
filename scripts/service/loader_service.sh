#!/bin/bash
# loader_service.sh
#
#

LIMIT=2
WD=$HOME/address-finder
while [ 1 -eq 1 ]
do
        if [ -f "$WD/status/load_looper.stop"  ]
        then
		 echo "stopped" > $WD/status/load_looper.status
                 rm $WD/status/load_looper.stop
                 exit 0
        fi

	while [ -f "$WD/status/load_looper.pause" ]
	do
		echo "Pausing for $(cat $WD/status/load_looper.pause)..."
		echo "paused" > $WD/status/load_looper.status
		sleep 10
	done

	echo "running" > $WD/status/load_looper.status

        FILE_COUNT=`ls -ltr $WD/new/ | wc -l`
        if [ $FILE_COUNT -lt $LIMIT ]
        then
                echo "Sleeping 1mins..."
                sleep 60
        else
		START=`date`
		$WD/scripts/service/load_filter.py
		END=`date`
		SECS=$(echo $(date -d "$END" +%s) - $(date -d "$START" +%s) | bc)
		echo "Time processing: $SECS"
	fi
done 
