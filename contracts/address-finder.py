# vanity_address.py
# This contract manages the user interactions.
#
#

from pyteal import *
def approval_program():
   handle_creation = Seq([
       App.globalPut(Bytes("SearchTypeOptions"), Bytes("init") ),
       App.globalPut(Bytes("NamePositionOptions"), Bytes("init") ),
       App.globalPut(Bytes("MinFee"), Int(3000) ),
       Return(Int(1))
   ])

   handle_closeout =  Return(Int(1))
   handle_updateapp = Return(Int(0))
   handle_deleteapp = Return(Int(1))

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

   close_to_check = Txn.close_remainder_to() == Global.zero_address()
   asset_close_to_check = Txn.asset_close_to() == Global.zero_address()
   rekey_check = Txn.rekey_to() == Global.zero_address()
   isCreator = Txn.sender() == Global.creator_address()

   ownerStatusUpdate = Txn.application_args[1]

   globalUpdateSearchType = Txn.application_args[1]
   globalUpdateNamePosition = Txn.application_args[2]
   globalUpdateMinFee = Btoi(Txn.application_args[3])

   userSearchType= Txn.application_args[1]
   userDesiredName = Txn.application_args[2]
   userNamePosition = Txn.application_args[3]

   handle_optin = Seq([  
      App.localPut(Int(0), Bytes("SearchType"), Bytes("Select Search Type...")),  
      App.localPut(Int(0), Bytes("SearchStatus"), Bytes("Waiting for User...")),
      App.localPut(Int(0), Bytes("DesiredName"), Bytes("")),
      App.localPut(Int(0), Bytes("NamePosition"), Bytes("")),
      Return(Int(1))
   ])

   clear_name_search = Seq([
      Assert( And(close_to_check, asset_close_to_check, rekey_check )), # check for bad things
      If(isCreator, Seq([ 
         App.localPut(Int(1), Bytes("SearchType"), Bytes("Select Search Type...")), # Reset
         App.localPut(Int(1), Bytes("SearchStatus"), ownerStatusUpdate), 
         App.localPut(Int(1), Bytes("DesiredName"), Bytes("")), # Reset
         App.localPut(Int(1), Bytes("NamePosition"), Bytes("")) # Reset 
         ]),
      Seq([
         App.localPut(Int(0), Bytes("SearchType"), Bytes("Select Search Type...")), # Reset
         App.localPut(Int(0), Bytes("SearchStatus"), Bytes("Cleared by User...")),  # if the creator is calling then use the custom message else reset.
         App.localPut(Int(0), Bytes("DesiredName"), Bytes("")), # Reset
         App.localPut(Int(0), Bytes("NamePosition"), Bytes("")) # Reset 
      ])), 
      Return(Int(1))      
   ])

   setup_name_search = Seq([ 
      Assert( And(close_to_check, asset_close_to_check, rekey_check )), # check for bad things
      Assert( Global.group_size() == Int(2) ),  # Check for 2 transactions
      Assert( Gtxn[0].type_enum() == TxnType.Payment ), # Check that the first was a payment
      Assert( Gtxn[0].receiver() ==  Global.creator_address() ), # to the creator
      Assert( Gtxn[0].amount() >= App.globalGet(Bytes("MinFee")) ), # For the minimum ammount.. this fee covers the rekey costs. 
      App.localPut(Int(0), Bytes("SearchType"), userSearchType),      
      App.localPut(Int(0), Bytes("DesiredName"), userDesiredName),
      App.localPut(Int(0), Bytes("NamePosition"),  userNamePosition),
      App.localPut(Int(0), Bytes("SearchStatus"), Bytes("Searching...")),
      Return(Int(1))
   ])

   update_globals = Seq([
      Assert( isCreator ),
      App.globalPut(Bytes("SearchTypeOptions"), globalUpdateSearchType ), 
      App.globalPut(Bytes("NamePositionOptions"), globalUpdateNamePosition ), 
      App.globalPut(Bytes("MinFee"), globalUpdateMinFee ),
      Return(Int(1))
   ])

   # This calculates the spendable balance
   contractSpendableBalance = Balance( Global.current_application_address() ) - MinBalance( Global.current_application_address() )

   claimExcessFuns = Seq([
           Assert( isCreator),
           payment( Global.current_application_address(), Global.creator_address() , contractSpendableBalance - Int(1000)),  # Save enough for tx fee
           Return(Int(1))
   ])

   handle_noop = Cond(
       [Txn.application_args[0] == Bytes("FindMeThisName"), setup_name_search],
       [Txn.application_args[0] == Bytes("ClearNameSearch"), clear_name_search],
       [Txn.application_args[0] == Bytes("UpdateGlobals"), update_globals],
       [Txn.application_args[0] == Bytes("ClaimExcessFunds"), claimExcessFuns],
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
