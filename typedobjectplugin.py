from __future__ import annotations
from typing import Callable, Dict, Tuple
from mypy.nodes import Var, SymbolTableNode, MDEF, ClassDef, Block, TypeInfo, SymbolTable
from mypy.types import Instance, Type
from mypy.plugin import Plugin, FunctionContext
from itertools import chain

class TypedObjectPlugin(Plugin):
    """ A plugin to make MyPy understand TypedObjects."""
    def get_function_hook(self, fullname: str) -> Callable[[FunctionContext], Type] | None:
        if fullname.startswith('typedobject.Object'):
            return new_typedobject
        return None

def create_type_info(type_info: TypeInfo, attributes: Dict[str, Type]) -> TypeInfo:
    """ Returns the TypeInfo of a new typedobject class. """
    new_class_def = ClassDef('Object' + str(attributes), defs = Block([]))
    new_class_def.fullname = 'Object' + str(attributes)

    info = TypeInfo(SymbolTable(), new_class_def, 'typedobject')
    info.bases = [Instance(type_info, [])]
    info.mro = [info, type_info]

    def get_symbol(field: Tuple[str, Type]):
        var =               Var(*field)
        var.info =          info
        var._fullname =     f"{'Object'}.{var.name}"
        return (var.name, SymbolTableNode(MDEF, var))
    info.names.update(map(get_symbol, attributes.items()))

    new_class_def.info = info
    return info 

def new_typedobject(ctx: FunctionContext):
    """ Returns an Instance of a new typedobject.Object. """
    assert isinstance(ctx.default_return_type, Instance)

    # Get and flatten attributes of input Object(s).
    objects = (_ for _ in ctx.arg_types[0] if isinstance(_, Instance))
    names_of_objects = chain.from_iterable(_.type.names.items() for _ in objects)
    attributes_of_objects = ((arg, node.type) for arg, node in names_of_objects if not node.type is None)

    # Get types of kwargs.
    kwargs = ((name, type) for name, type in zip(ctx.arg_names[1:][0], ctx.arg_types[1:][0]) if name)

    return Instance(
        create_type_info(
            type_info   = ctx.api.named_generic_type('typedobject.Object', []).type, 
            attributes  = dict(chain(attributes_of_objects, kwargs))
        ),
        []
    )

# TODO: add support for inferring return types when args contains a Union of Objects.  
# TODO: add automatically derived return types for functions that create an Object. 


def plugin(version: str):
    return TypedObjectPlugin