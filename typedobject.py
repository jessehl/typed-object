from __future__ import annotations
from typing import Optional
from itertools import chain

class Object:
    
    def __init__(self, *args: Optional[Object], **kwargs):
        attrs_to_set = {k:v for k,v in chain(
            chain.from_iterable((arg.__dict__.items() for arg in args if arg)),
            kwargs.items()
        )}
        for k,v in attrs_to_set.items():
            self.__setattr__(k,v) 

    def __repr__(self) -> str:
        values = (key.strip("'") + ' = ' + value.__repr__() for key, value in self.__dict__.items())
        return  f"({', '.join(values)})"


g = Object(Object(a = 1), None, a = '1', b = 2)





