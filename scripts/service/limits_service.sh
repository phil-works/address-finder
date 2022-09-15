while [[ 1 == 1 ]]
do
        if [[ -f "./limits_service.stop"  ]]

        then
                 rm ./limits_service.stop
                 exit 0
        fi

        START=`date`
        ./check_limits.py
        END=`date`
        SECS=$(echo $(date -d "$END" +%s) - $(date -d "$START" +%s) | bc)
        echo "Time processing: $SECS"
	echo "Sleeping 5 mins..."
	sleep 300
done

