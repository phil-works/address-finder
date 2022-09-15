#
# clearNameSearchOwner.sh
# 
#


source ~/config/envar

FOR_ACCT=$1

${gcmd} app call --app-id ${ADDRESS_FINDER_ID} --app-arg "str:ClearNameSearch" --app-arg "str:Cleared by System..." --app-account ${FOR_ACCT} -f $OWNER

goal app read --global --app-id $ADDRESS_FINDER_ID --guess-format

