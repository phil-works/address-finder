#!/usr/bin/env -S python3 -u
import sys
import json
import mysql.connector
import json
import base64
import yaml
import os
import MySQLdb

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

#app_tx = txn_data["application-transaction"]
#app_args = app_tx["application-args"]
#request_type = str(base64.b64decode(app_args[1]),'ascii')

lsd = txn_data["local-state-delta"]
delta = lsd[0]["delta"]
contest_no = ""
for item in delta:
    if str(base64.b64decode(item["key"]),'ascii') == "ContestNumber":
        nvals = item["value"]
        contest_no = nvals["uint"]
    elif str(base64.b64decode(item["key"]),'ascii') == "ContestGuess":
        nvals = item["value"]
        guess = nvals["uint"]

the_sender = txn_data["sender"]
confirmed_round = txn_data["confirmed-round"]

if contest_no == "":
    print("Was Update..")
    sql = "select max(contest_no) as contest_no from contest_guesses where address = %s"
    val = (the_sender,)
    mycursor.execute(sql,val)
    outp = mycursor.fetchone()
    contest_no = outp[0]


sql = "insert ignore into contest_guesses (contest_no, address, confirmed_round, guess) values (%s, %s, %s, %s)"
vals = (contest_no, the_sender, confirmed_round, guess)

try:
    try:
        mycursor.execute(sql,vals)
        mydb.commit()
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print(e)

finally:
    mydb.close()

os.remove(txn_file_dir + TXN_FILE)
