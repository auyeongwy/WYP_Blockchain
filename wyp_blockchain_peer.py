#! /usr/bin/env python3

from flask import Flask, jsonify
from wyp_blockchain import wyp_blockchain

class wyp_blockchain_peer(wyp_blockchain):
    """Constructor. Initialises the blockchain and sets up the Flask server."""
    def __init__(self):
        wyp_blockchain.__init__(self) # Init blockchain parent.
        

        self.app = Flask(__name__)
        @self.app.route('/mine_block', methods=['GET']) # Endpoint to mine a new block.
        def mine_block():
            new_block = self.add_block(self.mine_proof(), self.compute_hash(self.get_last_block()['proof']))
            return jsonify(new_block), 200
        

        @self.app.route('/get_chain', methods=['GET']) # Endpoint to get the current blockchain.
        def get_chain():
            return jsonify(self.get_chain()), 200


        @self.app.route('/chain_full_check', methods=['GET']) # Endpoint to verify the entire blockchain.
        def chain_full_check():
            if self.full_validity_check() is True:
                return jsonify({'Full Validity Check':'OK'}), 200
            else:
                return jsonify({'Full Validity Check':'Fail'}), 200


blockchain_peer = wyp_blockchain_peer()
blockchain_peer.app.run() # Flask server mode to wait for network requests