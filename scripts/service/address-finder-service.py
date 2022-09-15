#!/usr/bin/env -S python3 -u
import time
import base64
import json
import requests
import yaml
import os
from algosdk.v2client import  indexer
from algosdk.error import IndexerHTTPError

#
# Setup DB
#
with open(os.environ['HOME'] + "/config/godogwin-net.yaml", "r") as stream:
    try:
        gdwcfg = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

INDEXER_ADDRESS = gdwcfg["indexer_address"]
ALGOD_ADDRESS = gdwcfg["algod_address"]
ALGOD_TOKEN = gdwcfg["algod_token"]
HEALTHCHECK = gdwcfg["healthcheck_url"]

# Set the gloabal services config file. 
services_config_file = gdwcfg["services_config_file"]

with open(services_config_file, 'r') as fp:
    gd_data = yaml.safe_load(fp)

# Setup the variables for the service
MAX_CONNECTION_ATTEMPTS = gd_data["address-finder"]["MAX_CONNECTION_ATTEMPTS"] # 10
CONNECTION_ATTEMPT_DELAY_SEC = gd_data["address-finder"]["CONNECTION_ATTEMPT_DELAY_SEC"] # 2

last_round_searched_file = gd_data["address-finder"]["last_round_searched_file"] # $HOME/scripts/services/config/contest-round-searched.txt
txn_save_dir = gd_data["address-finder"]["txn_save_dir"]

with open(last_round_searched_file, "r") as stream:
    try:
        last_proc_rnd = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

#gd_data['gdwitems']['contracts']

def search_algo_calls(indexer_client: indexer.IndexerClient, minny_rnd):
    nexttoken = ""
    numtx = 1
    calls = []
    while numtx > 0:
        result = indexer_client.search_transactions(
            limit=1000,
            next_page=nexttoken,
            application_id=gd_data['address-finder']['app_id'],
            min_round=minny_rnd
        )
        calls += result['transactions']
        numtx = len(result['transactions'])
        #print("Number of Txs: " + str(numtx))
        if numtx > 0:
            # pointer to the next chunk of requests
            nexttoken = result['next-token']
    return calls

def process_tx(algo_txs):
    for tx in algo_txs:
        #pprint.pprint(tx)
        #value = input("Press enter to continue...")
        sender = tx["sender"]
        #app_tx = tx["application-transaction"]
        round_time = tx["round-time"]
        tx_type = tx["tx-type"]
        confirmed_round = tx["confirmed-round"]
        txn_id = tx["id"]

        # Payments
        if tx_type == "pay":
            payment_transaction = tx["payment-transaction"]
            payment_amount = payment_transaction["amount"]
            reciever = payment_transaction["receiver"]
            print("Processing Payment for Sender: " + sender[0:8] + " sending " + str(payment_amount) + " to " + reciever[0:8] + ". Confirmed in round " + str(confirmed_round) + " at " + time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(round_time)) + ".")
            txn_file_name = txn_save_dir + "pay." + txn_id + ".txn" 
            with open(txn_file_name, "w") as f:
                f.write(json.dumps(tx))
                f.close()

        # Application Calls
        if tx_type == "appl" and "application-transaction" in tx:
            #pprint.pprint(tx)
            #value = input("Press enter to continue...")
            app_tx = tx["application-transaction"]
            app_args = app_tx["application-args"]
            app_id = app_tx["application-id"]
            if len(app_args) != 0:
                # Application Calls
                print("Processing Application call for Sender: " + sender[0:8] + " for App ID " + str(app_id) + " with app arg "  + str(base64.b64decode(app_args[0]),'ascii') + ". Confirmed in round " + str(confirmed_round) + " at " + time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(round_time)) + ".")
                if str(base64.b64decode(app_args[0]),'ascii') == "FindMeThisName":
                    # TO-DO: Add look for name
                    #os.popen(look_for_this_name_script + " " + sender + " " + str(confirmed_round))
                    txn_file_name = txn_save_dir + "findmethisname." + txn_id + ".txn" 
                    with open(txn_file_name, "w") as f:
                        f.write(json.dumps(tx))
                        f.close()
                
                if str(base64.b64decode(app_args[0]),'ascii') == "ClearNameSearch":
                    # TO-DO: Add remove fromd database
                    #os.popen(remove_search_request_script + " " + sender + " " + str(confirmed_round))
                    txn_file_name = txn_save_dir + "clearnamesearch." + txn_id + ".txn" 
                    with open(txn_file_name, "w") as f:
                        f.write(json.dumps(tx))
                        f.close()

                if str(base64.b64decode(app_args[0]),'ascii') == "ContestGuess" or str(base64.b64decode(app_args[0]),'ascii') == "BreakOut":
                    txn_file_name = txn_save_dir + "contest_guess." + txn_id + ".txn"
                    with open(txn_file_name, "w") as f:
                        f.write(json.dumps(tx))
                        f.close()


            elif app_tx["on-completion"] == "optin":
                # Application Opt In
                print("Processing Application Opt-in for Sender: " + sender[0:8] + " for App ID: " + str(app_id))
                # TO-DO: add optin saving/logging
                #os.popen(save_optin_script + " " + str(app_id) + " " + sender)
                txn_file_name = txn_save_dir + "app-optin." + str(app_id) + "." + txn_id + ".txn" 
                with open(txn_file_name, "w") as f:
                    f.write(json.dumps(tx))
                    f.close()

            elif app_tx["on-completion"] == "clear" or app_tx["on-completion"] == "closeout":
                print("Processing App Closeout or Clear for Sender: " + sender[0:8] + " for App ID: " + str(app_id))
                txn_file_name = txn_save_dir + "clearnamesearch." + txn_id + ".txn"
                with open(txn_file_name, "w") as f:
                    f.write(json.dumps(tx))
                    f.close()

            
            # Process any inner Txs
            #if "inner-txns" in tx:
            #    inner_txs = tx["inner-txns"]
            #    process_tx(inner_txs)
    


def main():

    indexer_client = indexer.IndexerClient(
        indexer_token=ALGOD_TOKEN,
        indexer_address=INDEXER_ADDRESS
    )

    response = requests.get(HEALTHCHECK)
    nxt_round = response.json()
    this_round = nxt_round["round"]
    THIS_MIN_ROUND = last_proc_rnd

    while 1 == 1:
        last_round = this_round
        print("Checking round: " + str(last_round) + ", Min: " + str(THIS_MIN_ROUND))
        attempts = 1
        algo_calls = None
        while attempts <= MAX_CONNECTION_ATTEMPTS:
            try:
                #print("Collecting Algo Txs")
                algo_calls = search_algo_calls(indexer_client, THIS_MIN_ROUND)
                break
            except IndexerHTTPError:
                print(f'Indexer Client connection attempt '
                      f'{attempts}/{MAX_CONNECTION_ATTEMPTS}')
                print('Trying to contact Indexer Client again...')
                time.sleep(CONNECTION_ATTEMPT_DELAY_SEC)
            finally:
                attempts += 1
        if not algo_calls:
            time.sleep(CONNECTION_ATTEMPT_DELAY_SEC)
        else:
            process_tx(algo_calls)


        # Save the current round
        try:
            outFile = open(last_round_searched_file, 'w')
            outFile.write(str(last_round))
            outFile.close()
        except IOError as e:
            print ("I/O error({0})").format(e)

        response = requests.get(HEALTHCHECK)
        nxt_round = response.json()
        this_round = nxt_round["round"]
        while last_round == this_round:
            time.sleep(CONNECTION_ATTEMPT_DELAY_SEC)
            response = requests.get(HEALTHCHECK)
            nxt_round = response.json()
            this_round = nxt_round["round"]

        THIS_MIN_ROUND = this_round


if __name__ == "__main__":
    main()

