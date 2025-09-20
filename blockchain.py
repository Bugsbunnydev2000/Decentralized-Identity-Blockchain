import hashlib
import json
import datetime
from merkle import MerkleTree
from wallet import Wallet
import requests

class Transaction:
    def __init__(self, from_address, to_address, data, signature=None, timestamp=None):
        self.from_address = from_address
        self.to_address = to_address
        self.data = data
        self.timestamp = timestamp or datetime.datetime.now().isoformat()
        self.signature = signature

    def get_unsigned_dict(self):
        return {
            'from_address': self.from_address,
            'to_address': self.to_address,
            'data': self.data,
            'timestamp': self.timestamp
        }

    def get_signing_hash(self):
        return hashlib.sha256(json.dumps(self.get_unsigned_dict(), sort_keys=True).encode()).digest()

    def calculate_hash(self):
        return self.get_signing_hash().hex()

    def sign_transaction(self, signing_key):
        import ecdsa
        try:
            sk = ecdsa.SigningKey.from_string(bytes.fromhex(signing_key), curve=ecdsa.SECP256k1)
            hash_tx = self.get_signing_hash()
            self.signature = sk.sign(hash_tx).hex()
            print(f"Signed transaction with hash: {self.calculate_hash()[:10]}...")
        except Exception as e:
            print(f"Sign error: {e}")
            raise

    def is_valid(self):
        if not self.signature or not self.from_address:
            print("Validation failed: Missing signature or from_address")
            return False
        import ecdsa
        try:
            vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(self.from_address), curve=ecdsa.SECP256k1)
            hash_tx = self.get_signing_hash()
            return vk.verify(bytes.fromhex(self.signature), hash_tx)
        except Exception as e:
            print(f"Validation error: {e}")
            return False

    def to_dict(self):
        return {
            'from_address': self.from_address,
            'to_address': self.to_address,
            'data': self.data,
            'timestamp': self.timestamp,
            'signature': self.signature
        }

class Block:
    def __init__(self, index, transactions, previous_hash, validator):
        self.index = index
        self.timestamp = datetime.datetime.now().isoformat()
        self.transactions = transactions
        self.merkle_root = MerkleTree([tx.calculate_hash() for tx in transactions]).get_root() if transactions else '0'
        self.previous_hash = previous_hash
        self.validator = validator
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        hash_string = str(self.index) + self.timestamp + self.merkle_root + self.previous_hash + str(self.nonce) + self.validator
        return hashlib.sha256(hash_string.encode()).hexdigest()

    def mine_block(self, difficulty):
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block {self.index} mined by {self.validator}: {self.hash}")

    def to_dict(self):
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': [tx.to_dict() for tx in self.transactions],
            'merkle_root': self.merkle_root,
            'previous_hash': self.previous_hash,
            'validator': self.validator,
            'nonce': self.nonce,
            'hash': self.hash
        }

class Blockchain:
    def __init__(self, difficulty=3):
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty
        self.pending_transactions = []
        self.stake = {}  # {address: amount}
        self.nodes = []  # [('host', port)]

    def create_genesis_block(self):
        return Block(0, [], "0", "Genesis Validator")

    def add_stake(self, address, amount):
        self.stake[address] = self.stake.get(address, 0) + amount

    def choose_validator(self):
        if not self.stake:
            return "Default Validator"
        return max(self.stake, key=self.stake.get)

    def add_transaction(self, transaction):
        if transaction.is_valid():
            self.pending_transactions.append(transaction)
            print(f"Transaction added: {transaction.calculate_hash()[:10]}...")
        else:
            print("Transaction validation failed!")
            raise ValueError("Invalid transaction signature or data")

    def mine_pending_transactions(self):
        validator = self.choose_validator()
        block = Block(len(self.chain), self.pending_transactions[:], self.chain[-1].hash, validator)
        block.mine_block(self.difficulty)
        self.chain.append(block)
        self.pending_transactions = []
        return block

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
            if current.merkle_root != MerkleTree([tx.calculate_hash() for tx in current.transactions]).get_root():
                return False
            for tx in current.transactions:
                if not tx.is_valid():
                    return False
        return True

    def add_node(self, host, port):
        self.nodes.append((host, port))

    def to_dict(self):
        return {
            'chain': [block.to_dict() for block in self.chain],
            'difficulty': self.difficulty,
            'stake': self.stake,
            'nodes': self.nodes
        }

    def verify_credential(self, credential_id, issuer_address, recipient_address):
        """
        Verify if a credential exists in the blockchain and is valid.
        Args:
            credential_id (str): The credential identifier (e.g., 'Certified Developer').
            issuer_address (str): Public key of the issuer (from_address).
            recipient_address (str): Public key of the recipient (to_address).
        Returns:
            dict: {'valid': bool, 'details': str or dict, 'block_index': int or None}
        """
        for block in self.chain:
            for tx in block.transactions:
                if (tx.data.get('credential') == credential_id and
                    tx.from_address == issuer_address and
                    tx.to_address == recipient_address and
                    tx.is_valid()):
                    return {
                        'valid': True,
                        'details': tx.data,
                        'block_index': block.index
                    }
        return {'valid': False, 'details': 'Credential not found or invalid', 'block_index': None}

    def sync_chain(self):
        """
        Synchronize the chain with other nodes, adopting the longest valid chain.
        """
        longest_chain = self.chain
        max_length = len(self.chain)
        for host, port in self.nodes:
            try:
                response = requests.get(f'http://{host}:{port}/chain')
                if response.status_code == 200:
                    data = response.json()
                    chain = [Block(**block) for block in data['chain']]
                    if len(chain) > max_length and Blockchain(difficulty=self.difficulty, chain=chain).is_chain_valid():
                        longest_chain = chain
                        max_length = len(chain)
                        self.stake = data['stake']
                        self.nodes = data['nodes']
            except Exception as e:
                print(f"Failed to sync with {host}:{port}: {e}")
        self.chain = longest_chain
        print(f"Synced chain, length: {len(self.chain)}")