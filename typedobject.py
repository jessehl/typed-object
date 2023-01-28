from __future__ import annotations
from typing import Callable, Dict, Any, Protocol
from itertools import chain


class _Protocol(Protocol):
    __dict__: Dict[str, Any]

class Object:

    def __init__(self, *args: _Protocol, **kwargs):
        for k,v in dict(chain(
            chain.from_iterable((arg.__dict__.items() for arg in args if arg)),
            kwargs.items()
        )).items():
            self.__setattr__(k,v)
            
    def __dir__(self):
        return list(self.__dict__.keys())

    def __repr__(self) -> str:
        quote = "'"
        return  f" ({', '.join(key.strip(quote) + '=' + value.__repr__() for key, value in self.__dict__.items())}) "



class Bar(_Protocol):
    a: int
    b: Callable[[], None]
    c: str


def type_check(a: Bar):
    g = Object(a)
    g
    return Object(g).a + 100

a = type_check(Object(a = '3'))





    