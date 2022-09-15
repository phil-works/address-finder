#!/usr/bin/env python3
import mysql.connector
import json
import requests
import yaml
import os
import sys


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
mycurdict = mydb.cursor(dictionary=True)

# Set the gloabal services config file.
services_config_file = gdwcfg["services_config_file"]

with open(services_config_file, "r") as fp:
    try:
        gd_data = yaml.safe_load(fp)
    except yaml.YAMLError as exc:
        print(exc)
sql = """SELECT * FROM algoaddress.user_requests_matches where 
user_requests_matches_id in (select min(user_requests_matches_id) 
as user_requests_mataches_id from algoaddress.user_requests_matches where inprogress is null group by requestor)"""

try:
    mycurdict.execute(sql)
    results = mycurdict.fetchall()
    print("Found " + str(mycurdict.rowcount) + " records to process")
    #mydb.commit()
except (MySQLdb.Error, MySQLdb.Warning) as e:
    print(e)


for row in results:
    sql = "update user_requests_matches set inprogress = 'Y' where search_request_id = " + str(row["search_request_id"])
    try:
        mycursor.execute(sql)
        mydb.commit()
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print(e)

    if row["type"] == "Rekey":
        file_prefix = "af_rekey."
    else:
        file_prefix = row["type"] + "."

    filename = file_prefix + row["requestor"] + "." + str(row["user_requests_matches_id"]) + ".txt"

    with open(gd_data["txn_processor"]["txn_file_dir"] + filename, 'w') as f:
        json.dump(row, f)

