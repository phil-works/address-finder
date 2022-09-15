# Address Finder & Contest!

This project allows users to interact with an Algorand smart contract to enable a search for a vanity address. A vanity address contains a word or phrase. It's mostly a novelty feature.  When the service finds the address it will Rekey the address to the requestore giving them control. The requestor can approve transactions for that vanity address.  There is a fee to cover the transaction costs but nothing more is required.  

In the contest users submit a guess for which round one of the winning words will be found by the system.  When a winning word is found, the address is rekeyed to the owner account and the winner is paid out based on the smart contract logic.  The payout is scaled for longer words earn more payout.  The remainder of the pot is used for the next contest.

## How-to-use

There are two ways to interact with the smart contract.  First, there are shell scripts that can be altered slightly.  Second, there is a Web3 page to provide interactions. 
You will provide the text to be searched for.  Once an algorand address is found matching the text requested then the vanity address will be rekeyed to the requesters address. The smart contract will update the requestors status to indicate the new address. 

#### Search Types

- Rekey - simply rekeys the found address to the requestor. 

#### Text Positions

- Front -  **WINNER**VTQA3TAZSCKPK5FYGIFZJAI6LOYDTPKMYMVTS6TWQHHWWQ5MT4LI
