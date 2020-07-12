from abc import abstractmethod
from typing import TYPE_CHECKING, Callable, NoReturn, Type, TypeVar

from returns.interfaces.specific import io, result
from returns.primitives.hkt import KindN

if TYPE_CHECKING:
    from returns.io import IO, IOResult  # noqa: WPS433

_FirstType = TypeVar('_FirstType')
_SecondType = TypeVar('_SecondType')
_ThirdType = TypeVar('_ThirdType')
_UpdatedType = TypeVar('_UpdatedType')
_IOResultBasedType = TypeVar('_IOResultBasedType', bound='IOResultBasedN')


class IOResultBasedN(
    io.IOBasedN[_FirstType, _SecondType, _ThirdType],
    result.ResultBasedN[_FirstType, _SecondType, _ThirdType],
):
    """
    Allows to create unit containers from raw values and to apply wrapped funcs.

    See also:
        https://en.wikipedia.org/wiki/IOResultBased_functor
        http://learnyouahaskell.com/functors-IOResultBased-functors-and-monoids

    """

    @abstractmethod
    def bind_ioresult(
        self: _IOResultBasedType,
        function: Callable[[_FirstType], 'IOResult[_UpdatedType, _SecondType]'],
    ) -> KindN[_IOResultBasedType, _UpdatedType, _SecondType, _ThirdType]:
        """Allows to apply a wrapped function over a container."""

    @classmethod
    @abstractmethod
    def from_ioresult(
        cls: Type[_IOResultBasedType],  # noqa: N805
        inner_value: 'IOResult[_FirstType, _SecondType]',
    ) -> KindN[_IOResultBasedType, _FirstType, _SecondType, _ThirdType]:
        """Unit method to create new containers from any raw value."""

    @classmethod
    @abstractmethod
    def from_failed_io(
        cls: Type[_IOResultBasedType],  # noqa: N805
        inner_value: 'IO[_SecondType]',
    ) -> KindN[_IOResultBasedType, _FirstType, _SecondType, _ThirdType]:
        """Unit method to create new containers from any raw value."""


#: Type alias for kinds with one type argument.
IOResultBased1 = IOResultBasedN[_FirstType, NoReturn, NoReturn]

#: Type alias for kinds with two type arguments.
IOResultBased2 = IOResultBasedN[_FirstType, _SecondType, NoReturn]

#: Type alias for kinds with three type arguments.
IOResultBased3 = IOResultBasedN[_FirstType, _SecondType, _ThirdType]
