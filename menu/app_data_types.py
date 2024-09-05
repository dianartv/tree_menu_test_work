from dataclasses import dataclass, field
from typing import Any


@dataclass
class Item:
    id: int
    title: str
    url: str
    named_url: str
    parent_id: int = field(default_factory=int)
    active: bool = field(default=False)
    children: list[int] = field(default_factory=list)
    parent: Any = field(default=None)


@dataclass
class MenuTree:
    html: str
