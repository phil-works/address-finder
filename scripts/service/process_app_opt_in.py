#!/usr/bin/env -S python3 -u
import sys
import json
import mysql.connector
import json
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

#print(txn_data["sender"] + " " + str(txn_data["confirmed-round"]))

sql = "INSERT into algoaddress.app_optins (address, app_id, round) values (%s, %s, %s)"
vals = (txn_data["sender"], txn_data["application-transaction"]["application-id"], txn_data["confirmed-round"])

try:
    try:
        mycursor.execute(sql,vals)
        mydb.commit()
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print(e)

finally:
    mydb.close()

os.remove(txn_file_dir + TXN_FILE)
