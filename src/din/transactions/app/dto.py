from dataclasses import dataclass
from typing import Optional

@dataclass
class TransactionUpdate:
    amount: Optional[int] = None
    category: Optional[str] = None
    description: Optional[str] = None
    type: Optional[int] = None
