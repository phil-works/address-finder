#!/usr/bin/env -S python3 -u
import sys
import json
import mysql.connector
import json
import yaml
import os
import MySQLdb
import re
import base64
from algosdk.v2client import indexer
from algosdk.error import AlgodHTTPError, IndexerHTTPError


TXN_FILE= sys.argv[1]

#
# Setup DB
#
with open(os.environ['HOME'] + "/config/godogwin-net.yaml", "r") as stream:
    try:
        gdwcfg = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

# setup database connector
mydb = mysql.connector.connect(
  host=gdwcfg["gdwdb"]["host"],
  user=gdwcfg["gdwdb"]["user"],
  password=gdwcfg["gdwdb"]["pwd"],
  database=gdwcfg["gdwdb"]["algodb"]
)

mycursor = mydb.cursor()
#mycurdict = mydb.cursor(dictionary=True)

INDEXER_ADDRESS = gdwcfg["indexer_address"]
ALGOD_ADDRESS = gdwcfg["algod_address"]
ALGOD_TOKEN = gdwcfg["algod_token"]
HEALTHCHECK = gdwcfg["healthcheck_url"]
header = {'X-Api-key': ALGOD_TOKEN}

indexer_client = indexer.IndexerClient(
    indexer_token=ALGOD_TOKEN,
    indexer_address=INDEXER_ADDRESS,
    headers=header
)

# Set the gloabal services config file.
services_config_file = gdwcfg["services_config_file"]

with open(services_config_file, "r") as fp:
    try:
        gd_data = yaml.safe_load(fp)
    except yaml.YAMLError as exc:
        print(exc)

txn_file_dir = gd_data["txn_processor"]["txn_file_dir"] #"/home/godogdev/address-finder/txn_files/"
with open(txn_file_dir + TXN_FILE, "r") as jf:
        txn_data = json.load(jf)

#print(txn_data["sender"] + " " + str(txn_data["confirmed-round"]))

# Get the payment amount. 
# curl http://127.0.0.1:8980/v2/accounts/V32DXG3X56ARR6IDDEU65Y2U5PURF2T7S6QOHZQ6C5ANT35QNGIYIGGJCY/transactions?tx-type=pay\&min-round=1297241\&max-round=1297241
def search_algo_calls(indexer_client: indexer.IndexerClient, the_sender, the_rnd):
    nexttoken = ""
    the_type = "pay"
    numtx = 1
    calls = []
    while numtx > 0:
        result = indexer_client.search_transactions(
            limit=1000,
            next_page=nexttoken,
            txn_type=the_type,
            address=the_sender,
            #addressr_role="sender",
            min_round=the_rnd,
            max_round=the_rnd
        )
        calls += result['transactions']
        numtx = len(result['transactions'])
        #print("Number of Txs: " + str(numtx))
        if numtx > 0:
            # pointer to the next chunk of requests
            nexttoken = result['next-token']
    return calls

payments = search_algo_calls(indexer_client, txn_data["sender"], txn_data["confirmed-round"])

for payment in payments:
    if payment["payment-transaction"]["receiver"] == gd_data["address-finder"]["contract_address"]:
        our_payment = payment["payment-transaction"]["amount"]


#print(our_payment)
priority = our_payment - gd_data["address-finder"]["min-fee"] 
if priority == 0:
    priority = 1

app_tx = txn_data["application-transaction"]
app_args = app_tx["application-args"]
request_type = str(base64.b64decode(app_args[1]),'ascii')
requested_tx = str(base64.b64decode(app_args[2]),'ascii')
requested_pos = str(base64.b64decode(app_args[3]),'ascii')

print(requested_tx)

if not re.match("^[A-Za-z0-8]*$", requested_tx):
    print("Not good.. have bad characters")
    # start clear name search process
    txn_data["requestor"] = txn_data["sender"]
    txn_data["status_text"] = "Invalid Name Requested"
    with open(txn_file_dir + "algo_clear_name_search." + txn_data["sender"] + ".txt", "w") as f:
        json.dump(txn_data, f)

    os.remove(txn_file_dir + TXN_FILE)
    sys.exit()


sql = "INSERT into algoaddress.search_requests (type, text, requestor, priority, position, txn_no, requested_dt) values (%s, UPPER(%s), %s, %s, %s, %s, %s)"
vals = (request_type, requested_tx, txn_data["sender"], priority, requested_pos, txn_data["id"], txn_data["round-time"])

#print("Vals: " + str(vals))

try:
    try:
        mycursor.execute(sql,vals)
        mydb.commit()
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print(e)

finally:
    mydb.close()

os.remove(txn_file_dir + TXN_FILE)
