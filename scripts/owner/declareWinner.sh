#
# declareWinner.sh
# 
#


source ~/config/envar

FROM_ACCT=$1
WORD=$2

${gcmd} clerk send -a 1100000 -f ${FROM_ACCT} -t ${FROM_ACCT}  --rekey-to "${OWNER}" -o unsignedtx1.tx
${gcmd} app call --app-id ${ADDRESS_FINDER_ID} --app-arg "str:DeclareContestWinner" --app-arg "str:${WORD}" -f $OWNER -o unsignedtx2.tx

cat unsignedtx1.tx unsignedtx2.tx > combinedtransactions.tx
${gcmd} clerk group -i combinedtransactions.tx -o groupedtransactions.tx
${gcmd} clerk split -i groupedtransactions.tx -o split.tx
${gcmd} clerk sign -i split-0.tx -o signout-0.tx
${gcmd} clerk sign -i split-1.tx -o signout-1.tx
cat signout-0.tx signout-1.tx > signout.tx
${gcmd} clerk rawsend -f signout.tx


goal app read --global --app-id ${ADDRESS_FINDER_ID} --guess-format

rm *.tx
if [ -f *.tx.rej ]
then
	rm *.tx.rej
fi
