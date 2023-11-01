#! /usr/bin/env python3

import datetime
import hashlib
import json
import sys


class wyp_blockchain():
    def __init__(self):
        """Constructor. Initilises the chain and adds the genesis block."""
        self.chain = []
        self.add_block(p_proof=1, p_previous_hash="0")


    def add_block(self, p_proof, p_previous_hash):
        """Adds a new block to the current chain.

        Parameters
        p_proof: The proof of the new block.
        p_previous_hash: Value the previous hash.

        Returns: The new block that was added. Note that the block is already automatically appended to the chain.         
        """
        block = {'index': len(self.chain)+1, # New block is size of current chain + 1.
                 'timestamp': datetime.datetime.now(datetime.timezone.utc).isoformat(), # The UTC time this block is created.
                 'proof': p_proof, # The proof that this block solves the blockchain problem.
                 'previous_hash': p_previous_hash # The previous hash of the previous block
                 }
        self.chain.append(block)
        self.print_block(-1, "New block added: ")
        return block

    
    def print_block(self, p_index, p_pretext=""):
        """Prints a block in the chain to stdout.
        
        Parameters
        p_index: The index in the chain to print.
        p_pretext: Prepends some text to be printed where required.
        """
        print(p_pretext+json.dumps(self.chain[p_index], sort_keys=True))


    def get_last_block(self):
        """Returns the last block in the chain."""
        return self.chain[-1]
    

    def mine_proof(self):
        """Mines a new proof. In this implementation we simply use the proof value in the previous block. Returns the new proof as a numerical value."""
        new_proof = 1
        proof_ok = False
        while proof_ok is False:
            proof_hash = hashlib.sha256(str(new_proof**2 - self.chain[-1]['proof']**2).encode()).hexdigest() # Try to mine a proof candidate
            if proof_hash[:4] == '0000': # Mining condition. In this example 1st 4 chars in the hash must be '0000'.
                proof_ok = True
            else:
                new_proof += 1
        return new_proof


    def compute_hash(self, p_block):
        """Computes and returns the hash of a block.
        
        Parameters
        p_block: The block to compute the hash for.
        """
        return hashlib.sha256(json.dumps(p_block, sort_keys=True).encode()).hexdigest()
    

    def full_validity_check(self):
        """Checks the validity of the entire chain, returning True if OK, False if Not. Status and progress of checks are printed to stdout."""
        print("Checking All Blocks")
        self.print_block(0, "Genesis Block: ")
        index = 1
        while index < len(self.chain): # Iterate through the chain and check all blocks.           
            if self.chain[index]['previous_hash'] != self.compute_hash(self.chain[index-1]['proof']): # Check the hash of the previous block matches record in current block
                self.print_block(index, "Block Not OK: ")
                return False
            proof_hash = hashlib.sha256(str(self.chain[index]['proof']**2 - self.chain[index-1]['proof']**2).encode()).hexdigest() # Verify the proof for the current block is correct
            if proof_hash[:4] != '0000':
                self.print_block(index, "Block Not OK: ")
                return False

            self.print_block(index, "Block OK: ")            
            index += 1

        print("All Blocks OK.")
        return True
    

    def get_chain(self):
        """Returns the entire blockchain."""
        return self.chain
    

def unit_test():
    """Runs the unit test on this module."""
    print("Running unit test for "+sys.argv[0])
    my_blockchain = wyp_blockchain() # Create a block with only the genesis block.
    my_blockchain.add_block(my_blockchain.mine_proof(), my_blockchain.compute_hash(my_blockchain.get_last_block()['proof'])) # Add a block
    my_blockchain.add_block(my_blockchain.mine_proof(), my_blockchain.compute_hash(my_blockchain.get_last_block()['proof'])) # Add another block  
    my_blockchain.full_validity_check() # Check the entire blockchain
    return 0

if __name__ =='__main__':
    sys.exit(unit_test())