# 2. Implement a UTXO (Unspent Transaction Output) model using Pydantic in Python.

from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import uuid4

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

# Example usage
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
