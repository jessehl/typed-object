from __future__ import annotations
from typing import Callable, Type
from mypy.nodes import Var, SymbolTableNode, MDEF
from mypy.types import Instance
from mypy.types import Type
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

    # Fetch args types.
    objects = (_ for _ in ctx.arg_types[0] if isinstance(_, Instance))
    args_of_objects = chain.from_iterable(_.type.names.items() for _ in objects)
    args = ((arg, node.type) for arg, node in args_of_objects if not node.type is None)

    # Fetch kwargs types. 
    kwargs = zip(chain.from_iterable(ctx.arg_names[1:]), chain.from_iterable(ctx.arg_types[1:]))

    # Dedupe fields. 
    all_fields = dict(chain(args, kwargs))

    # TODO: add support for inferring return types when args contains a Union of Objects.  
    # TODO: Object() now only has one Symbol Table entry, so we're overwriting this entry when modifing the return type. 
    info = ctx.default_return_type.type

    print(info)


    def add_field(name: str, type: Type):
        var =               Var(name, type)
        var.info =          info
        var._fullname =     f"{info.fullname}.{var.name}"
        info.names[name] =  SymbolTableNode(MDEF, var)
        return (type, name)
    
    [add_field(str(name), type) for name, type in all_fields.items()]
    
    return Instance(
        typ =       ctx.default_return_type.type,
        args =      list(all_fields.values()),
        line =      ctx.default_return_type.line,
        column =    ctx.default_return_type.column
    )


def plugin(version: str):
    return TypedObjectPlugin