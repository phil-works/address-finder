#!/bin/bash
# address_creation_service.sh
#
#

echo "Starting service with pid: $$"
WD=$HOME/address-finder
echo $$ > $WD/status/address_creation_service.pid
LIMIT=100
while [ 1 -eq 1 ]
do
	FILE_COUNT=`ls -ltr $WD/new/ | wc -l`
	if [ $FILE_COUNT -ge $LIMIT ]
	then
		echo "Sleeping 5mins..."
		sleep 600
	else

		START=`date`
		FTS=$(date +%Y%m%d%H%M%S)
		echo "Making file: address.$FTS.$$.txt ..."
		$WD/scripts/service/find_vanity.py > $WD/temp/address.$FTS.$$.txt
		mv $WD/temp/address.$FTS.$$.txt $WD/new/address.$FTS.$$.txt
		END=`date`
		SECS=$(echo $(date -d "$END" +%s) - $(date -d "$START" +%s) | bc)
		echo "Time processed: $SECS"
        	if [ -f "$WD/status/address_looper.stop"  ]
        	then
                	rm $WD/status/address_looper.stop
			rm $WD/status/address_creation_service.pid
                	exit 0
        	fi
	fi
        if [ -f "$WD/status/address_looper.stop"  ]
        then
                rm $WD/status/address_looper.stop
                rm $WD/status/address_creation_service.pid
                exit 0
        fi
done
