#
# wait_for_status.sh
#
#

export APP=$1
export DESIRED_STATUS=$2

export OUR_FILE=$HOME/address-finder/status/${APP}.status


export THE_STATUS=`cat $OUR_FILE`

while [ $THE_STATUS != $DESIRED_STATUS ]
do
	echo "Waiting for ${APP}'s status to change from ${THE_STATUS} to ${DESIRED_STATUS}..."
	sleep 10
	THE_STATUS=`cat $OUR_FILE`
done 

echo "Done! ${APP}'s status is now ${DESIRED_STATUS}..."
