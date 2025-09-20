import threading
from blockchain import Blockchain
from wallet import Wallet
from network import start_server, broadcast_block
from utils import load_blockchain_from_file, save_blockchain_to_file

if __name__ == "__main__":
    
    nexus_forge = load_blockchain_from_file()

    
    nexus_forge.nodes = [] 
    nexus_forge.add_node('localhost', 5000)  

    print("Syncing chain...")
    nexus_forge.sync_chain()

    server_thread = threading.Thread(target=start_server, args=(nexus_forge, 'localhost', 5001))
    server_thread.start()

    wallet1 = Wallet()
    wallet2 = Wallet()
    print(f"Wallet1 Public (Issuer): {wallet1.public_key}")
    print(f"Wallet2 Public (Recipient): {wallet2.public_key}")
    nexus_forge.add_stake(wallet1.public_key, 100)
    nexus_forge.add_stake(wallet2.public_key, 50)

    print("Creating tx1...")
    tx1 = wallet1.create_transaction(wallet2.public_key, {'identity': 'Alice', 'credential': 'Certified Developer', 'details': 'Issued by University X'})
    print(f"tx1 hash: {tx1.calculate_hash()[:10]}..., valid: {tx1.is_valid()}")

    print("Creating tx2...")
    tx2 = wallet2.create_transaction(wallet1.public_key, {'identity': 'Bob', 'credential': 'Verified User'})
    print(f"tx2 hash: {tx2.calculate_hash()[:10]}..., valid: {tx2.is_valid()}")

    nexus_forge.add_transaction(tx1)
    nexus_forge.add_transaction(tx2)

    print("Mining block...")
    new_block = nexus_forge.mine_pending_transactions()
    broadcast_block(new_block, nexus_forge.nodes, self_host='localhost', self_port=5001)

    print("Is chain valid?", nexus_forge.is_chain_valid())
    print("Chain length:", len(nexus_forge.chain))
    save_blockchain_to_file(nexus_forge)

    print("Press Enter to exit...")
    input()