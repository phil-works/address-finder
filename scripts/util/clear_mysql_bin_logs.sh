#
# clear_mysql_bin_logs.sh
#
#

source ~/config/envar

cd ~/address-finder/
echo "Log purge and organize" > ./status/load_looper.pause
./scripts/util//wait_for_status.sh load_looper paused
mysql -h $GDWHOST -u $GDWUSR -p${GDWPWD} -D $ADDRDB -e "PURGE BINARY LOGS BEFORE DATE(NOW() - INTERVAL 1 hour); OPTIMIZE TABLE available;"
rm ./status/load_looper.pause

