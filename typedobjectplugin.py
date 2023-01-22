from __future__ import annotations
from typing_extensions import Final, Literal
from typing import Callable, TypeVar
import typing as ty
from mypy.nodes import (
    Var, Argument, ARG_POS, FuncDef, PassStmt, Block,
    SymbolTableNode, MDEF
)
from mypy.nodes import NameExpr
from mypy.types import UnionType, NoneType, Instance, ExtraAttrs
from mypy.types import NoneTyp, Type, CallableType, get_proper_type, Instance, UnionType
from mypy.typevars import fill_typevars
from mypy.semanal import set_callable_name
from mypy.plugin import Plugin, ClassDefContext, FunctionContext
from mypy.plugins.attrs import attr_class_maker_callback
from mypy.plugins.common import add_method
from mypy.plugins.common import (
    _get_decorator_bool_argument,
    add_attribute_to_class,
    add_method,
    deserialize_and_fixup_type,
)
from mypy.nodes import (
    ClassDef, Block, TypeInfo, SymbolTable, SymbolTableNode, MDEF, GDEF, Var
)


from typing import NewType

T = TypeVar('T')


class MyPlugin(Plugin):
    """A plugin to make MyPy understand TypedObjects."""
    def get_function_hook(self, fullname: str) -> Callable[[FunctionContext], Type] | None:
        print('fullname',fullname)
        if fullname == 'typedobject.Object':
            return get_shizzle


def get_shizzle(ctx: FunctionContext):
    try:
        types = ctx.arg_types[1:][0]
        names = ctx.arg_names[1:][0]
        info = ctx.default_return_type.type
        print(types, names, ctx.default_return_type, info)


        def add_field(
            var: Var, is_initialized_in_class: bool = False, is_property: bool = False
        ) -> None:
            var.info = info
            var.is_initialized_in_class = is_initialized_in_class
            var.is_property = is_property
            var._fullname = f"{info.fullname}.{var.name}"
            info.names[var.name] = SymbolTableNode(MDEF, var)

        fields = [Var(name, typ) for name, typ in zip(names, types)]
        for var in fields:
            add_field(var, is_property=True)
    
        my_instance = Instance(ctx.default_return_type.type, types,
                    line=ctx.default_return_type.line,
                    column=ctx.default_return_type.column)
 
        return my_instance




    except Exception as e:
        print(e)



def plugin(version: str):
    return MyPlugin
