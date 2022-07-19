#
# claimExcessFunds.sh
# balance must be over 100000 in order to claim else you get a "you're broke" msg. 


source ~/config/envar

${gcmd} account balance --address ${OWNER}
${gcmd} app call --app-id ${ADDRESS_FINDER_ID} --app-arg "str:ClaimExcessFunds" -f $OWNER
${gcmd} account balance --address ${OWNER}

