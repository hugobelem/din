from sqlalchemy.orm import Session
from ..core.entity import Transaction
from .model import TransactionModel
from .repository import TransactionRepository
from ..utils.mappers import to_model, to_entity


class AlchemyTransactionRepository(TransactionRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, tx: Transaction):
        self.session.add(to_model(tx))
        self.session.commit()

    def list(self) -> list[Transaction]:
        rows = self.session.query(TransactionModel).all()
        return [to_entity(row) for row in rows]
