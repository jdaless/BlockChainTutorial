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
    def __init__(self, state):
        genesisBlockTxns = [state]
        genesisBlockContents = {u'blockNumber':0,u'parentHash':None,u'dataCount':1,u'data':genesisBlockTxns}
        genesisHash = hashMe( genesisBlockContents )
        genesisBlock = {u'hash':genesisHash,u'contents':genesisBlockContents}

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
