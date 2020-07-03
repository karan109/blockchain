# Blockchain

There are 3 operations which take place in any blockchain:

1. The users post their transactions.
2. The miners validate selected transactions from the transaction pool and produce a nonce as proof of work.
3. They submit the nonce which is checked by the nodes and if proven correct it is added to the blockchain.

Here we have:
1. The user submits some content.
2. For mining any content in the pool is selected by the miner. (Miner performs using their own hardware, however we have used the server’s computational power to perform this here.) 
3. On nonce submission it is checked if the hash is below a certain target value(We have set it to 2^248) i.e. the hash values have 2 leading zeros(difficulty = 256)

The links =>

/
GET: returns all the blocks in JSON format
POST: Explained later


/content : Add to content pool
GET: returns all the unmined contents in the content pool(Those which have not been added to the blockchain.
POST: receives a json object including the content which is added to the content pool. Returns the added content object.
Post request example: {“content”: “This text will be added to the content pool.” }
Request Response: {“id”: 6, “content”: “This text will be added to the content pool.”}


/mine : This link performs what is actually done by the miner on their own hardware. 
GET: returns all the unmined contents in the content pool(Those which have not been added to the blockchain.
POST: receives a json object containing the id of the content object to be mined. Returns the id of the request and nonce and hash value of new block.
Post request example: {“id”: 6}
Request Response: {“id”: 6, “nonce”: 519, “hash”: 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824 }


/add :
GET: returns all the unmined contents in the content pool(Those which have not been added to the blockchain.
POST: receives a json object containing the id of the content object to be mined and the nonce which the miner wants to submit. 
Returns the newly created block(if nonce checks out). Otherwise returns an error.
Post request example: {“id”: 6, “nonce”: 519}


While in a real blockchain all 3 events would take place separately, a user submits the content while the miner finds the nonce which is then validated by the blockchain,
here we have also created a way which combines all the tasks and directly adds a new block as a post request from the user is received which contains the content.
This can be found at  /
Post Request format: {“content”: “Content”}
This returns a json which contains the details of the newly added block.

