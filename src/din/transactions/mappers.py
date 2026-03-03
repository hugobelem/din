from .entity import Transaction
from .model import TransactionModel


def to_model(tx: Transaction) -> TransactionModel:
    return TransactionModel(
        description=tx.description,
        amount=tx.amount,
        category=tx.category,
        date=tx.date,
        type=tx.type,
    )

def to_entity(model: TransactionModel) -> Transaction:
    return Transaction(
        id=model.id,
        description=model.description,
        amount=model.amount,
        category=model.category,
        date=model.date,
        type=model.type,
    )
