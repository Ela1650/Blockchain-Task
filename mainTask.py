import hashlib
import time
from typing import List
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

# Define the Transaction model
class Transaction(BaseModel):
    sender: str
    receiver: str
    amount: float

# Define the Block model
class Block(BaseModel):
    index: int
    timestamp: float
    transactions: List[Transaction]
    previous_hash: str
    proof: int
    hash: str

    def calculate_hash(self) -> str:
        """Calculate and return the hash of the block."""
        block_string = f"{self.index}{self.timestamp}{self.transactions}{self.previous_hash}{self.proof}"
        return hashlib.sha256(block_string.encode()).hexdigest()

# Blockchain class with debugging prints
class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """Create the first block in the blockchain (genesis block)."""
        genesis_block = Block(
            index=0,
            timestamp=time.time(),
            transactions=[],
            previous_hash="0",
            proof=100,
            hash="genesis_hash"
        )
        self.chain.append(genesis_block)

    def add_block(self, block: Block):
        """Add a new block to the chain if it's valid."""
        print(f"Validating Block: {block}")
        if self.is_valid_block(block):
            self.chain.append(block)
            print(f"Block added: {block}")
            return True
        else:
            print(f"Block is invalid: {block}")
            return False

    def mine_block(self):
        """Simulate the mining of a new block."""
        last_block = self.chain[-1]
        index = last_block.index + 1
        timestamp = time.time()
        proof = self.proof_of_work(last_block.proof)
        
        # Create a new block with the calculated hash
        block = Block(
            index=index,
            timestamp=timestamp,
            transactions=self.pending_transactions,
            previous_hash=last_block.hash,
            proof=proof,
            hash=""
        )
        
        # Calculate the hash for the new block
        block.hash = block.calculate_hash()
        
        # Reset the list of pending transactions after mining
        self.pending_transactions = []
        
        # Add the mined block to the blockchain
        self.add_block(block)
        return block

    def proof_of_work(self, last_proof: int) -> int:
        """Simple Proof of Work algorithm."""
        proof = 0
        while not self.is_valid_proof(last_proof, proof):
            proof += 1
        return proof

    def is_valid_proof(self, last_proof: int, proof: int) -> bool:
        """Check if the current proof is valid."""
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        print(f"Checking Proof: {guess_hash}")
        return guess_hash[:4] == "0000"

    def is_valid_block(self, block: Block) -> bool:
        """Check if a given block is valid."""
        last_block = self.chain[-1]
        print(f"Last Block: {last_block}")
        print(f"Block Index: {block.index}, Last Block Index: {last_block.index}")
        
        if block.index != last_block.index + 1:
            print(f"Index mismatch: {block.index} != {last_block.index + 1}")
            return False

        if block.previous_hash != last_block.hash:
            print(f"Previous Hash mismatch: {block.previous_hash} != {last_block.hash}")
            return False

        if not self.is_valid_proof(last_block.proof, block.proof):
            print(f"Invalid proof: {block.proof}")
            return False
        
        # Validate hash calculation
        calculated_hash = block.calculate_hash()
        if block.hash != calculated_hash:
            print(f"Hash mismatch: {block.hash} != {calculated_hash}")
            return False

        return True


# FastAPI app
app = FastAPI()
blockchain = Blockchain()

@app.post("/mine_block", response_model=Block)
async def mine_block():
    try:
        # Mine a new block
        block = blockchain.mine_block()
        return block
    except Exception as e:
        # Return detailed error response
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/new_transaction")
async def new_transaction(transaction: Transaction):
    blockchain.pending_transactions.append(transaction)
    return {"message": "Transaction added successfully."}

@app.post("/add_block")
async def add_block(block: Block):
    if blockchain.add_block(block):
        return {"message": "Block added successfully."}
    else:
        raise HTTPException(status_code=400, detail="Invalid block.")

@app.get("/chain")
async def get_chain():
    return blockchain.chain
