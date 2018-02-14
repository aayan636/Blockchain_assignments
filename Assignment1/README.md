# Description

This project is a simulation of blockchain.
- `block.py`        - Individual Block structure
  - Contains transactions, peer_id of peer who generated block, length of current blockchain

- `blockchain.py`   - Blockchain structure for each peer
  - Owned by each peer
  - Contains tree structure of blockchain
  - Manages adding new Transactions and new Blocks to Blockchain

- `main.py`         - Main function

- `message.py`      - Message structure exchanged between peers
  - Contains send function which send message to the receiver's Queue
  - Includes network delay
  - All send operations are non-blocking

- `params.py`       - All global parameters

- `peer.py`         - Peer structure
  - Contains async gen_transaction and gen_block
  - Contains thread safe Queue for reveiving messages
  - Note that we have used Semaphores to manage and process Queues in an async fashion
  - process_message manages sending message in a loopless fashion
  - render manages rendering the blockchain for the current peer

- `simulator.py`    - Simulates Peers' interaction
  - Generates and simulates the blockchain network
  - Simulator spawns individual independent peer threads
  - Peer threads' interaction is managed and documented

- `transaction.py`  - Transaction structure

# How to run

Prerequisite : ete2 package to render blockchain trees
Change the parameters in `params.py`

run `python main.py`

Press `ctrl + \` to take save the tree file of each node.
The output is saved in `outputs` folder
