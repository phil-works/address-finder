#
# clearNameSearchOwner.sh
# if you're the owner then use this script to clear a users search. 


source ~/config/envar

FOR_ACCT=$1
MSG=$2

${gcmd} app call --app-id ${ADDRESS_FINDER_ID} --app-arg "str:ClearNameSearch" --app-arg "str:${MSG}" --app-account ${FOR_ACCT} -f $OWNER

goal app read --local --app-id ${ADDRESS_FINDER_ID} --from ${FOR_ACCT}

