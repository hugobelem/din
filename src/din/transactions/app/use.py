from typing import Literal
from datetime import datetime
from zoneinfo import ZoneInfo
from ..core.entity import Transaction
from ..infra.repository import TransactionRepository


class AddTransaction:
    def __init__(self, repo: TransactionRepository) -> None:
        self.repo = repo

    def execute(
            self,
            description: str,
            amount: int,
            category: str,
            type: Literal[1, 2, 3]
        ):
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
        return self.repo.list()
