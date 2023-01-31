from __future__ import annotations
from itertools import chain




class Object:
    def __init__(self, *args: Object, **kwargs) -> None:
        self.__dict__.update(
            chain.from_iterable((vars(arg).items() for arg in args if arg)),
            **kwargs
        )
        
    def __repr__(self) -> str:
        quote = "'"
        return  f"({', '.join(key.strip(quote) + '=' + value.__repr__() for key, value in self.__dict__.items())})"



