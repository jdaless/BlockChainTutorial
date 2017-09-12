from blockChain import *
from transactions import *
from validation import *

blockSizeLimit = 3
txnBuffer = []

while(True):
    command = input("> ").split()
    if(command[0] == "transaction"):
        if(command[1] == "rand"):
            txn = randomTransaction();
        else:
            fr = command[1]
            to = command[2]
            amt = int(command[3])
            txn = {fr: 0-amt,to: amt}
        txnBuffer.append(txn)

        # if we have enough transactions for a block
        if(len(txnBuffer)>blockSizeLimit-1):
            print("Making a block...")
            ## Gather a set of valid transactions for inclusion
            txnList = []
            while (len(txnBuffer) > 0) & (len(txnList) < blockSizeLimit):
                newTxn = txnBuffer.pop()
                validTxn = isValidData(newTxn,state) # This will return False if txn is invalid

                if validTxn:           # If we got a valid state, not 'False'
                    txnList.append(newTxn)
                    state = updateState(newTxn,state)
                else:
                    print("ignored transaction")
                    sys.stdout.flush()
                    continue  # This was an invalid transaction; ignore it and move on

            ## Make a block
            chain.makeBlock(txnList)
        else:
            print(txnBuffer)

    elif(command[0] == "init"):
        if(len(command)==1):
            state={"Charlie":50, "Ada":50}
        else:
            state = {command[1]:int(command[2])}
            chain = BlockChain(state)

    elif(command[0] == "save"):
        f = open('BlockChain.json', 'w')
        f.write(json.dumps(chain.chain,sort_keys=True))
        f.close()

    elif(command[0] == "import"):
        f = open('BlockChain.json', 'r')
        importChain = json.loads(f.read())
        f.close()
        importState = checkChain(importChain)
        if(importState):
            chain = BlockChain(None)
            chain.chain = importChain
        state = checkChain(chain.chain)

    elif(command[0] == "state"):
        print(checkChain(chain.chain))

    else:
        print("Not a valid command")
