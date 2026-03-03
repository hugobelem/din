from dataclasses import dataclass
from datetime import datetime

from typing import Literal

@dataclass
class Transaction:
    id: str | None
    description: str
    amount: int
    category: str
    date: datetime
    type: Literal[1, 2, 3]
