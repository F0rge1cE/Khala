import hashlib
import json
from time import time # time() return unix time
from uuid import uuid4

from textwrap import dedent
from flask import Flask, jsonify, request

import BlockChain

# Instantiate a new node
app = Flask(__name__)

# Generate an unique ID for the node
nodeID = str(uuid4()).replace('-', '')

# Instantiate the BlockChain object
blockchain = BlockChain.Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
	# Use the proof of work algorithm to get the next proof
	lastBlock = blockchain.lastBlock
	lastProof = lastBlock['proof']

	proof = blockchain.proof_of_work(lastProof)

	# Given a reward for finding the proof
	# Sender '0' signify that this node has mined a new coin
	blockchain.newTransaction(
		sender='0', 
		recipient=nodeID,
		amount=1,
		)

	# Forge the new Block by adding it to the chain
	previous_hash = blockchain.hash(lastBlock)
	block = blockchain.newBlock(previous_hash=previous_hash, proof=proof)

	response = {
		'message': "New block forged",
		'index': block['index'],
		'transactions': block['transactions'],
		'proof': block['proof'],
		'previous_hash': block['previous_hash'],
	}
	return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
	values = request.get_json()

	# Check that the required fields are in the POST'ed data
	required = ['sender', 'recipient', 'amount']
	if not all(k in values for k in required):
		return 'Miss values', 400

	# Create a new transaction
	index = blockchain.newTransaction(values['sender'], values['recipient'], values['amount'])
	

	response = { 
		'message': f'This transaction will be added to block # {index}'
	}

	return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
	response = {
		'chain': blockchain.chain,
		'length': len(blockchain.chain)
	}

	return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
	values = request.get_json()

	nodes = values.get('nodes')
	if nodes is None:
		return "Error: invalid list of Nodes", 400

	for node in nodes:
		blockchain.registerNode(node)

	response = {
		'message': 'New nodes have been added!',
		'total_nodes': list(blockchain.nodes),
	}
	return jsonify(response), 201


@app.route('/nodes/resolve', methods=['POST']):
def consensus():
	replaced = blockchain.resolve_conflicts()

	if replaced:
		response = {
			'message': 'Our chain was replaced!'
			'new_chain': blockchain.chain
		}
	else:
		response = {
			'message': 'Our chain was authoritative!'
			'chain': blockchain.chain
		}
return jsonify(response), 200





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)






