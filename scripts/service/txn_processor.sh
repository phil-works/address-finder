#!/bin/bash
# txn_processor.sh
#
#

LIMIT=2
WD=$HOME/address-finder
SDIR=${WD}/scripts/service

function crc () {
RC=$1
if [[ $RC -ne 0 ]]
then
	echo "Looks like there was an error... moving txn file to error directory."
	mv $WD/txn_files/${TXN_FILE} $WD/txn_errs/${TXN_FILE}
fi

}

echo "$(date "+%F %H:%M:%S"): Starting..."
while [ 1 -eq 1 ]
do
        if [ -f "$WD/status/txn_processor.stop"  ]
        then
		 echo "stopped" > $WD/status/txn_processor.status
                 rm $WD/status/txn_processor.stop
                 exit 0
        fi

	echo "running" > $WD/status/txn_processor.status

	FILE_LIST=`ls $WD/txn_files/`
        for TXN_FILE in $FILE_LIST
	do
		case $TXN_FILE in
			app-optin*)
				echo "$(date "+%F %H:%M:%S"): App Opt-in"
				$SDIR/process_app_opt_in.py $TXN_FILE
				crc $?
				;;
			clearnamesearch*)
				echo "$(date "+%F %H:%M:%S"): Clear name search"
				$SDIR/process_clear_search.py $TXN_FILE
				crc $?
				;;
			findmethisname*)
				echo "$(date "+%F %H:%M:%S"): Search Request"
				$SDIR/process_find_this_name.py $TXN_FILE
				crc $?
				;;
			af_rekey*)
				echo "$(date "+%F %H:%M:%S"): Address Finder Rekey"
				$SDIR/process_algo_rekey.py $TXN_FILE
				crc $?
				;;
			af_contest*)
				echo "$(date "+%F %H:%M:%S"): Declare Contest Winner"
				$SDIR/process_af_contest.py $TXN_FILE
				crc $?
				;;
			algo_clear_name_search*)
				echo "$(date "+%F %H:%M:%S"): Algo Clear Name Search"
				$SDIR/process_algo_clear_name_search.py $TXN_FILE
				crc $?
				;;
			contest_guess*)
				echo "$(date "+%F %H:%M:%S"): Contest Guess"
				$SDIR/process_contest_guess.py $TXN_FILE
				crc $?
				;;
			pay*)
				echo "$(date "+%F %H:%M:%S"): Payment WoooHooo!"
				rm $SDIR/txn_files/${TXN_FILE}
				;;
			*)
				echo "$(date "+%F %H:%M:%S"): found ${TXN_FILE} but don't know what to do"
				mv $WD/txn_files/${TXN_FILE} $WD/txn_errs/${TXN_FILE}
				;;
		esac
	done

	#echo "Sleeping 1..."
	sleep 1
done 
