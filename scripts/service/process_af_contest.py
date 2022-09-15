#!/usr/bin/env -S python3 -u
import sys
import json
import mysql.connector
import json
import yaml
import os
import MySQLdb
import requests
from algosdk import mnemonic, account, util, constants
from algosdk.future import transaction
from algosdk.v2client import algod, indexer
from algosdk.error import AlgodHTTPError, IndexerHTTPError


TXN_FILE = sys.argv[1]

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

def declare_winner(winner, found_addr, private_key, win_word):
    params = algod_client.suggested_params()
    params.flat_fee = constants.MIN_TXN_FEE
    params.fee = 1000
    unsigned_txn0 = transaction.PaymentTxn(found_addr, params, found_addr, 0, None, None, None, OWNER)
    app_args = ("DeclareContestWinner", win_word, found_addr)
    accounts = (winner, found_addr)
    unsigned_txn1 = transaction.ApplicationNoOpTxn(OWNER, params, CONTRACT_ID, app_args, accounts)
    app_args = ("xx",)
    unsigned_txn2 = transaction.ApplicationNoOpTxn(OWNER, params, CONTRACT_ID, app_args)
    gid = transaction.calculate_group_id([unsigned_txn0, unsigned_txn1, unsigned_txn2])
    unsigned_txn0.group = gid
    unsigned_txn1.group = gid
    unsigned_txn2.group = gid
    # sign transactions
    stxn1 = unsigned_txn0.sign(private_key)
    stxn2 = unsigned_txn1.sign(OWNERPK)
    stxn3 = unsigned_txn2.sign(OWNERPK)
    # send them over network (note that the accounts need to be funded for this to work)
    txid = algod_client.send_transactions([stxn1, stxn2, stxn3])
    # wait for confirmation
    try:
        transaction.wait_for_confirmation(algod_client, txid, 4)
    except Exception as err:
        print(err)
        return

def send_primer_to_rekey(rekey_address):
     # build transaction
    params = algod_client.suggested_params()
    # comment out the next two (2) lines to use suggested fees
    params.flat_fee = constants.MIN_TXN_FEE
    params.fee = 1000
    amount = gd_data["address-finder"]["min-fee"]
    unsigned_txn = transaction.PaymentTxn(OWNER, params, rekey_address, amount, None, None)
    signed_txn = unsigned_txn.sign(OWNERPK)
    txid = algod_client.send_transaction(signed_txn)
    # wait for confirmation
    try:
        transaction.wait_for_confirmation(algod_client, txid, 4)
    except Exception as err:
        print(err)
        return


try:
    response = requests.get(HEALTHCHECK)
    nxt_round = response.json()
    this_round = nxt_round["round"]

    sql = """SELECT cg.address, cg.guess, cg.contest_no,
          case
	       when cg.guess > winning_round then cg.guess - winning_round
               when cg.guess < winning_round then winning_round - cg.guess
          end as rankin
          FROM algoaddress.contest_guesses cg, 
          (select address, max(confirmed_round) as confirmed_round from contest_guesses group by address) mr,
          (select %s as winning_round) wr
           where cg.contest_no in (select max(contest_no) as contest_no from contest_guesses)
           and cg.address = mr.address and cg.confirmed_round = mr.confirmed_round 
           order by rankin limit 1 ;"""
    vals = (this_round,)
    try:
        mycursor.execute(sql,vals)
        winner = mycursor.fetchone()
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print(e)

    send_primer_to_rekey(txn_data["address"])
    declare_winner(winner[0],txn_data["address"], txn_data["private_key"], txn_data["match_part"]) 
    sql = """insert into contest_winners (address, private_key, name, name_len, user_requests_matches_id, contest_no, winning_round, winner)
    values (%s, %s, %s, %s, %s, %s, %s, %s)"""
    vals = (txn_data["address"], txn_data["private_key"],txn_data["name"], txn_data["name_len"], txn_data["user_requests_matches_id"],winner[2] , this_round, winner[0])
    try:
        mycursor.execute(sql,vals)
        sql = "delete from user_requests_matches where user_requests_matches_id = %s"
        vals = (txn_data["user_requests_matches_id"],)
        mycursor.execute(sql,vals)
        mydb.commit()
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print(e)


    os.remove(txn_file_dir + TXN_FILE)

finally:
    mydb.close()
