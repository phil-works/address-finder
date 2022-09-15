# Services
There are 5 services that drive the backend.  

- address_creation_service.sh - This script controlls how many files of addresses are created. If the max amount of files is created the script will wait.  This prevents the file system from filling up. 
- find_vanity.py - creates one file of algorand addresses. 

- loader_service.sh - Checks for new files to load. It will wait if there are none. 
- load_filter.py - loads one file into mysql and then runs the matching process. 

- match_processor_service.sh - runs the match_processor.py
- match_processor.py - this script queries the database to find requests with matches. 

- address-finder-service.py - this service reads the algorand blockchain and creates transaction files based on the applications calls it finds. 

- txn_processor.sh - this script looks for txn_files and then calls the processing script. 

- process_af_contest.py - declares the winner of the contest. 
- process_algo_clear_name_search.py - creates the algorand transaction to execute ClearNameSearch. This would be called when a request match is found or if there is a bad request. 
- process_algo_rekey.py - processes the rekey of the matched address to the requestor. Creates a file for an algo clear name search.
- process_app_opt_in.py - adds addresses to the opt in table. Keep track of who is using the app. 
- process_clear_search.py - removes the requests from the database. This is called when A user requests a clear or for a completed request. 
- process_contest_guess.py - adds the contest guess to the database.
- process_find_this_name.py - adds the request to the database. Can trigger a clear name search if the request is invalid. 
