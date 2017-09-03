#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

import snake_coin
import json

from flask import Flask
from flask import request
node = Flask(__name__)
'''
从现在开始，SnakeCoin的数据将会是一些交易记录，所以每一个区块的数据区将会是一个由交易记录组成的列表。
我们将会像下面一样定义一个交易记录。每一个交易记录都会是一个JSON对象，列举着SnakeCoin的发送方，SnakeCoin的接收方，和SnakeCoin转让的数量。
现在我们知道了我们的交易记录是怎样的了，我们需要把它们加入一台我们区块链网络中的电脑，
这被称为节点。为了这样做，我们会创建一个简单的HTTP服务器，这样任何用户都可以让我们的节点知道一个新的交易记录产生了。
一个节点将能够接受一个以交易记录作为body的POST请求。这就是为什么交易记录是JSON格式的原因，
我们需要把它们作为一个请求的body传送到我们的服务器。
'''

'''
现在当用户互相间发送SnakeCoin时，我们有了一个可以保存记录的方法。
这就是为什么人们把区块链称为公开的，分布式的分类账：所有交易记录的存储对所有人可见，
并且被保存在网络的每一个节点中。
'''

# Store the transactions that this node has in a list
this_nodes_transactions = []

@node.route('/txion', methods=['POST'])
def transaction():
	if request.method == 'POST':
		# On each new POST request, we extract the transaction data
		new_txion = request.get_json()
		# Then we add the transaction to our list
		this_nodes_transactions.append(new_txion)

		# Because the transaction was successfully submitted, we will log it to our console
		print("New transaction")
		print("FROM: {}".format(new_txion['from']))
		print("TO: {}".format(new_txion['to']))
		print("AMOUNT: {}".format(new_txion['amount']))

		# Then we let the client know it worked out
		return "Transaction submission successful\n"


minor_address = "q3nf394hjg-random-miner-address-34nf3i4nflkn3oi"

# 为了控制挖掘新区块的难度，我们会实现一个工作量证明（Proof-of-Work）算法。工作量证明算法本质上是生成一个难以被创造，
# 但易于被验证的结果。这个结果被称为证明，而且正如它听起来一样，它是一台电脑执行了确定数量的计算的证明。
###
# curl "localhost:5000/txion" -H "Content-Type: application/json" -d '{"from": "akjflw", "to": "fjlakdj", "amount": 3}'
###
def proof_of_work(last_proof):
	# Create a variable that we will use to find our next proof of work
	incrementor = last_proof + 1

	# Keep incrementing the incrementor until it's equal to a number divisible by 9
	# and the proof of work of the previous block in the chain
	while not (incrementor % 9 == 0 and incrementor % last_proof == 0):
		incrementor += 1

	# Once that number is found, we can return it as a proof of our work

	return incrementor

###
# curl localhost:5000/mine
###
@node.route('/mine', methods=['GET'])
def mine():
	# Get the last proof of work
	last_block = snake_coin.blockchain[len(snake_coin.blockchain) - 1]
	# last_proof = last_block.data['proof-of-work']
	last_proof = last_block.data[3]

	# Find the proof of work for the current block being mined
	# Note: The program will hang here until a new proof of work is found

	proof = proof_of_work(last_proof)

	# Once we find a valid proof of work, we know we can mine a block so we reward the miner by adding a transaction

	this_nodes_transactions.append(
		{"from": "network", "to": minor_address, "amount": 1}
	)

	# Now we can gather the data needed to create the new block
	new_block_data = {
		"proof-of-work": proof,
		"transactions": list(this_nodes_transactions)
	}
	new_block_index = last_block.index + 1
	new_block_timestamp = this_timestamp = snake_coin.date.datetime.now()
	last_block_hash = last_block.hash

	# Empty transaction list
	this_nodes_transactions[:] = []

	# Now create the new block!
	mined_block = snake_coin.Block(
		new_block_index,
		new_block_timestamp,
		new_block_data,
		last_block_hash
	)
	snake_coin.blockchain.append(mined_block)

	# Let the client know we mined a block
	return json.dumps({"index": new_block_index,
	                   "timestamp": str(new_block_timestamp),
	                   "data": new_block_data,
	                   "hash": last_block_hash}) + "\n"

# 并且我们能在网络上发行SnakeCoin给人们，使他们能互相发送了。但正如我们所说，我们只在一台电脑上做到了这些。
# 如果区块链是去中心化的，我们如何能够确定每一个节点中的链是一样的呢？为了做到这一点，我们让每一个节点广播它的链的版本给其他节点，
# 并且允许他们接受其他节点的链。这之后，每一个节点必须核实其他节点的链，所以每一个网络中的节点都与产生的区块链看起来一致了。
# 这被称为共识（consensus）算法。
@node.route('/blocks', methods=['GET'])
def get_blocks():
	'''
	如果一个节点的链与另一个节点的不一样（就是说有冲突），然后网络中最长的链会保留下来，
	其他较短的链将会被删除。如果我们网络中的链之间没有冲突，那么我们继续。
	'''
	chain_to_send = snake_coin.blockchain

	# Convert our blocks into dictionaries so we can send them as json objects later
	for block in chain_to_send:
		block_index = str(block.index)
		block_timestamp = str(block.timestamp)
		block_data = str(block.data)
		block_hash = block.hash
		block = {
			"index": block_index,
			"timestamp": block_timestamp,
			"data": block_data,
			"hash": block_hash
		}

	# Send our chain to whomever requested it
	chain_to_send = json.dumps(chain_to_send)
	return chain_to_send

def find_new_chains():
	# Get the blockchains of every other node
	other_chains = []

	for node_url in peer_nodes:
		# Get their chains using a GET request
		block = requests.get(node_url + "/blocks").content

		# Convert the JSON object to a Python dictionary
		block = json.loads(block)

		# Add it to our list
		other_chains.append(block)

	return other_chains

def consensus():
	# Get the blocks from other nodes
	other_chains = find_new_chains()

	# If our chain isn't longest, then we store the longest chain
	longest_chain = snake_coin.blockchain
	for chain in other_chains:
		if len(longest_chain) < len(chain):
			longest_chain = chain

	# If the longest chain wasn't ours, then we set our chain to the longest
	snake_coin.blockchain = longest_chain

node.run()