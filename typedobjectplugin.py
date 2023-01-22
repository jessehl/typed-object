from __future__ import annotations
from typing import Callable, TypeVar
from mypy.nodes import (
    Var, SymbolTableNode, MDEF
)

from mypy.types import Instance, NoneType
from mypy.types import Type, Instance
from mypy.plugin import Plugin, FunctionContext
from itertools import chain
from typedobject import Object


class Bar:
    def visit_instance(self, ins):
        print(ins)

class TypedObjectPlugin(Plugin):
    """A plugin to make MyPy understand TypedObjects."""
    def get_function_hook(self, fullname: str) -> Callable[[FunctionContext], Type] | None:
        if fullname == 'typedobject.Object':
            return add_input_args_to_class_hook
        return None

def add_input_args_to_class_hook(ctx: FunctionContext):
    assert isinstance(ctx.default_return_type, Instance)

    # Fetch argument name-type pairs (both args and kwargs).
    input_args = chain(zip(chain.from_iterable(ctx.arg_names), chain.from_iterable(ctx.arg_types)))
    names_types = list((name, type) for name, type in input_args if not isinstance(type, NoneType))

    print("here")
    # TODO: Get all attributes from 'args' (i.e. from other TypedObjects).
    try:
        bar = [(name, Instance(type, []).type.slots) for name, type in names_types]
        print('bar', bar)
    except Exception as e:
        print(e)

    print('names_types', names_types)

    info = ctx.default_return_type.type 

    def add_field(
        var: Var, is_initialized_in_class: bool = False, is_property: bool = False
    ) -> None:
        var.info = info
        var.is_initialized_in_class = is_initialized_in_class
        var.is_property = is_property
        var._fullname = f"{info.fullname}.{var.name}"
        info.names[var.name] = SymbolTableNode(MDEF, var)

    fields = [Var(str(name), typ) for name, typ in names_types]
    for var in fields:
        add_field(var, True, True)

    my_instance = Instance(ctx.default_return_type.type, [],
                line=ctx.default_return_type.line,
                column=ctx.default_return_type.column)

    return my_instance






def plugin(version: str):
    return TypedObjectPlugin
