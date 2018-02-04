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
	return "Mining a new block!"


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
	values = request.get_json()

	# Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
    	return 'Miss values', 400

    # Create a new transaction
    index = blockchain.newTransaction(values['sender'], values['recipient'], values['amount'])

    response = { 'message': f'This transaction will be added to block # {index}' }
	return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def funn_chain():
	response = {
		'chain': blockchain.chain
		'length': len(blockchain.chain)
	}

	return jsonify(response), 200



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)






