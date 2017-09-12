import hashlib, json, sys

def hashMe(msg=""):
    # For convenience, this is a helper function that wraps our hashing algorithm
    if type(msg)!=str:
        msg = json.dumps(msg,sort_keys=True)  # If we don't sort keys, we can't guarantee repeatability!

    if sys.version_info.major == 2:
        return unicode(hashlib.sha256(msg).hexdigest(),'utf-8')
    else:
        return hashlib.sha256(str(msg).encode('utf-8')).hexdigest()

class BlockChain:

    def __init__(self, state):
        genesisBlockTxns = [state]
        genesisBlockContents = {u'blockNumber':0,u'parentHash':None,u'dataCount':1,u'data':genesisBlockTxns}
        genesisHash = hashMe( genesisBlockContents )
        genesisBlock = {u'hash':genesisHash,u'contents':genesisBlockContents}

        self.chain = [genesisBlock];

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
