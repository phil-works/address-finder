# Algorand Smart Contracts

This contract controls the interactions with blockchain users.

### Scripts
- genAddressFinder.sh - compiles and deploys the smart contracts to the network. 
- address-finder.py - the main smart contract. 
- clear.py - a generic clear contract. 
- address-finder_contract.teal - The output of the pyteal generation. 
- clear_contract.teal - The output of the pyteal generation. 

### Functions

Example scripts found in the scripts directory. 

- FindMeThisName - Sets up the search. 
- ClearNameSearch - Clears the search. Used by requestor and owner.  
- UpdateGlobals - Used to setup the global variables which contain options for the service. 
- ClaimExcessFunds - in the off chance that someone sends a tip to the contract address rather than the owner address then this function will provide a way to collect those funds. 
