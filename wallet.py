import ecdsa
import hashlib

class Wallet:
    def __init__(self):
        
        sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1, hashfunc=hashlib.sha256)
        self.private_key = sk.to_string().hex()
        self.public_key = sk.verifying_key.to_string().hex()
        print(f"Wallet Public: {self.public_key[:20]}...") 

    def create_transaction(self, to_address, data):
        from blockchain import Transaction
        tx = Transaction(self.public_key, to_address, data)
        tx.sign_transaction(self.private_key)
        return tx