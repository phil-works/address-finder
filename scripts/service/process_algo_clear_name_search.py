#!/usr/bin/env -S python3 -u
import time
import base64
import mysql.connector
import json
import requests
import yaml
import os
import sys
from algosdk.v2client import algod, indexer
from algosdk.error import AlgodHTTPError, IndexerHTTPError
from algosdk.future import transaction
from algosdk import mnemonic, account, util, constants, encoding


TXN_FILE = sys.argv[1]

#
# Setup Configs
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


INDEXER_ADDRESS = gdwcfg["indexer_address"]
ALGOD_ADDRESS = gdwcfg["algod_address"]
ALGOD_TOKEN = gdwcfg["algod_token"]
HEALTHCHECK = gdwcfg["healthcheck_url"]
OWNER = gdwcfg["OWNER"]
OWNERPK = gdwcfg["OWNERPK"]
CONTRACT_ID = gd_data["address-finder"]["app_id"]

algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)

def clear_name_search(requestor, status_text):
    params = algod_client.suggested_params()
    params.flat_fee = constants.MIN_TXN_FEE 
    params.fee = 1000
    app_args = ("ClearNameSearch", status_text)
    accounts = (requestor,)
    unsigned_txn = transaction.ApplicationNoOpTxn(OWNER, params, CONTRACT_ID, app_args, accounts)
    signed_txn = unsigned_txn.sign(OWNERPK)
    txid = algod_client.send_transaction(signed_txn)
    # wait for confirmation 
    try:
        transaction.wait_for_confirmation(algod_client, txid, 4)  
    except Exception as err:
        print(err)
        return


clear_name_search( txn_data["requestor"], txn_data["status_text"])

os.remove(txn_file_dir + TXN_FILE)
