from enum import Enum, EnumMeta
from typing import Any, TypeVar

from shared_kernel.domain.exception import ValueObjectEnumError

ValueObjectType = TypeVar("ValueObjectType", bound="ValueObject")


class ValueObject:
    def __composite_values__(self):
        return self.value,

    @classmethod
    def from_value(cls, value: Any) -> ValueObjectType:
        if isinstance(cls, EnumMeta):
            for item in cls:
                if item.value == value:
                    return item
            raise ValueObjectEnumError

        instance = cls(value=value)
        return instance


class TypeFuel(ValueObject, str, Enum):
    GASOLINE = "GASOLINE"
    DIESEL = "DIESEL"
    GAS = "GAS"
    ELECTRIC = "ELECTRIC"


class TypeTransmission(ValueObject, str, Enum):
    MECANIC = "MECANIC"
    AUTOMATIC = "AUTOMATIC"
