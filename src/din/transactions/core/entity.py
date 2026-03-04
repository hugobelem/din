import ulid
from datetime import datetime, date
from dataclasses import dataclass, field
from .objects import TransactionType


def generate_ulid() -> str:
    return ulid.new().str


@dataclass
class Transaction:
    created: datetime
    type: TransactionType
    due: date
    description: str
    amount: int
    category: str
    id: str = field(default_factory=generate_ulid)
