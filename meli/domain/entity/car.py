from dataclasses import dataclass
from datetime import date

from shared_kernel.domain.entity import Entity
from shared_kernel.domain.value_object import TypeFuel, TypeTransmission


@dataclass(eq=False, slots=True)
class Car(Entity):
    title: str
    year: int
    color: str
    engine: float
    brand: str
    model: str
    version: str
    type_fueld: TypeFuel
    transmission: TypeTransmission
    kilometers: int
    date_published: date
    price: float
    url: str
