#
# setContestOptions.sh
# 
#


source ~/config/envar

WORDLIST=",PHLWRK,PHLWORK,PHILWRK,PHLWRKS,PHLWORKS,PHILWRKS,PHILWORK,PHILWORKS,"

${gcmd} app call --app-id ${ADDRESS_FINDER_ID} --app-arg "str:UpdateContestGlobals" --app-arg "int:1000000" --app-arg "int:130000" --app-arg "str:${WORDLIST}" --app-arg "str:Y"  -f $OWNER

goal app read --global --app-id ${ADDRESS_FINDER_ID} --guess-format

