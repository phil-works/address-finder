#!/bin/bash
# match_processor_service.sh
#
#

WD=$HOME/address-finder
echo "running" > $WD/status/match_processor_service.status
while [ 1 -eq 1 ]
do
        if [ -f "$WD/status/match_processor_service.stop"  ]
        then
		 echo "stopped" > $WD/status/match_processor_service.status
                 rm $WD/status/match_processor_service.stop
                 exit 0
        fi

	$WD/scripts/service/match_processor.py

	echo "Sleeping 5..."
	sleep 5
done 
