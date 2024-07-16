from dataclasses import dataclass, field
from typing import Optional

@dataclass
class User:
    id: str
    name: str
    state: str = 'initial'

@dataclass
class Item:
    name: str
    category: str
    price: float
    description: str
    id: Optional[int] = field(default=None)