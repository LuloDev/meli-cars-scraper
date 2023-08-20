class ValueObjectEnumError(Exception):
    """This exception is raised  when a  valueobject enum  has provided incorrect data."""

    def __str__(self):
        return "Value Object got invalid value."


class BaseMsgException(Exception):
    """This exception is raised to base exception."""
    message: str

    def __str__(self):
        return self.message
