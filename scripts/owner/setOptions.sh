#
# setOptions.sh
# Will setup the options for the address finder.
#


source ~/config/envar

${gcmd} app call --app-id ${ADDRESS_FINDER_ID} --app-arg "str:UpdateGlobals" --app-arg "str:,Rekey," --app-arg "str:,Front," --app-arg "int:103000"  -f $OWNER


goal app read --global --app-id ${ADDRESS_FINDER_ID} --guess-format

