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
from algosdk import mnemonic, account, util, constants

TXN_FILE= sys.argv[1]

#
# Setup Configs
#
with open(os.environ['HOME'] + "/config/godogwin-net.yaml", "r") as stream:
    try:
        gdwcfg = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)


# setup database connector
#mydb = mysql.connector.connect(
#  host=gdwcfg["gdwdb"]["host"],
#  user=gdwcfg["gdwdb"]["user"],
#  password=gdwcfg["gdwdb"]["pwd"],
#  database=gdwcfg["gdwdb"]["algodb"]
#)

#mycursor = mydb.cursor()
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

algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)

def send_primer_to_rekey(rekey_address):
     # build transaction
    params = algod_client.suggested_params()
    # comment out the next two (2) lines to use suggested fees
    params.flat_fee = constants.MIN_TXN_FEE 
    params.fee = 1000
    amount = 101000
    unsigned_txn = transaction.PaymentTxn(OWNER, params, rekey_address, amount, None, None)
    signed_txn = unsigned_txn.sign(OWNERPK)
    txid = algod_client.send_transaction(signed_txn)
    # wait for confirmation 
    try:
        transaction.wait_for_confirmation(algod_client, txid, 4)  
    except Exception as err:
        print(err)
        return


def rekey_to_requestor(rekey_address, rekey_pk, requestor):
    params = algod_client.suggested_params()
    params.flat_fee = constants.MIN_TXN_FEE 
    params.fee = 1000
    unsigned_txn = transaction.PaymentTxn(rekey_address, params, rekey_address, 0, 0, None, None, requestor)
    signed_txn = unsigned_txn.sign(rekey_pk)
    txid = algod_client.send_transaction(signed_txn)
    txn_data["rekey_txid"] = txid
    # wait for confirmation 
    try:
        transaction.wait_for_confirmation(algod_client, txid, 4)  
    except Exception as err:
        print(err)
        return

send_primer_to_rekey(txn_data["address"])

rekey_to_requestor(txn_data["address"], txn_data["private_key"], txn_data["requestor"])

#sql = "delete from algoaddress.user_requests_matches where requestor = %s and type = %s"
#val = (txn_data["requestor"],txn_data["type"])

#mycursor.execute(sql,val)

#sql = "delete from algoaddress.search_requests where requestor = %s and type = %s"
#val = (txn_data["requestor"],txn_data["type"])

#mycursor.execute(sql,val)
#mydb.commit()

txn_data["status_text"] = "Found address, " + txn_data["address"] + ", and rekeyed it to you."
filename = "algo_clear_name_search." + txn_data["requestor"] + ".txt"

with open(txn_file_dir + filename, 'w') as f:
    json.dump(txn_data, f)

os.remove(txn_file_dir + TXN_FILE)
