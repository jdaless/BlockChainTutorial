# BlockChainTutorial
A quick implementation the blockchain based off of the work here: https://github.com/emunsing/tutorials/blob/master/BuildYourOwnBlockchain.ipynb

## How to read
blockChain.py contains the blockchain datatype as well as a wrapper for the hashing function.

transactions.py contains business logic for a token system that is built on this blockchain

node.py is a node that can add transactions to the blockchain.

## How to use
Run node.py. You have five commands:

\> state

Tells you the current state of the transaction system.

\> export

Save the current blockchain in BlockChain.json.

\> import

Import BlockChain.json into the current node.

\> init [arg1] [arg2]

If args are empty, simply create a new blockchain initialized with Ada and Charlie each having 50 tokens.
Otherwise, arg1 is an account name and arg2 is a starting amount of tokens in the system.

\> transaction [arg1] [arg2] [arg3]

If args are empty, generate a random transaction between Ada and Charlie for up to 3 tokens.
Otherwise, transfer arg3 tokens from arg1 to arg2.
