import socket
import threading
import json
from blockchain import Block, Transaction

def start_server(blockchain, host='localhost', port=5000):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Node listening on {host}:{port}")
    while True:
        conn, addr = server.accept()
        data = conn.recv(8192)
        if data:
            try:
                received_data = json.loads(data.decode())
                transactions = [Transaction(**tx) for tx in received_data['transactions']]
                block = Block(received_data['index'], transactions, received_data['previous_hash'], received_data['validator'])
                block.nonce = received_data['nonce']
                block.timestamp = received_data['timestamp']
                block.hash = received_data['hash']
                block.merkle_root = received_data['merkle_root']
                
                if block.hash == block.calculate_hash() and blockchain.chain[-1].hash == block.previous_hash:
                    blockchain.chain.append(block)
                    print(f"Received and added block {block.index} from {addr}")
                else:
                    print(f"Invalid block received from {addr}: hash_valid={block.hash == block.calculate_hash()}, prev_hash_match={blockchain.chain[-1].hash == block.previous_hash}")
            except Exception as e:
                print(f"Error receiving block from {addr}: {e}")
        conn.close()

def broadcast_block(block, nodes, self_host='localhost', self_port=5000):
    block_dict = block.to_dict()
    for host, port in nodes:
        if host == self_host and port == self_port:  
            continue
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            s.sendall(json.dumps(block_dict).encode())
            s.close()
            print(f"Broadcasted block {block.index} to {host}:{port}")
        except Exception as e:
            print(f"Failed to broadcast to {host}:{port}: {e}")