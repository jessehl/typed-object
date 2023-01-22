from __future__ import annotations
from typing import Callable
from mypy.nodes import Var, SymbolTableNode, MDEF
from mypy.types import Instance
from mypy.types import Type, Instance
from mypy.plugin import Plugin, FunctionContext
from itertools import chain

class TypedObjectPlugin(Plugin):
    """ A plugin to make MyPy understand TypedObjects."""
    def get_function_hook(self, fullname: str) -> Callable[[FunctionContext], Type] | None:
        if fullname == 'typedobject.Object':
            return add_input_args_to_class
        return None


def add_input_args_to_class(ctx: FunctionContext):
    assert isinstance(ctx.default_return_type, Instance)

    # Fetch argument name-type pairs (both args and kwargs).
    input_args = chain(zip(chain.from_iterable(ctx.arg_names), chain.from_iterable(ctx.arg_types)))

    # TODO: how is it possible that nested object assignment (i.e. 'a = Object(a = 1); b = Object(a)') is typed properly?
    # The types of 'a' are never assigned to the created object, it seems. 

    # TODO: add support for inferring return types when args contains a Union of Objects.  

    # args = ctx.arg_types[0]
    # if args:

     #   items = args[0].type.names.items()
      #  for key, item in items:
       #     print(key)
        #    print(item)
            
    info = ctx.default_return_type.type
    def add_field(name: str, type: Type):
        var =               Var(name, type)
        var.info =          info
        var._fullname =     f"{info.fullname}.{var.name}"
        info.names[name] =  SymbolTableNode(MDEF, var)
        return (type, name)

    test = [add_field(str(name), type) for name, type in input_args]
    print("here")
    print(test)

    return Instance(
        typ =       ctx.default_return_type.type, 
        args =      [],
        line =      ctx.default_return_type.line,
        column =    ctx.default_return_type.column
    )


def plugin(version: str):
    return TypedObjectPlugin