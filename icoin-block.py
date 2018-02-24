from flask import Flask
from flask import request
import json
import requests
import hashlib as hasher
import datetime as date
node = Flask(__name__)

#Definition of an indy coin block
class Block:
	def __init__(self, index, timestamp, data, previous_hash):
		self.index = index
		self.timestamp = timestamp
		self.data = data
		self.previous_hash = previous_hash
		self.hash = self.hash_block()
		
	def hash_block(self):
		sha = hasher.sha256()
		sha.update(str(self.index) + 
				   str(self.timestamp) + 
				   str(self.data) +
				   str(self.previous_hash))
		return sha.hexdigest()

def create_genesis_block():
	return Block(0, date.datetime.now(), {
		"proof-of-work": 9,
		"transactions": None
	}, "0")

miner_address = "qow204kkvj302-some-address-a5s13x5s8e652c515s"
blockchain = []
blockchain.append(create_genesis_block())
this_nodes_transactions = []
peer_nodes = []
mining = true

def next_block(last_block):
	this_index = last_block.index + 1
	this_timestamp = date.datetime.now()
	this_data = "Block: " + str(this_index)
	this_hash = last_block.hash
	return Block(this_index, this_timestamp, this_data, this_hash)
	
blockchain = [create_genesis_block()]
previous_block = blockchain[0]

initial_blocks = 20

for i in range(0, initial_blocks):
	
	block_to_add = next_block(previous_block)
	blockchain.append(block_to_add)
	previous_block = block_to_add
	
	print("Block #{} has been added to the blockchain.".format(block_to_add.index))
	print("Hash: {}\n".format(block_to_add.hash))
	

	
@node.route('/transaction', methods=['POST'])
def transaction():
	new_transaction = request.getjson()
	this_nodes_transactions.append(new_transaction)
	
	print "New transaction"
	print "FROM: {}".format(new_transaction['from'].encode('ascii', 'replace'))
	print "TO: {}".format(new_transaction['to'].encode('ascii', 'replace'))
	print "AMOUNT: {}\n".format(new_txion['amount'])
	
	return "Transaction successful\n"
	
@node.route('/blocks', methods=['GET'])
def get_blocks():
	chain_to_send = blockchain
	for i in range(len(chain_to_send)):
		block = chain_to_send[i]
		block_index = str(block.index)
		block_timestamp = str(block.timestamp)
		block_data = str(block.data)
		block_hash = block.hash
		chain_to_send[i] = {
			"index": block_index,
			"timestamp": block_timestamp,
			"data": block_data,
			"hash": block_hash
		}
	chain_to_send = json.dumps(chain_to_send)
	return chain_to_send
	
def proof_of_work(last_proof):
	incrementor = last_proof + 1
	while not (imcrementor % 9 == 0 and incrementor % last_proof == 0):
		incrementor += 1
	return incrementor
	
@node.route('/mine', methods = ['GET'])
def mine():
	last_block = blockchain[len(blockchain) - 1]
	last_proof = last_block.data['proof-of-work]
	proof = proof_of_work(last_proof)
	this_nodes_transactions.append(
		{ "from": "network", "to": miner_address, "amount": 1 }
	)
	new_block_data = {
		"proof-of-work": proof,
		"transactions": list(this_nodes_transactions)
	}
	new_block_index = last_block.index + 1
	new_block_timestamp = this_timestamp = date.datetime.now()
	last_block_hash = last_block.hash
	
	this_nodes_transactions[:] = []
	mined_block = Block(
		new_block_index,
		new_block_timestamp,
		new_block_data,
		last_block_hash
	)
	blockchain.append(mined_block)
	
	return json.dumps({
		"index": new_block_index
		"timestamp": str(new_block_timestamp)
		"data": new_block_data,
		"hash": last_block_hash
	}) + "\n
