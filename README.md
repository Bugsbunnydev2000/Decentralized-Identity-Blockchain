# Decentralized-Identity-Blockchain
A simple decentralized blockchain implementation focused on managing digital identities and verifiable credentials.
This project demonstrates a basic Proof-of-Stake (PoS) blockchain with peer-to-peer synchronization, transaction signing using ECDSA, Merkle trees for integrity, and a Flask-based API for interacting with the chain.
It's designed for educational purposes to showcase how blockchain can be used for secure, tamper-proof identity management, such as issuing and verifying credentials (e.g., certifications or user verifications).

# Project Overview

# What It Does : 

Blockchain Core: Maintains a chain of blocks containing transactions. Each transaction represents the issuance or transfer of a credential (e.g., "Certified Developer" issued by an authority).

Digital Identities: Uses public-private key pairs (wallets) for signing and verifying transactions, ensuring authenticity.

Consensus Mechanism: Simple Proof-of-Stake (PoS) where validators are chosen based on stake amounts. Blocks are "mined" by solving a basic nonce-based puzzle with adjustable difficulty.

P2P Synchronization: Nodes can sync chains with peers to adopt the longest valid chain.

Credential Verification: Built-in method to verify if a credential exists in the chain, is signed by the correct issuer, and belongs to the recipient.

API Endpoints: A Flask app provides RESTful APIs for getting the chain, adding transactions, mining blocks, verifying credentials, and creating signed transactions.

Security Features: Transactions are signed with ECDSA (SECP256k1 curve), and blocks use Merkle roots for efficient verification.

# Goals : 

1- Demonstrate decentralized identity management without a central authority.

2- Provide a lightweight blockchain example for learning purposes, including cryptography, networking, and consensus.

3- Allow users to issue, store, and verify credentials in a tamper-resistant way.

4- Support multi-node setups to simulate a distributed network.

# This is not production-ready—it's a proof-of-concept with simplifications (e.g., no advanced security against attacks, limited scalability).

-------------------------------------

# Prerequisites : 

Python 3.8+: The project uses Python features and libraries compatible with recent versions.

```bash
pip install -r requirements.txt
```

Key libraries:

ecdsa: For elliptic curve digital signatures.

flask: For the API server.

requests: For HTTP communication between nodes.

No external databases or services are required. The blockchain state is stored in a local JSON file.

--------------------------

# Installation : 

1- Clone the repository:

```bash
git clone https://github.com/Bugsbunnydev2000/Decentralized-Identity-Blockchain.git
cd Decentralized-Identity-Blockchain
```

2- Install dependencies : 

```bash
pip install -r requirements.txt
```
-----------------------------------

# How to Run : 
The project includes scripts for running nodes and an API server. Nodes communicate over localhost on ports 5000 and 5001 by default.

# Running Nodes : 

```bash
python main.py
```

Starts a server on localhost:5000.
Creates sample wallets, adds stake, creates transactions, mines a block, and broadcasts it.
Syncs with other nodes (e.g., Node 2).

# Node 2 (Secondary Node):

Run this in a separate terminal:

```bash
python node2.py
```

Starts a server on localhost:5001.
Similar to Node 1: creates transactions, mines, and broadcasts.
Syncs with Node 1.

After running both, the nodes will sync chains. Check console output for mining logs, transaction hashes, and chain validity.

Running the API Server

The API provides endpoints for interacting with the blockchain. Run it in a separate terminal:

```bash
python app.py
```

Starts Flask on localhost:8000.

It loads the blockchain from chain.json (if exists) and syncs with nodes on ports 5000/5001.

API Endpoints

GET /chain: Returns the full blockchain as JSON.

POST /transaction: Add a new transaction (requires JSON with from_address, to_address, data, signature, timestamp).

POST /mine: Mine a new block with pending transactions.

POST /verify_credential: Verify a credential (requires JSON with credential_id, issuer_address, recipient_address).

POST /create_transaction: Create and add a signed transaction using the API's wallet (requires JSON with to_address, credential_id, details).

Example using curl to create a transaction:

```bash
curl -X POST http://localhost:8000/create_transaction -H "Content-Type: application/json" -d '{"to_address": "recipient_public_key", "credential_id": "Certified Developer", "details": "Issued by University X"}'
```

# Blockchain Persistence

The chain is saved to chain.json after mining.

On startup, nodes load from chain.json if it exists; otherwise, a new genesis chain is created.

# Testing

Run nodes and API as above.

Use tools like Postman or curl to interact with the API.

Verify chain integrity: After mining, check console for "Is chain valid? True".

Test verification: Use the /verify_credential endpoint with data from sample transactions.

# Acknowledgments : 

Built with inspiration from blockchain tutorials and libraries like ECDSA for cryptography. 

Special thanks to Grok, Chatgpt, and YouTube for learning and understanding the basics of blockchain.

# This project its just for fun and learning . 
