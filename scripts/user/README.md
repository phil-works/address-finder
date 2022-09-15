# User Scripts

Example of the local state after request made:
```
ContestGuess:23601651
ContestNumber:23461043
DesiredName:NEW4U
GuessReset:23601665
NamePosition:Front
SearchStatus:Searching...
SearchType:Rekey
SentAmount:103000
```
Here is the Global state after a request is made. Notice the LockedForFinder amount. 
```
ContestFee:1000000
ContestNumber:23461043
ContestOpen:Y
ContestPrizePool:11000000
GuessResetTimeout:130000
LastWinningMatch:None
LockedForFinder:103000
MinFee:103000
NamePositionOptions:,Front,
SearchTypeOptions:,Rekey,
WinWordList:,PHLWRK,PHLWORK,PHILWRK,PHLWRKS,PHLWORKS,PHILWRKS,PHILWORK,PHILWORKS,
```

The local state after the backend service has rekey the address it found for you
```
ContestGuess:23601651
ContestNumber:23461043
DesiredName:
GuessReset:23601665
NamePosition:
SearchStatus:Found address, NEW4UFTF3TKLS7YC4YGMGKA5CXTVHIMGM6UJMSEWEBKELTVLIHJO6ACG2I, and rekeyed it to you.
SearchType:Select Search Type...
SentAmount:0
```

And the Global state now has the funds unlocked.
```
ContestFee:1000000
ContestNumber:23461043
ContestOpen:Y
ContestPrizePool:11000000
GuessResetTimeout:130000
LastWinningMatch:None
LockedForFinder:0
MinFee:103000
NamePositionOptions:,Front,
SearchTypeOptions:,Rekey,
WinWordList:,PHLWRK,PHLWORK,PHILWRK,PHLWRKS,PHLWORKS,PHILWRKS,PHILWORK,PHILWORKS,
```
