# contest_contract_clear.py

from pyteal import *

def clear_state_program():
   program = Return(Int(1))
   # Mode.Application specifies that this is a smart contract
   return compileTeal(program, Mode.Application, version=5)

# print out the results
print(clear_state_program())

