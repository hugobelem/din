from datetime import date
from din.transactions.core.entity import Transaction, TransactionType
from din.transactions.core.repository import TransactionRepository
from din.shared.core.clock import Clock
from .dto import TransactionUpdate


class AddTransaction:
    def __init__(self, repo: TransactionRepository, clock: Clock) -> None:
        self._repo = repo
        self._clock = clock

    def execute(
            self,
            type: TransactionType,
            due: date | None,
            description: str,
            amount: int,
            category: str,
        ) -> None:

        due_date = due or date.today()

        if type == TransactionType.EXPENSE:
            amount = -abs(amount)

        model = Transaction(
            created=self._clock.now(),
            type=type,
            due=due_date,
            description=description,
            amount=amount,
            category=category,
        )
        self._repo.add(model)


class ListTransactions:
    def __init__(self, repo: TransactionRepository) -> None:
        self._repo = repo

    def execute(self) -> list[Transaction]:
        return self._repo.all()
    

class GetTransaction:
    def __init__(self, repo: TransactionRepository) -> None:
        self._repo = repo

    def execute(self, id: str) -> Transaction | None:
        return self._repo.get(id)
    

class UpdateTransaction:
    def __init__(self, repo: TransactionRepository) -> None:
        self._repo = repo

    def execute(self, id: str, fields: TransactionUpdate) -> Transaction | None:
        transaction = self._repo.get(id)
        if not transaction:
            return
        
        if fields.amount is not None and transaction.type == TransactionType.EXPENSE:
            fields.amount = -abs(fields.amount)
    
        return self._repo.update(id, fields)


class DeleteTransaction:
    def __init__(self, repo: TransactionRepository) -> None:
        self._repo = repo

    def execute(self, id: str) -> None:
        return self._repo.delete(id)
    

class GetTotal:
    def __init__(self, repo: TransactionRepository) -> None:
        self._repo = repo

    def execute(self) -> int:
        ts = self._repo.all()

        return sum([t.amount for t in ts])


class GetTotalBalance:
    def __init__(self, repo: TransactionRepository) -> None:
        self._repo = repo

    def execute(self) -> int:
        ts = self._repo.all()

        today = date.today()
        up_to_today = [t for t in ts if t.due <= today]

        return sum([t.amount for t in up_to_today])

class GetTotalIncome:
    def __init__(self, repo: TransactionRepository) -> None:
        self._repo = repo

    def execute(self) -> int:
        ts = self._repo.all()

        return sum([t.amount for t in ts if t.type == TransactionType.INCOME])
    
class GetTotalExpense:
    def __init__(self, repo: TransactionRepository) -> None:
        self._repo = repo

    def execute(self) -> int:
        ts = self._repo.all()

        return sum([t.amount for t in ts if t.type == TransactionType.EXPENSE])
