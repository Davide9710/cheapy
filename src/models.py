from dataclasses import dataclass

@dataclass
class User:
    id: str
    name: str
    state: str = 'initial'