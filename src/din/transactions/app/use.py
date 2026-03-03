from typing import Literal
from zoneinfo import ZoneInfo
from datetime import datetime
from .dto import TransactionUpdate
from ..core.entity import Transaction
from ..core.repository import TransactionRepository


class AddTransaction:
    def __init__(self, repo: TransactionRepository) -> None:
        self.repo = repo

    def execute(
            self,
            description: str,
            amount: int,
            category: str,
            type: Literal[1, 2, 3]
        ) -> None:
        model = Transaction(
            id=None,
            description=description,
            amount=amount,
            category=category,
            date=datetime.now(ZoneInfo('America/Recife')),
            type=type
        )
        self.repo.add(model)


class ListTransactions:
    def __init__(self, repo: TransactionRepository) -> None:
        self.repo = repo

    def execute(self) -> list[Transaction]:
        return self.repo.all()
    

class GetTransaction:
    def __init__(self, repo: TransactionRepository) -> None:
        self.repo = repo

    def execute(self, id: str) -> Transaction | None:
        return self.repo.get(id)
    

class UpdateTransaction:
    def __init__(self, repo: TransactionRepository) -> None:
        self.repo = repo

    def execute(self, id: str, fields: TransactionUpdate) -> Transaction | None:
        return self.repo.update(id, fields)


class DeleteTransaction:
    def __init__(self, repo: TransactionRepository) -> None:
        self.repo = repo

    def execute(self, id: str) -> None:
        return self.repo.delete(id)
