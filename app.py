from flask import Flask, jsonify, request
from blockchain import Blockchain, Transaction
from wallet import Wallet
from utils import load_blockchain_from_file, save_blockchain_to_file

app = Flask(__name__)
nexus_forge = load_blockchain_from_file()


nexus_forge.nodes = [('localhost', 5000), ('localhost', 5001)]
nexus_forge.sync_chain()   
wallet = Wallet()  

@app.route('/chain', methods=['GET'])
def get_chain():
    nexus_forge.sync_chain()  
    return jsonify(nexus_forge.to_dict())

@app.route('/transaction', methods=['POST'])
def new_transaction():
    data = request.get_json()
    required = ['from_address', 'to_address', 'data', 'signature', 'timestamp']
    if not all(k in data for k in required):
        return jsonify({'message': 'Missing fields'}), 400
    tx = Transaction(data['from_address'], data['to_address'], data['data'], 
                     data['signature'], data['timestamp'])
    try:
        nexus_forge.add_transaction(tx)
        return jsonify({'message': 'Transaction added', 'tx_hash': tx.calculate_hash()}), 201
    except ValueError as e:
        return jsonify({'message': str(e)}), 400

@app.route('/mine', methods=['POST'])
def mine_block():
    nexus_forge.sync_chain() 
    block = nexus_forge.mine_pending_transactions()
    save_blockchain_to_file(nexus_forge)
    return jsonify({'message': 'Block mined', 'block': block.to_dict()}), 201

@app.route('/verify_credential', methods=['POST'])
def verify_credential():
    data = request.get_json()
    required = ['credential_id', 'issuer_address', 'recipient_address']
    if not all(k in data for k in required):
        return jsonify({'message': 'Missing fields'}), 400
    nexus_forge.sync_chain()  
    result = nexus_forge.verify_credential(
        data['credential_id'], 
        data['issuer_address'], 
        data['recipient_address']
    )
    return jsonify(result), 200

@app.route('/create_transaction', methods=['POST'])
def create_transaction():
    data = request.get_json()
    required = ['to_address', 'credential_id', 'details']
    if not all(k in data for k in required):
        return jsonify({'message': 'Missing fields'}), 400
    tx_data = {'identity': 'User', 'credential': data['credential_id'], 'details': data['details']}
    tx = wallet.create_transaction(data['to_address'], tx_data)
    nexus_forge.add_transaction(tx)
    return jsonify({
        'message': 'Transaction created and added',
        'tx_hash': tx.calculate_hash(),
        'signature': tx.signature,
        'from_address': wallet.public_key
    }), 201

if __name__ == '__main__':
    app.run(port=8000)