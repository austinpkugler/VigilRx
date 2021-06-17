import json

from web3 import Web3
from solc import compile_standard


compiled_sol = compile_standard({
    "language": "Solidity",
    "sources": {
        "Greeter.sol": {
            "content": '''
                 pragma solidity ^0.8.4;

                 contract Greeter {
                   string public greeting;

                   constructor() public {
                       greeting = 'Hello';
                   }

                   function setGreeting(string memory _greeting) public {
                       greeting = _greeting;
                   }

                   function greet() view public returns (string memory) {
                       return greeting;
                   }
                 }
               '''
        }
    },
    "settings":
    {
        "outputSelection": {
            "*": {
                "*": [
                    "metadata", "evm.bytecode", "evm.bytecode.sourceMap"
                ]
            }
        }
    }
})

# w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))


# import json

# # import solc
# from solc import compile_source
# from web3 import Web3


# with open('contracts/Prescription.sol') as file:
#     sol = file.read()

# compiled_sol = compile_source(sol)


# # compiled_sol = compile_standard(contracts)

# # w3 = Web3(Web3.EthereumTesterProvider())
# # w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
# # w3.eth.default_account = w3.eth.accounts[0]
# # bytecode = compiled_sol['contracts']['Greeter.sol']['Greeter']['evm']['bytecode']['object']
