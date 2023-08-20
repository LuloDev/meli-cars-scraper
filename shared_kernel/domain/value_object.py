from enum import Enum, EnumMeta
from typing import Any, TypeVar

from shared_kernel.domain.exception import ValueObjectEnumError

ValueObjectType = TypeVar("ValueObjectType", bound="ValueObject")


# pylint: disable=R0903
class ValueObject:
    """This class represent valuObject."""

    def __composite_values__(self):
        return self.value  # pylint: disable=E1101

    @classmethod
    def from_value(cls, value: Any) -> ValueObjectType:
        if isinstance(cls, EnumMeta):
            for item in cls:  # pylint: disable=E1133
                if item.value == value:
                    return item
            raise ValueObjectEnumError

        instance = cls(value=value)
        return instance


class TypeFuel(ValueObject, str, Enum):
    """This class represent Type Fuels"""
    GASOLINE = "GASOLINE"
    DIESEL = "DIESEL"
    GAS = "GAS"
    ELECTRIC = "ELECTRIC"


class TypeTransmission(ValueObject, str, Enum):
    """This class represent Type ransmission"""
    MECANIC = "MECANIC"
    AUTOMATIC = "AUTOMATIC"
