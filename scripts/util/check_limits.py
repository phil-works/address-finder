#!/usr/bin/env -S python3 -u
import mysql.connector
import os
import yaml

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

lowlimitfile = gd_data["load_filter"]["lowlimitfile"] #"/home/godogdev/address-finder/limit-low.txt"
limits_file = gd_data["load_filter"]["limits_path"] #"/home/godogdev/address-finder/limits.yaml" 
status_dir = gd_data["load_filter"]["status_dir"] #/home/godogdev/address-finder/status/
wait_for_status = gd_data["load_filter"]["wait_for_status"]  #/home/godogdev/address-finder/wait_for_status.sh


with open(limits_file, "r") as stream:
    try:
        limits_cfg = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

for check_len in limits_cfg:
    print("Checking " + str(check_len))
    sql = "SELECT count(*) FROM algoaddress.gdw_available where match_len = " + str(check_len) +"; "
    mycursor.execute(sql)
    act_amt = mycursor.fetchone()
    if act_amt[0] <= limits_cfg[check_len]:
        print(str(check_len) + " - " + str(limits_cfg[check_len]) + " - " +  str(act_amt[0]))
    else:
        over_amt = act_amt[0] - limits_cfg[check_len]
        print(str(check_len) + " - " + str(limits_cfg[check_len]) + " - " +  str(act_amt[0]) + " OVER by " + str(over_amt))
        print("Pausing loader...")
        os.system("echo check_limits > " + status_dir + "load_looper.pause")
        os.system(wait_for_status + " load_looper paused")
        print("Removing overage...")
        sql = "Delete from gdw_available where match_len = " + str(check_len) + " ORDER BY RAND() LIMIT " + str(over_amt) +"; "
        #print(sql)
        mycursor.execute(sql)
        mydb.commit()
        #sql="OPTIMIZE TABLE available;"
        #mycursor.execute(sql)
        #mydb.commit()
        os.system("echo " + str(check_len) + " > " + lowlimitfile)
        print("Removing loader pause. Go free and load! load! LOAD!")
        os.system("rm " + status_dir + "load_looper.pause")
