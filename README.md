# Address Finder

This project allows users to interact with an Algorand smart contract to enable a search for a vanity address.  There is a fee to cover the transaction costs but nothing more is required.

## How-to-use

There are two ways to interact with the smart contract.  First, there are shell scripts that can be altered slightly.  Second, there is a Web3 page to provide interactions. 
You will provide the text to be searched for.  Once an algorand address is found matching the text requested then the vanity address will be rekeyed to the requesters address. The smart contract will update the requestors status to indicate the new address. 

#### Search Types

- Rekey - simply rekeys the found address to the requestor. 
- Save for Game (coming soon) - Will store the key to be used by the requestor in a blockchain game.
- Secure Private Key Delivery - Still in planning stages.  The idea being that the private key would be transferred back to the requestor in a secure fashion.  Likely the key would be encrypted and transferred. 

#### Text Positions

Examples of text positions..  Let's say we're searching for WINNER. Example addresses that are not real.

- Front -  **WINNER**VTQA3TAZSCKPK5FYGIFZJAI6LOYDTPKMYMVTS6TWQHHWWQ5MT4LI
- Any - VTQA3TAZSCKPK5FYGIFZJAI6L**WINNER**OYDTPKMYMVTS6TWQHHWWQ5MT4LI
- Back - VTQA3TAZSCKPK5FYGIFZJAI6LOYDTPKMYMVTS6TWQHHWWQ5MT4LI**WINNER**

#### Matching Logic

In development. 

- Normal match - finds exactly what you're looking for
- Mostly match - Finds pretty much what you're looking for.  Example: WINNR or WNNER
- 1337 Match - W1NN3R

