from abc import ABC, abstractmethod
from .entity import Transaction


class TransactionRepository(ABC):
    @abstractmethod
    def add(self, tx: Transaction) -> None:
        ...

    @abstractmethod
    def list(self) -> list[Transaction]:
        ...
