from dataclasses import dataclass

@dataclass
class TransactionUpdate:
    type: int | None = None
    due: str | None = None
    description: str | None = None
    amount: int | None = None
    category: str | None = None
