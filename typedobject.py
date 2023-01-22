from __future__ import annotations
from typing import Optional, cast
from itertools import chain

class Object:
    
    def __init__(self, *args: Optional[Object], **kwargs): 
        for k,v in chain(
            chain.from_iterable((arg.__dict__.items() for arg in args if arg)),
            kwargs.items()
        ):
            self.__setattr__(k,v) 

    def __repr__(self) -> str:
        values = (key.strip("'") + ' = ' + value.__repr__() for key, value in self.__dict__.items())
        return  f"({', '.join(values)})"


g = Object(a = 1, b = '2')

g.b + '3'
g.a + 1
g.c + '2'

