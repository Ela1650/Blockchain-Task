# Blockchain & UTXO Model with FastAPI

This project demonstrates how to implement a **Blockchain** using **FastAPI** and a simple **UTXO (Unspent Transaction Output)** model for managing transactions. The blockchain API provides endpoints for mining blocks, adding transactions, and viewing the blockchain. Additionally, a UTXO model is implemented to validate transactions ensuring input and output amounts match.

## Features

### Blockchain API (FastAPI)
- **Mining a New Block**: Trigger the mining process and add a new block to the blockchain.
- **New Transaction**: Add a new transaction with sender, receiver, and amount.
- **Add Block**: Manually add a block to the blockchain with validation.
- **View Blockchain**: Fetch the current blockchain.

### UTXO Model
- **UTXO Model**: Define unspent transaction outputs (UTXOs) using Pydantic.
- **Transaction Validation**: Ensure that the sum of inputs equals the sum of outputs in a transaction.

## Getting Started

### Prerequisites
Make sure you have the following installed:
- Python 3.7+
- pip (Python package manager)

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Ela1650/Blockchain-Task.git
    cd Blockchain-Task
    ```

2. Set up a virtual environment:
    ```bash
    python -m venv .venv
    ```

3. Activate the virtual environment:
    - **Windows**:
      ```bash
      .\.venv\Scripts\activate
      ```
    - **macOS/Linux**:
      ```bash
      source .venv/bin/activate
      ```

4. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

5. Run the FastAPI application:
    ```bash
    uvicorn main:app --reload
    ```
    The API will be available at `http://127.0.0.1:8000`.

## API Endpoints

### 1. `/mine_block` - Trigger Mining of a New Block
**Method**: `POST`  
**Description**: Mines a new block and adds it to the blockchain.  
**Response**:
```json
{
  "index": 1,
  "timestamp": 1633112321.12345,
  "transactions": [],
  "previous_hash": "genesis_hash",
  "proof": 100,
  "hash": "some_calculated_hash_value"
}
```

### 2. `/new_transaction` - Add a New Transaction
**Method**: `POST`  
**Request Body**:
```json
{
  "sender": "Alice",
  "receiver": "Bob",
  "amount": 50.0
}
```
**Response**: 
```json
{
  "message": "Transaction added successfully."
}
```

### 3. `/add_block` - Add a Block to the Blockchain
**Method**: `POST`  
**Request Body**: A block object containing transactions.  
**Response**:
```json
{
  "message": "Block added successfully."
}
```
**If invalid block**:
```json
{
  "detail": "Invalid block."
}
```

### 4. `/chain` - View the Blockchain
**Method**: `GET`  
**Response**: The current state of the blockchain.
```json
[
  {
    "index": 0,
    "timestamp": 1633112321.12345,
    "transactions": [],
    "previous_hash": "0",
    "proof": 100,
    "hash": "genesis_hash"
  },
  {
    "index": 1,
    "timestamp": 1633112321.6789,
    "transactions": [
      {
        "sender": "Alice",
        "receiver": "Bob",
        "amount": 50.0
      }
    ],
    "previous_hash": "genesis_hash",
    "proof": 100,
    "hash": "some_calculated_hash_value"
  }
]
```

## UTXO Model

The **UTXO Model** is a way of managing unspent transaction outputs (UTXOs) for the blockchain transactions. Each transaction has **inputs** (existing UTXOs) and **outputs** (new UTXOs). The model ensures that the sum of the inputs equals the sum of the outputs.

### UTXO Model Example

```python
from pydantic import BaseModel, Field
from uuid import uuid4
from typing import List

class UTXO(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    amount: float
    recipient: str

class Transaction(BaseModel):
    inputs: List[UTXO]
    outputs: List[UTXO]

    def validate_transaction(self):
        input_sum = sum(utxo.amount for utxo in self.inputs)
        output_sum = sum(utxo.amount for utxo in self.outputs)
        if input_sum != output_sum:
            raise ValueError("Input and output amounts do not match")
```

- **UTXO**: Represents unspent transaction outputs with `amount` and `recipient`.
- **Transaction**: Represents a transaction with inputs (UTXOs being spent) and outputs (new UTXOs created).

### Example Usage

```python
if __name__ == "__main__":
    # Create some UTXOs
    utxo1 = UTXO(amount=50.0, recipient="Alice")
    utxo2 = UTXO(amount=30.0, recipient="Bob")

    # Create a transaction
    transaction = Transaction(
        inputs=[utxo1],
        outputs=[UTXO(amount=30.0, recipient="Charlie"), UTXO(amount=20.0, recipient="Dave")]
    )

    # Validate the transaction
    try:
        transaction.validate_transaction()
        print("Transaction is valid")
    except ValueError as e:
        print(f"Transaction validation failed: {e}")
```

This example creates some UTXOs, constructs a transaction with inputs and outputs, and validates whether the transaction is valid based on the sum of inputs and outputs.

## Testing the API

You can test the API endpoints using **Postman** or any other API testing tool.

### Test `/mine_block`
- **Method**: `POST`
- **URL**: `http://127.0.0.1:8000/mine_block`

### Test `/new_transaction`
- **Method**: `POST`
- **URL**: `http://127.0.0.1:8000/new_transaction`
- **Body**:
```json
{
  "sender": "Alice",
  "receiver": "Bob",
  "amount": 50.0
}
```

### Test `/add_block`
- **Method**: `POST`
- **URL**: `http://127.0.0.1:8000/add_block`
- **Body**: Provide a block object to add to the blockchain.

### Test `/chain`
- **Method**: `GET`
- **URL**: `http://127.0.0.1:8000/chain`

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
