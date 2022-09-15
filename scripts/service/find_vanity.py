#!/usr/bin/env -S python3 -u

from algosdk import account

# Variables containing Private Key and Address
PRIVATE_KEY = ""
ADDRESS = ""
counter=0
max_count=50000

# Keep looping until desired address is found.
while (counter < max_count):
    PRIVATE_KEY, ADDRESS = account.generate_account()
    print(ADDRESS + '|' + PRIVATE_KEY )
    counter += 1

