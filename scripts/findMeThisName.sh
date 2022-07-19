#
# findMeThisName.sh
# this script will setup search.
#


source ~/config/envar

FROM_ACCT=$1
SEARCH_TYPE=$2
DESIRED_NAME=$3
NAME_POSI=$4


${gcmd} clerk send -a 50000 -f ${FROM_ACCT}  -t "${OWNER}" -o unsignedtx1.tx
${gcmd} app call --app-id ${ADDRESS_FINDER_ID} --app-arg "str:FindMeThisName" --app-arg "str:${SEARCH_TYPE}" --app-arg "str:${DESIRED_NAME}" --app-arg "str:${NAME_POSI}" -f $FROM_ACCT -o unsignedtx2.tx

cat unsignedtx1.tx unsignedtx2.tx > combinedtransactions.tx
${gcmd} clerk group -i combinedtransactions.tx -o groupedtransactions.tx
${gcmd} clerk split -i groupedtransactions.tx -o split.tx
${gcmd} clerk sign -i split-0.tx -o signout-0.tx
${gcmd} clerk sign -i split-1.tx -o signout-1.tx
cat signout-0.tx signout-1.tx > signout.tx
${gcmd} clerk rawsend -f signout.tx


goal app read --local --guess-format --app-id ${ADDRESS_FINDER_ID} --from ${FROM_ACCT}

rm *.tx

