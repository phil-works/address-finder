#!/bin/bash

#date '+keyreg-teal-test start %Y%m%d_%H%M%S'

#set -e
#set -x
set -o pipefail
export SHELLOPTS
source ~/config/envar

gcmd="goal"

PYTHON=python3

PYTEAL_APPROVAL_PROG="./address-finder.py"
PYTEAL_CLEAR_PROG="./clear.py"
TEAL_APPROVAL_PROG="./address-finder_contract.teal"
TEAL_CLEAR_PROG="./clear_contract.teal"

# compile PyTeal into TEAL
"$PYTHON" "$PYTEAL_APPROVAL_PROG" > "$TEAL_APPROVAL_PROG"
"$PYTHON" "$PYTEAL_CLEAR_PROG" > "$TEAL_CLEAR_PROG"

# create app
APP_ID=$(
  ${gcmd} app create --creator "${OWNER}" \
    --approval-prog "$TEAL_APPROVAL_PROG" \
    --clear-prog "$TEAL_CLEAR_PROG" \
    --global-byteslices 2 \
    --global-ints 1 \
    --local-byteslices 4 \
    --local-ints 0 |
    grep Created |
    awk '{ print $6 }'
)
#echo "App ID = ${APP_ID}"

${gcmd} app info --app-id $APP_ID
