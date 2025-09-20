import json
from blockchain import Blockchain, Block, Transaction

def save_blockchain_to_file(blockchain, filename='chain.json'):
    with open(filename, 'w') as f:
        json.dump(blockchain.to_dict(), f, indent=4)
    print(f"Blockchain saved to {filename}")

def load_blockchain_from_file(filename='chain.json', difficulty=3):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        bc = Blockchain(difficulty)
        bc.chain = []
        for block_data in data['chain']:
            transactions = [Transaction(**tx) for tx in block_data['transactions']]
            block = Block(block_data['index'], transactions, block_data['previous_hash'], block_data['validator'])
            block.timestamp = block_data['timestamp']
            block.nonce = block_data['nonce']
            block.hash = block_data['hash']
            block.merkle_root = block_data['merkle_root']
            bc.chain.append(block)
        bc.stake = data['stake']
        bc.nodes = data['nodes']
        return bc
    except FileNotFoundError:
        print("No saved chain found, starting new.")
        return Blockchain(difficulty)