from dataclasses import dataclass


@dataclass(eq=False, slots=False, init=False)
class MeliItem():
    url: str
    title: str
    year: int | None = None
    color: str | None = None
    engine: float | None = None
    brand: str | None = None
    model: str | None = None
    version: str | None = None
    typeFueld: str | None = None
    transmission: str | None = None
    kilometers: int | None = None
    date_published: str | None = None
    price: float | None = None
