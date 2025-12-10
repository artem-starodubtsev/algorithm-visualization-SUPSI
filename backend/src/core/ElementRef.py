from .Logger import Logger
from dataclasses import dataclass
from .LoggedStructureInterface import LoggedStructureInterface


@dataclass(frozen=True)
class ElementRef[T]:
    _ref: LoggedStructureInterface[T]
    _idx: int | tuple[int, int]
    _logger: Logger

    @property
    def value(self) -> T:
        return self._ref.get_value(self._idx)

    @staticmethod
    def unwrap(el: 'ElementRef[T] | T') -> T:
        return el.value if isinstance(el, ElementRef) else el

    def to_dict(self) -> dict:
        d = {
            'ref': self._ref.name(),
            'value': self.value,
        }
        if isinstance(self._idx, int):
            d['idx'] = self._idx
        else:
            d['y'], d['x'] = self._idx
        return d

    def swap(self, other: 'ElementRef[T]') -> None:
        if (self._ref is other._ref and self._idx == other._idx) or self is other:
            return
        a_ref, a_idx = self._ref, self._idx
        b_ref, b_idx = other._ref, other._idx
        a_val = self.value
        b_val = other.value
        # a_ref[a_idx] = b_val
        # b_ref[b_idx] = a_val
        a_ref.set_value(a_idx, b_val)
        b_ref.set_value(b_idx, a_val)
        self._logger.log(
            {
                'type': 'swap',
                'el': self.to_dict(),
                'other': other.to_dict(),
            }
        )

    def _cmp(self, other: 'ElementRef[T] | T', op: str) -> bool:
        from .LoggedValue import LoggedValue
        if isinstance(other, LoggedValue):
            return NotImplemented

        other_val = ElementRef.unwrap(other)
        res = self.value.__getattribute__({
                                              'gt': "__gt__",
                                              'ge': "__ge__",
                                              'lt': "__lt__",
                                              'le': "__le__",
                                              'eq': "__eq__",
                                              'ne': "__ne__"
                                          }[op])(other_val)
        self._logger.log(
            {
                'type': 'compare',
                'op': op,
                'el': self.to_dict(),
                'other': other.to_dict() if isinstance(other, ElementRef) else other,
                'result': res
            }
        )
        return res

    def __eq__(self, other: 'ElementRef[T] | T') -> bool:
        return self._cmp(other, 'eq')

    def __ne__(self, other: 'ElementRef[T] | T') -> bool:
        return self._cmp(other, 'ne')

    def __lt__(self, other: 'ElementRef[T] | T') -> bool:
        return self._cmp(other, 'lt')

    def __le__(self, other: 'ElementRef[T] | T') -> bool:
        return self._cmp(other, 'le')

    def __gt__(self, other: 'ElementRef[T] | T') -> bool:
        return self._cmp(other, 'gt')

    def __ge__(self, other: 'ElementRef[T] | T') -> bool:
        return self._cmp(other, 'ge')

    def __add__(self, other: 'ElementRef[T] | T') -> T:
        return self.value + ElementRef.unwrap(other)

    def __radd__(self, other: 'ElementRef[T] | T') -> T:
        return ElementRef.unwrap(other) + self.value

    def __sub__(self, other: 'ElementRef[T] | T') -> T:
        return self.value - ElementRef.unwrap(other)

    def __rsub__(self, other: 'ElementRef[T] | T') -> T:
        return ElementRef.unwrap(other) - self.value

    def __mul__(self, other: 'ElementRef[T] | T') -> T:
        return self.value * ElementRef.unwrap(other)

    def __rmul__(self, other: 'ElementRef[T] | T') -> T:
        return ElementRef.unwrap(other) * self.value

    def __truediv__(self, other: 'ElementRef[T] | T') -> T:
        return self.value / ElementRef.unwrap(other)

    def __rtruediv__(self, other: 'ElementRef[T] | T') -> T:
        return ElementRef.unwrap(other) / self.value

    def __floordiv__(self, other: 'ElementRef[T] | T') -> T:
        return self.value // ElementRef.unwrap(other)

    def __rfloordiv__(self, other: 'ElementRef[T] | T') -> T:
        return ElementRef.unwrap(other) // self.value