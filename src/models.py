from dataclasses import dataclass

@dataclass
class User:
    id: str
    name: str
    state: str = 'initial'

@dataclass
class Item:
    id: int
    name: str
    category: str
    price: float
    description: str