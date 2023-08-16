from dataclasses import field
from typing import Any, TypeVar
from datetime import date

EntityType = TypeVar("EntityType", bound="Entity")


class Entity:
    id: int = field(init=False)
    create_at: date
    uptade_at: date

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, type(self)):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash(self.id)


class AggregateRoot(Entity):
    """
    An entry point of aggregate.
    """
    pass
