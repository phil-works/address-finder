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

## Address Finder Contest!

The contest is a split-the-pot game where players guess the closet round when one of the winning words will be found by the Address Finder Service. 

#### Rules and such:
1. The cost is 1 Algo (1000000 micro algo)
2. Make a guess greater than the current algorand round. 
3. You can update your guess after 130,000 rounds, just slightly less than 1 week. 
4. If you happened to get blocked in by two other players then you can get update your guess imedieately by using the BreakOut feature. 
    Example,   User1 guess round 1010, user2 guesses 1009 and user3 guesses 1011 then user1 can BreakOut.  Before `(1009-user2, 1010-user1, 1011-user3)` -> after BreakOut `(1009-user2, 1010-open, 1011-user3, 1309-user1)`
5. The winner is the player with the closest guess to the winning round.  Over or under doesn't matter.. if players have the same amount of rounds then the player who submitted their guess first wins. 
6. When a winner is declared the game resets with the left over funds becoming the new pot. Players must pay the entry fee again. 

The smart contract verifies that an address that starts with a Winning Word has been rekeyed to the Owner address. This prevents funny business. 

Winning Words:
 - PHLWRK
 - PHLWORK
 - PHILWRK
 - PHLWRKS
 - PHLWORKS
 - PHILWRKS
 - PHILWORK
 - PHILWORKS
  
 The payout is based on the length of the Winning Word. The smart contract controlls this payout. 
 | Length | Payout % |
 | ------ | ------- |
 | 6 | 60% |
 | 7 | 80% | 
 | 8 | 90% | 
 | 9 | 100% |
 
 
 #### Considerations: 
 - The speed in which the address finder service discovers a winning word is based on the hardware processing capabilies.  My dev box searched 40 mil records an hour while the production box can search 170 million and hour.
 - The contest is subject to outages. If the address finder service isn't running then winning words can't be found. 
 - I make no money from this contest. It costs money to run the hardwards and network.
 - I do it because it's fun. 
