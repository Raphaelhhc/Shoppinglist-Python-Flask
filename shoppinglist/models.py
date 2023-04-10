from dataclasses import dataclass, field

@dataclass
class Item:
    _id: str
    name: str
    cost: int
    priority: str
    memo: str = None
    requirement: list[str] = field(default_factory=list)
    choices: list[str] = field(default_factory=list)
    bought: bool = False

@dataclass
class Choice:
    _id: str
    name: str
    price: int
    brand: str = None
    where: str = None
    address: str = None

@dataclass
class User:
    _id: str
    email: str
    password: str
    items: list[str] = field(default_factory=list)