#
# contestGuessUpdate.sh
#
#

source ~/config/envar

FROM_ACCT=$1
GUESS=$2

${gcmd} app call --app-id ${ADDRESS_FINDER_ID} --app-arg "str:ContestGuess" --app-arg "int:${GUESS}" -f $FROM_ACCT

goal app read --local --app-id ${ADDRESS_FINDER_ID} -f ${FROM_ACCT} --guess-format

rm *.tx
if [ -f *.tx.rej ]
then
	rm *.tx.rej
fi
