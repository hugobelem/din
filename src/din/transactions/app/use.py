from typing import Literal
from zoneinfo import ZoneInfo
from datetime import datetime, date
from .dto import TransactionUpdate
from ..core.entity import Transaction
from ..core.repository import TransactionRepository


class AddTransaction:
    def __init__(self, repo: TransactionRepository) -> None:
        self.repo = repo

    def execute(
            self,
            type: Literal[1, 2, 3],
            due: str | None,
            description: str,
            amount: int,
            category: str,
        ) -> None:

        due_date = date.today()
        if due:
            due_date = date.strptime(due, '%Y-%m-%d')

        if type == 2:
            amount = -abs(amount)

        model = Transaction(
            id=None,
            created=datetime.now(ZoneInfo('America/Recife')),
            type=type,
            due=due_date,
            description=description,
            amount=amount,
            category=category,
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
        if fields.due:
            setattr(fields, 'due', date.strptime(fields.due, '%Y-%m-%d'))

        return self.repo.update(id, fields)


class DeleteTransaction:
    def __init__(self, repo: TransactionRepository) -> None:
        self.repo = repo

    def execute(self, id: str) -> None:
        return self.repo.delete(id)
    

class GetTotal:
    def __init__(self, repo: TransactionRepository) -> None:
        self.repo = repo

    def execute(self) -> int:
        ts = self.repo.all()

        return sum([t.amount for t in ts])


class GetTotalBalance:
    def __init__(self, repo: TransactionRepository) -> None:
        self.repo = repo

    def execute(self) -> int:
        ts = self.repo.all()

        today = date.today()
        up_to_today = [t for t in ts if t.due <= today]

        return sum([t.amount for t in up_to_today])

class GetTotalIncome:
    def __init__(self, repo: TransactionRepository) -> None:
        self.repo = repo

    def execute(self) -> int:
        ts = self.repo.all()

        return sum([t.amount for t in ts if t.type == 1])
    
class GetTotalExpense:
    def __init__(self, repo: TransactionRepository) -> None:
        self.repo = repo

    def execute(self) -> int:
        ts = self.repo.all()

        return sum([t.amount for t in ts if t.type == 2])
