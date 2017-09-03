#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
import hashlib as hasher
import datetime as date

'''
我们首先定义我们的块将是什么样子。在块链中，每个块都有时间戳和可选的索引，
在SnakeCoin中，将同时存储两者，并且为了帮助确保整个块链的完整性，每个块将具有自识别散列。
像比特币一样，每个块的散列将是块的索引，时间戳，数据以及前一个块的哈希散列的加密散列。
当然，这些数据可以是任何你想要的。
'''
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

'''
我们正在创建一个块链，需要向实际的链条添加块。如前所述，每个块都需要上一个块的信息。
也就是说，出现了一个问题：块区中的第一个块怎么到达那里？因此，第一个块，或起源块，
是一个特殊的块。在许多情况下，它是手动添加的或具有允许添加的唯一逻辑值。
'''
def create_genesis_block():
	# Manually construct a block with
	# index zero and arbitrary previous hash
	return Block(0, date.datetime.now(), 'Genesis Block', 0)


'''
我们需要一个函数来生成块链中的后续块。该函数将将链中的前一个块作为参数，
创建要生成的块的数据，并返回具有其相应数据的新块。当新块得到先前块中的哈希信息时，
块链的完整性随着每个新的块而增加。如果我们没有这样做，外界信息会更容易“改变过去”，
并用自己的更新变化来替代我们的链条。这个哈希链作为加密证明，有助于确保一旦块被添加到块链中，
它不能被替换或删除。
'''
def next_block(last_block):
	this_index = last_block.index + 1
	this_timestamp = date.datetime.now()
	this_data = "Hey! I'm block ", str(this_index)
	this_hash = last_block.hash
	return Block(this_index, this_timestamp, this_data, this_hash)


# def main():
'''
创建我们的blockchain！在我们的例子中，blockchain本身就是一个简单的Python列表。
列表的第一个元素是起源块。当然，我们需要添加后续的块。因为SnakeCoin是最小的块，
所以我们只添加20个新的块。我们可以用for循环来做到这一点。
'''
# Create the blockchain and add the genesis block to the chain
blockchain = [create_genesis_block()]
previous_block = blockchain[0]

# How many blocks need to be added to the chain
# after the genesis block
num_of_block_to_be_added = 20

for i in range(0, num_of_block_to_be_added):
	block_to_add = next_block(previous_block)
	blockchain.append(block_to_add)
	previous_block = block_to_add
	# Tell everyone about it
	print("Block #{} has been added to the block chain!".format(block_to_add.index))
	print("Hash: {}\n".format(block_to_add.hash))

# if __name__ == '__main__':
# 	main()