from abc import ABC, abstractmethod
from .entity import Transaction
from ..app.dto import TransactionUpdate


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
