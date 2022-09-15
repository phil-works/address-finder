#!/bin/bash
#
# Generate and mint the contract. 

source ~/config/envar

PYTHON=python3

PYTEAL_APPROVAL_PROG="./address-finder.py"
PYTEAL_CLEAR_PROG="./clear.py"
TEAL_APPROVAL_PROG="./vanity_contract.teal"
TEAL_CLEAR_PROG="./vanity_clear.teal"

# compile PyTeal into TEAL
"$PYTHON" "$PYTEAL_APPROVAL_PROG" > "$TEAL_APPROVAL_PROG"
"$PYTHON" "$PYTEAL_CLEAR_PROG" > "$TEAL_CLEAR_PROG"

# create app
APP_ID=$(
  ${gcmd} app create --creator "${OWNER}" \
    --approval-prog "$TEAL_APPROVAL_PROG" \
    --clear-prog "$TEAL_CLEAR_PROG" \
    --global-byteslices 5 \
    --global-ints 6 \
    --local-byteslices 4 \
    --local-ints 4 |
    grep Created |
    awk '{ print $6 }'
)
#echo "App ID = ${APP_ID}"

${gcmd} app info --app-id $APP_ID

