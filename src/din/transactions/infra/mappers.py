from typing import Any
from dataclasses import asdict
from din.transactions.core.entity import Transaction
from din.transactions.app.dto import TransactionUpdate
from .model import TransactionModel


def to_model(tx: Transaction) -> TransactionModel:
    return TransactionModel(
        id=tx.id,
        created=tx.created,
        type=tx.type,
        due=tx.due,
        description=tx.description,
        amount=tx.amount,
        category=tx.category,
    )

def to_entity(model: TransactionModel) -> Transaction:
    return Transaction(
        id=model.id,
        created=model.created,
        type=model.type,
        due=model.due,
        description=model.description,
        amount=model.amount,
        category=model.category,
    )

def to_dict(obj: TransactionUpdate) -> dict[str, Any]:
    return {k: v for k, v in asdict(obj).items() if v is not None}
