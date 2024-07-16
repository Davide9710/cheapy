from dataclasses import dataclass, field
from typing import Optional

@dataclass
class User:
    id: str
    name: str
    state: str = 'initial'

@dataclass
class Item:
    id: Optional[int] = field(default=None)
    name: str
    category: str
    price: float
    description: str