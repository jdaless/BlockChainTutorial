import hashlib, json, sys

# Wrapper for the python hasing algorithm
def hashMe(msg=""):
    if type(msg)!=str:
        msg = json.dumps(msg,sort_keys=True)

    if sys.version_info.major == 2:
        return unicode(hashlib.sha256(msg).hexdigest(),'utf-8')

    else:
        return hashlib.sha256(str(msg).encode('utf-8')).hexdigest()

# BlockChain data type.
class BlockChain:

    # Initialize the blockchain by creating a genesis block.
    # State describes the state of data in the genesis block.
    def __init__(self, state, validate_logic, update_logic):
        genesisBlockTxns = [state]
        genesisBlockContents = {u'blockNumber':0,u'parentHash':None,u'dataCount':1,u'data':genesisBlockTxns}
        genesisHash = hashMe( genesisBlockContents )
        genesisBlock = {u'hash':genesisHash,u'contents':genesisBlockContents}

        self.isValidData = validate_logic
        self.updateState = update_logic
        self.chain = [genesisBlock];

    # Not necessary for this demo, but made things look pretty in testing.
    # Good if you want to understand the structure of a block
    def __str__(self):
        ret = ""
        for block in self.chain:
            ret = ret + "block: "+str(block['contents']['blockNumber'])
            ret = ret + "\n\tcontents:"
            if(block['contents']['parentHash'] == None):
                parent = "None, this is the genesis block"
            else:
                parent = block['contents']['parentHash']
            ret = ret + "\n\t\tparent: "+ parent
            ret = ret + "\n\t\tdata count: "+str(block['contents']['dataCount'])
            ret = ret + "\n\t\tdata:"
            for data in block['contents']['data']:
                ret = ret + "\n\t\t\t" + str(data)
            ret = ret + "\n\thash: " + block['hash'] + "\n\n"
        return ret

    def checkBlockHash(self, block):
        # Raise an exception if the hash does not match the block contents
        expectedHash = hashMe( block['contents'] )
        if block['hash']!=expectedHash:
            raise Exception('Hash does not match contents of block %s'%
                            block['contents']['blockNumber'])
        return

    # Create a new block and add it to the chain using the data
    #   you want to put in it.
    # Returns the block in case you need to validate it.
    def makeBlock(self, data):
        parentBlock = self.chain[-1]
        parentHash  = parentBlock[u'hash']
        blockNumber = parentBlock[u'contents'][u'blockNumber'] + 1
        blockContents = {u'blockNumber':blockNumber,u'parentHash':parentHash,
                        u'dataCount':len(data),'data':data}
        blockHash = hashMe( blockContents )
        block = {u'hash':blockHash,u'contents':blockContents}

        self.chain.append(block)
        return block

    def checkBlockValidity(self,block,parent,state):
        # We want to check the following conditions:
        # - Each of the data are valid updates to the system state
        # - Block hash is valid for the block contents
        # - Block number increments the parent block number by 1
        # - Accurately references the parent block's hash
        parentNumber = parent['contents']['blockNumber']
        parentHash   = parent['hash']
        blockNumber  = block['contents']['blockNumber']

        # Check transaction validity; throw an error if an invalid transaction was found.
        for data in block['contents']['data']:
            if self.isValidData(data,state):
                state = self.updateState(data,state)
            else:
                raise Exception('Invalid data in block %s: %s'%(blockNumber,txn))

        self.checkBlockHash(block) # Check hash integrity; raises error if inaccurate

        if blockNumber!=(parentNumber+1):
            raise Exception('Hash does not match contents of block %s'%blockNumber)

        if block['contents']['parentHash'] != parentHash:
            raise Exception('Parent hash not accurate at block %s'%blockNumber)

        return state

    def checkChain(self):

        state = {}
        ## Prime the pump by checking the genesis block
        # We want to check the following conditions:
        # - Each of the transactions are valid updates to the system state
        # - Block hash is valid for the block contents

        for data in self.chain[0]['contents']['data']:
            state = self.updateState(data,state)
        self.checkBlockHash(self.chain[0])
        parent = self.chain[0]

        ## Checking subsequent blocks: These additionally need to check
        #    - the reference to the parent block's hash
        #    - the validity of the block number
        for block in self.chain[1:]:
            state = self.checkBlockValidity(block,parent,state)
            parent = block

        return state
