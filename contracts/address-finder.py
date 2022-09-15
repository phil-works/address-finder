# address-finder.py
# This contract manages the user interactions.
#
#

from pyteal import *
def approval_program():
   handle_creation = Seq([
       App.globalPut(Bytes("SearchTypeOptions"), Bytes("init") ),
       App.globalPut(Bytes("NamePositionOptions"), Bytes("init") ),
       App.globalPut(Bytes("MinFee"), Int(103000) ), # .0103 algo
       App.globalPut(Bytes("LockedForFinder"), Int(0) ),      
       App.globalPut(Bytes("ContestFee"), Int(1000000) ), # 1 algo
       App.globalPut(Bytes("ContestPrizePool"), Int(0) ),
       App.globalPut(Bytes("ContestNumber"), Global.round() ),
       App.globalPut(Bytes("GuessResetTimeout"), Int(130000)), # little less than 1 week at 4.5sec rounds. 
       App.globalPut(Bytes("LastWinningMatch"), Bytes("None")),
       App.globalPut(Bytes("WinWordList"), Bytes("None")),
       App.globalPut(Bytes("ContestOpen"), Bytes("N")),
       Return(Int(1))
   ])

   # Common
   close_to_check = Txn.close_remainder_to() == Global.zero_address()
   asset_close_to_check = Txn.asset_close_to() == Global.zero_address()
   rekey_check = Txn.rekey_to() == Global.zero_address()
   isCreator = Txn.sender() == Global.creator_address()

   handle_closeout =  Seq([
      Assert( And(close_to_check, asset_close_to_check, rekey_check )),  # Check for funny business
      If( App.localGet(Int(0), Bytes("SentAmount")) != Int(0) ) # If they have something locked then lets set it free.. to me. 
      .Then(App.globalPut(Bytes("LockedForFinder"), App.globalGet(Bytes("LockedForFinder")) - App.localGet(Int(0), Bytes("SentAmount")))),  # Update locked amount.
      Return(Int(1))
   ])

   handle_updateapp = Seq([ Assert( isCreator), Return(Int(1)) ])  
   handle_deleteapp = Seq([ Assert( isCreator), Return(Int(1)) ]) 

   @Subroutine(TealType.none)
   def payment( sender, receiver, amount ):
       return Seq([
          InnerTxnBuilder.Begin(),
          InnerTxnBuilder.SetFields(
           {
               TxnField.type_enum: TxnType.Payment,
               TxnField.sender: sender,
               TxnField.receiver: receiver,
               TxnField.amount: amount,
               TxnField.fee: Int(1000)
           }
          ),
          InnerTxnBuilder.Submit(),
          Return()
    ])

   @Subroutine(TealType.uint64)
   def find_string( lookfor, inthis ):
      i = ScratchVar(TealType.uint64)  # Loop Counter
      lfl = ScratchVar(TealType.uint64)  # look for length
      mxl = ScratchVar(TealType.uint64)  # Max length of string to search
      return Seq([
         lfl.store(Len(lookfor)), 
         mxl.store(Len(inthis) - Len(lookfor)), 
         For( i.store(Int(0)),  i.load() <= mxl.load() ,  i.store(i.load() + Int(1)) ).Do(
            If( lookfor == Extract(inthis, i.load(), lfl.load() ) ) 
            .Then ( Return(Int(1)))
         ),
         Return(Int(0))
      ])

   # Search
   ownerStatusUpdate = Txn.application_args[1]

   globalUpdateSearchType = Txn.application_args[1]
   globalUpdateNamePosition = Txn.application_args[2]
   globalUpdateMinFee = Btoi(Txn.application_args[3])   

   globalUpdateContestFee = Btoi(Txn.application_args[1])
   globalUpdateGuessResetTimeout = Btoi(Txn.application_args[2])
   globalUpdateWinWordList = Txn.application_args[3]
   globalUpdateContestOpen = Txn.application_args[4]

   userSearchType= Txn.application_args[1]
   userDesiredName = Txn.application_args[2]
   userNamePosition = Txn.application_args[3]

   # Contest
   userContestGuess = Btoi(Txn.application_args[1])
   nextReset = Global.round() + App.globalGet(Bytes("GuessResetTimeout"))
   contestWinner = Txn.accounts[1]
   winningWord = Txn.application_args[1]
   payout_percent = ScratchVar(TealType.uint64)
   payout_amount = ScratchVar(TealType.uint64)
   strWinAddress = Txn.application_args[2]

   #Breakout
   senderGuess =  App.localGet( Int(0), Bytes("ContestGuess") )
   actBelowGuess = App.localGet( Int(1), Bytes("ContestGuess") )
   actAboveGuess = App.localGet( Int(2), Bytes("ContestGuess") )


   handle_optin = Seq([ 
      Assert( And(close_to_check, asset_close_to_check, rekey_check )), # check for bad things
      App.localPut(Int(0), Bytes("SearchType"), Bytes("Select Search Type...")),  
      App.localPut(Int(0), Bytes("SearchStatus"), Bytes("Waiting for User...")),
      App.localPut(Int(0), Bytes("DesiredName"), Bytes("")),
      App.localPut(Int(0), Bytes("NamePosition"), Bytes("")),
      App.localPut(Int(0), Bytes("SentAmount"), Int(0)),
      App.localPut(Int(0), Bytes("ContestNumber"), Int(0)),
      App.localPut(Int(0), Bytes("ContestGuess"), Int(0)),
      App.localPut(Int(0), Bytes("GuessReset"), Int(0)),      
      Return(Int(1))
   ])

   clear_name_search = Seq([
      Assert( And(close_to_check, asset_close_to_check, rekey_check )), # check for bad things
      If(isCreator, Seq([ 
         App.localPut(Int(1), Bytes("SearchType"), Bytes("Select Search Type...")), # Reset
         App.localPut(Int(1), Bytes("SearchStatus"), ownerStatusUpdate), 
         App.localPut(Int(1), Bytes("DesiredName"), Bytes("")), # Reset
         App.localPut(Int(1), Bytes("NamePosition"), Bytes("")), # Reset 
         App.globalPut(Bytes("LockedForFinder"), App.globalGet(Bytes("LockedForFinder")) - App.localGet(Int(1), Bytes("SentAmount"))),
         App.localPut(Int(1), Bytes("SentAmount"), Int(0)),
         ]),
      Seq([
         App.localPut(Int(0), Bytes("SearchType"), Bytes("Select Search Type...")), # Reset
         App.localPut(Int(0), Bytes("SearchStatus"), Bytes("Cleared by User...")),  # if the creator is calling then use the custom message else reset.
         App.localPut(Int(0), Bytes("DesiredName"), Bytes("")), # Reset
         App.localPut(Int(0), Bytes("NamePosition"), Bytes("")), # Reset 
         App.globalPut(Bytes("LockedForFinder"), App.globalGet(Bytes("LockedForFinder")) - App.localGet(Int(0), Bytes("SentAmount"))),
         App.localPut(Int(0), Bytes("SentAmount"), Int(0)),
      ])), 
      Return(Int(1))      
   ])

   setup_name_search = Seq([ 
      Assert( And(close_to_check, asset_close_to_check, rekey_check )), # check for bad things
      Assert( Global.group_size() >= Int(2) ),  # Check for 2 transactions
      Assert( Gtxn[0].type_enum() == TxnType.Payment ), # Check that the first was a payment
      Assert( Gtxn[0].receiver() ==  Global.current_application_address() ), # to the creator
      Assert( Gtxn[0].amount() >= App.globalGet(Bytes("MinFee")) ), # For the minimum ammount.. this fee covers the rekey costs. 
      Assert( find_string( Concat(Bytes(","), userSearchType, Bytes(",")), App.globalGet(Bytes("SearchTypeOptions")) )), # Check Type
      Assert( find_string( Concat(Bytes(","), userNamePosition, Bytes(",")), App.globalGet(Bytes("NamePositionOptions")) )), # Check Position 
      Assert( App.localGet(Int(0), Bytes("SentAmount")) == Int(0) ), # if there is no money they are ready to give more. 
      App.localPut(Int(0), Bytes("SearchType"), userSearchType),      
      App.localPut(Int(0), Bytes("DesiredName"), userDesiredName),
      App.localPut(Int(0), Bytes("NamePosition"),  userNamePosition),
      App.localPut(Int(0), Bytes("SearchStatus"), Bytes("Searching...")),
      App.localPut(Int(0), Bytes("SentAmount"), Gtxn[0].amount() ),     
      App.globalPut(Bytes("LockedForFinder"), Gtxn[0].amount() + App.globalGet(Bytes("LockedForFinder"))),
      Return(Int(1))
   ])

   # This joins and sets the guess for the contest. 
   contest_guess = Seq([
      Assert( And(close_to_check, asset_close_to_check, rekey_check )),
      Assert( App.globalGet(Bytes("ContestOpen")) == Bytes("Y") ),
      Assert( Global.round() < userContestGuess ), # Make sure its a good guess. 
      If( App.localGet( Int(0), Bytes("ContestNumber") ) != App.globalGet( Bytes("ContestNumber") ))
      .Then( Seq([ 
         # It's a new contest so they have to pay.       
         Assert( Global.group_size() == Int(2) ),  # Check for 2 transactions
         Assert( Gtxn[0].type_enum() == TxnType.Payment ), # Check that the first was a payment
         Assert( Gtxn[0].receiver() ==  Global.current_application_address() ), # to the contract address. 
         Assert( Gtxn[0].amount() >= App.globalGet( Bytes("ContestFee") ) ),
         App.localPut( Int(0), Bytes("ContestNumber"), App.globalGet( Bytes("ContestNumber") ) ),
         App.localPut( Int(0), Bytes("ContestGuess"), userContestGuess ),
         App.localPut( Int(0), Bytes("GuessReset"), nextReset ),
         App.globalPut( Bytes("ContestPrizePool"), App.globalGet( Bytes("ContestFee") ) + App.globalGet(Bytes("ContestPrizePool") ) )         
      ]))
      .Else( Seq([ 
         Assert( Global.round() > App.localGet( Int(0), Bytes("GuessReset") ) ),
         App.localPut( Int(0), Bytes("ContestGuess"), userContestGuess ),
         App.localPut( Int(0), Bytes("GuessReset"), nextReset ),
      ])),
      Return(Int(1))    
   ])

   declare_contest_winner = Seq([ 
      Assert( isCreator ),
      Assert( Global.group_size() >= Int(2) ),  # Check for 2 transactions
      Assert( Gtxn[0].sender() == Gtxn[0].receiver() ), # When we rekey we send a 0 payment to ourselves and use the rekey flag
      Assert( Gtxn[0].amount() == Int(0) ),
      Assert( Gtxn[0].rekey_to() == Global.creator_address() ), # this checks to make sure its a rekey. 
      Assert( find_string( Concat(Bytes(","), winningWord, Bytes(",")), App.globalGet(Bytes("WinWordList")) )), # verify the word is in the list
      Assert( find_string(winningWord,strWinAddress)), # Verify the address contains the word. Should trigger in the first loop. 
      payout_percent.store(Int(0)),
      If( Len( winningWord ) == Int(9))
      .Then( payout_percent.store(Int(100)) )
      .ElseIf( Len( winningWord ) == Int(8) )
      .Then( payout_percent.store(Int(90)) )
      .ElseIf( Len( winningWord ) == Int(7) )
      .Then( payout_percent.store(Int(80)) )
      .ElseIf( Len( winningWord ) == Int(6) )
      .Then( payout_percent.store(Int(60)) ),
      payout_amount.store( App.globalGet(Bytes("ContestPrizePool") ) * payout_percent.load() ),
      payout_amount.store( payout_amount.load() / Int(100) ),
      App.globalPut( Bytes("ContestPrizePool"), App.globalGet(Bytes("ContestPrizePool") ) - payout_amount.load() - Int(1000) ), #Pool pays the txn fee to pay the winner
      payment( Global.current_application_address(), contestWinner, payout_amount.load()),
      App.globalPut( Bytes("ContestNumber"), Global.round() + Int(1) ),
      App.globalPut(Bytes("LastWinningMatch"), Gtxn[0].sender()),  
      Return(Int(1))
   ])

   break_out = Seq([ 
      Assert( And(close_to_check, asset_close_to_check, rekey_check )),
      Assert( App.localGet( Int(0), Bytes("ContestNumber") ) == App.globalGet( Bytes("ContestNumber") ) ), # Make sure we're the same contest
      Assert( senderGuess - Int(1) == actBelowGuess ),  # Check below
      Assert( senderGuess + Int(1) == actAboveGuess ),   # Check above
      Assert( Global.round() < userContestGuess ), # Make sure its a good guess. 
      # If they've passed the tests then they are blocked and we should set them free.
      App.localPut( Int(0), Bytes("ContestGuess"), userContestGuess ),
      App.localPut( Int(0), Bytes("GuessReset"), nextReset ),
      Return(Int(1))
   ])

   # Used too add funds to the prize pool. 
   seed_contest_pool = Seq([
      Assert( isCreator ),
      Assert( Global.group_size() == Int(2) ),
      Assert( Gtxn[0].type_enum() == TxnType.Payment ), # Check that the first was a payment
      Assert( Gtxn[0].receiver() ==  Global.current_application_address() ),
      App.globalPut( Bytes("ContestPrizePool"), Gtxn[0].amount() + App.globalGet(Bytes("ContestPrizePool") ) ),
      Return(Int(1))  
   ])

   update_globals = Seq([
      Assert( isCreator ),
      App.globalPut( Bytes("SearchTypeOptions"), globalUpdateSearchType ), 
      App.globalPut( Bytes("NamePositionOptions"), globalUpdateNamePosition ), 
      App.globalPut( Bytes("MinFee"), globalUpdateMinFee ),
      Return(Int(1))
   ])

   update_contest_globals = Seq([
      Assert( isCreator ),
      App.globalPut( Bytes("ContestFee"),  globalUpdateContestFee), 
      App.globalPut( Bytes("GuessResetTimeout"),  globalUpdateGuessResetTimeout), 
      App.globalPut( Bytes("WinWordList"), globalUpdateWinWordList),
      App.globalPut( Bytes("ContestOpen"), globalUpdateContestOpen),
      Return(Int(1))
   ])

   # This calculates the spendable balance
   contractSpendableBalance = Balance( Global.current_application_address() ) - MinBalance( Global.current_application_address() ) - App.globalGet(Bytes("ContestPrizePool") ) - App.globalGet(Bytes("LockedForFinder"))

   claimExcessFunds = Seq([
           Assert( isCreator),
           payment( Global.current_application_address(), Global.creator_address() , contractSpendableBalance - Int(1000)),  # Save enough for tx fee
           Return(Int(1))
   ])

   xtraxtra = Seq([
      Assert( isCreator),
      Return(Int(1))
   ])

   handle_noop = Cond(
       [Txn.application_args[0] == Bytes("FindMeThisName"), setup_name_search],
       [Txn.application_args[0] == Bytes("ClearNameSearch"), clear_name_search],
       [Txn.application_args[0] == Bytes("ContestGuess"), contest_guess],
       [Txn.application_args[0] == Bytes("BreakOut"), break_out],
       [Txn.application_args[0] == Bytes("DeclareContestWinner"), declare_contest_winner ],
       [Txn.application_args[0] == Bytes("SeedContestPool"), seed_contest_pool],
       [Txn.application_args[0] == Bytes("UpdateGlobals"), update_globals],
       [Txn.application_args[0] == Bytes("UpdateContestGlobals"), update_contest_globals],
       [Txn.application_args[0] == Bytes("ClaimExcessFunds"), claimExcessFunds],
       [Txn.application_args[0] == Bytes("xx"), xtraxtra],
   )

   program = Cond(
       [Txn.application_id() == Int(0), handle_creation],
       [Txn.on_completion() == OnComplete.OptIn, handle_optin],
       [Txn.on_completion() == OnComplete.CloseOut, handle_closeout],
       [Txn.on_completion() == OnComplete.UpdateApplication, handle_updateapp],
       [Txn.on_completion() == OnComplete.DeleteApplication, handle_deleteapp],
       [Txn.on_completion() == OnComplete.NoOp, handle_noop]
   )
   # Mode.Application specifies that this is a smart contract
   return compileTeal(program, Mode.Application, version=5)

# print out the results
print(approval_program())
