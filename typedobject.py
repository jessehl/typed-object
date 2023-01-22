from __future__ import annotations
from typing import Optional, Union, Dict, Any
from itertools import chain

class Object:
    
    def __init__(self, *args: Optional[Object], **kwargs):
        for k,v in dict(chain(
            chain.from_iterable((arg.__dict__.items() for arg in args if arg)),
            kwargs.items()
        )).items():
            self.__setattr__(k,v) 

    def __repr__(self) -> str:
        quote = "'"
        return  f" ({', '.join(key.strip(quote) + '=' + value.__repr__() for key, value in self.__dict__.items())}) "

def type_check() -> None:
    a = Object(a = 1)
    
    Object(a).a + 100 