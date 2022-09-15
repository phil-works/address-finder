# clear.py
#
# This excutes when a user clears the contract from their account... 
#  Pass or fail this will clear... this leaves us with an issue of locked fund that can't be unlocked... ever. 
#  As long as they don't try any funny business it won't be a big issue.  The contract could be updated to allow for manual unlocking of funds.
#  The issue with manual unlocking of funds comes with trust. aka rug pull. 

from pyteal import *

def clear_state_program():
   program = Seq([ Assert( Txn.close_remainder_to() == Global.zero_address()),
   Assert( Txn.asset_close_to() == Global.zero_address()),
   Assert( Txn.rekey_to() == Global.zero_address()),
   If( App.localGet(Int(0), Bytes("SentAmount")) != Int(0) ) # If they have something locked then lets set it free.. to me.
      .Then(App.globalPut(Bytes("LockedForFinder"), App.globalGet(Bytes("LockedForFinder")) - App.localGet(Int(0), Bytes("SentAmount")))),
   Return(Int(1))
   ])
   # Mode.Application specifies that this is a smart contract
   return compileTeal(program, Mode.Application, version=5)

# print out the results
print(clear_state_program())

