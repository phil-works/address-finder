#
# setOptions.sh
# Will setup the options for the address finder.
#


source ~/config/envar

${gcmd} app call --app-id ${ADDRESS_FINDER_ID} --app-arg "str:UpdateGlobals" --app-arg "str:Rekey,Save for Game" --app-arg "str:Front,Any,End" --app-arg "int:3000"  -f $OWNER


goal app read --global --guess-format --app-id ${ADDRESS_FINDER_ID}

