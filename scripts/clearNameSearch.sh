#
# clearNameSearch.sh 
#


source ~/config/envar

FOR_ACCT=$1

${gcmd} app call --app-id ${ADDRESS_FINDER_ID} --app-arg "str:ClearNameSearch" -f ${FOR_ACCT}


goal app read --local --guess-format --app-id ${ADDRESS_FINDER_ID} --from ${FOR_ACCT}

