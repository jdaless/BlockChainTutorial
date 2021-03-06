from blockChain import *
from transactions import *

# Initialize the transaction buffer and set the block size
blockSizeLimit = 3
txnBuffer = []

while(True):
    command = input("> ").split()
    if(command[0] == "transaction"):
        if(len(command) == 1):
            txn = randomTransaction();
        else:
            fr = command[1]
            to = command[2]
            amt = int(command[3])
            txn = {fr: 0-amt,to: amt}
        txnBuffer.append(txn)

        # If we have enough transactions for a block, make one
        if(len(txnBuffer)>blockSizeLimit-1):
            print("Making a block...")
            txnList = []

            while (len(txnBuffer) > 0) & (len(txnList) < blockSizeLimit):
                newTxn = txnBuffer.pop()
                validTxn = isValidData(newTxn,state)

                if validTxn:
                    txnList.append(newTxn)
                    state = updateState(newTxn,state)
                else:
                    print("ignored transaction")
                    sys.stdout.flush()
                    continue  # This was an invalid transaction; ignore it and move on

            # Make a block
            chain.makeBlock(txnList)
        else:
            print(txnBuffer)

    elif(command[0] == "init"):
        if(len(command)==1):
            state={"Charlie":50, "Ada":50}
        else:
            state = {command[1]:int(command[2])}
        chain = BlockChain(state,isValidData,updateState)

    elif(command[0] == "save"):
        f = open('BlockChain.json', 'w')
        f.write(json.dumps(chain.chain,sort_keys=True))
        f.close()

    elif(command[0] == "import"):
        f = open('BlockChain.json', 'r')
        importChain = json.loads(f.read())
        importBC = BlockChain(None,isValidData,updateState)
        importBC.chain = importChain
        f.close()
        importState = importBC.checkChain()
        if(importState):
            chain = importBC
        state = chain.checkChain()

    elif(command[0] == "state"):
        print(chain.checkChain())

    else:
        print("Not a valid command")
