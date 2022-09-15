#
# breakOut.sh
#
#

source ~/config/envar

FROMACT=$1
GUESS=$2
LOWACT=$3
HIGHACT=$4


${gcmd} app call --app-id ${ADDRESS_FINDER_ID} --app-arg "str:BreakOut" --app-arg "int:${GUESS}" --app-account $LOWACT --app-account $HIGHACT -f $FROMACT


goal app read --local --app-id ${ADDRESS_FINDER_ID} -f ${FROMACT} --guess-format
