from abc import ABC, abstractmethod
from din.transactions.app.dto import TransactionUpdate
from .entity import Transaction


class TransactionRepository(ABC):
    @abstractmethod
    def add(self, tx: Transaction) -> None:
        ...

    @abstractmethod
    def all(self) -> list[Transaction]:
        ...

    @abstractmethod
    def get(self, id: str) -> Transaction | None:
        ...

    @abstractmethod
    def update(self, id: str, fields: TransactionUpdate) -> Transaction | None:
        ...

    @abstractmethod
    def delete(self, id: str) -> None:
        ...
