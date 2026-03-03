from sqlalchemy.orm import Session
from .model import TransactionModel
from ..core.entity import Transaction
from ..app.dto import TransactionUpdate
from ..core.repository import TransactionRepository
from ..utils.mappers import to_model, to_entity, to_dict


class AlchemyTransactionRepository(TransactionRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, tx: Transaction) -> None:
        self.session.add(to_model(tx))
        self.session.commit()

    def all(self) -> list[Transaction]:
        rows = self.session.query(TransactionModel).all()
        return [to_entity(row) for row in rows]
    
    def get(self, id: str) -> Transaction | None:
        obj = self.session.get(TransactionModel, id)

        if not obj:
            return None

        return to_entity(obj)
        
    def update(self, id: str, fields: TransactionUpdate) -> Transaction | None:
        obj = self.session.get(TransactionModel, id)

        if not obj:
            return None
        
        for k, v in to_dict(fields).items():
            setattr(obj, k, v)

        self.session.commit()
        self.session.refresh(obj)

        return to_entity(obj)

    
    def delete(self, id: str) -> None:
        obj = self.session.get(TransactionModel, id)

        if not obj:
            return None

        self.session.delete(obj)
        self.session.commit()
