# Algorand Smart Contracts

This contract controls the interactions with blockchain users.

### Scripts
- genAddressFinder.sh - compiles and deploys the smart contracts to the network. 
- address-finder.py - the main smart contract. 
- clear.py - a clear program to unlock funds when the user clears. 
- address-finder_contract.teal - The output of the pyteal generation. 
- clear_contract.teal - The output of the pyteal generation. 

### Functions

Example scripts found in the scripts directory. 

#### User
- FindMeThisName - Sets up the search. 
- ClearNameSearch - Clears the search.
- ContestGuess - sets the contestants guess. 
- BreakOut - used to change your guess when there are other guesses surrounding yours. 

#### Owner
- UpdateGlobals - Used to setup the global variables which contain options for the service. 
- UpdateContestGlobals - Used to setup the contest variables. 
- ClearNameSearch - Used to reset a search if someone inputs an invalid request. 
- ClaimExcessFunds - in the off chance that someone sends a tip to the contract address rather than the owner address then this function will provide a way to collect those funds. 
- DeclareContestWinner - this will validate that an account has been rekeys to the owner address and that it contains one of the winning words.  Also determins the payout percentage. 
- SeedContestPool - Allows the owner to send money to the contest prize pool. 