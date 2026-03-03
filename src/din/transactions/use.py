from datetime import date
from .entity import Transaction
from .repository import TransactionRepository


class AddTransaction:
    def __init__(self, repo: TransactionRepository) -> None:
        self.repo = repo

    def execute(self, description: str, amount: float, category: str, type: str):
        model = Transaction(
            id=1,
            description=description,
            amount=amount,
            category=category,
            date=date.today(),
            type=type
        )
        self.repo.add(model)


class ListTransactions:
    def __init__(self, repo: TransactionRepository) -> None:
        self.repo = repo

    def execute(self) -> list[Transaction]:
        return self.repo.list()
