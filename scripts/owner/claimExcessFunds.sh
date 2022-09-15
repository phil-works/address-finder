#
# claimExcessFunds.sh
# 
#


source ~/config/envar

${gcmd} app call --app-id ${ADDRESS_FINDER_ID} --app-arg "str:ClaimExcessFunds" -f $OWNER 


goal app read --global --app-id ${ADDRESS_FINDER_ID} --guess-format

