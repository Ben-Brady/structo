import typing as t
import annotationlib
from .literal import Literal
from ..serializer import Serializer, Format
from ..serialise import read_serializable, write_serializable


class UnionSerializer[T](Serializer[T]):
    format: t.TypeVar
    _tdescriminator: Format
    _tvalues: list[Format]

    def __init__(self, union: t.TypeVar, args: t.TypeVarTuple) -> None:
        if args.evaluate_default is None:
            raise ValueError("TODO")

        evaluate = args.evaluate_default(annotationlib.Format.VALUE)
        print(evaluate)
        self.format = union
        assert isinstance(
            union, t.Union
        ), "second argument must be a union e.g. Union[A | B | C, ...]"
        (tvalues,) = list(t.get_args(tvalues))

        self._tvalues = list(t.get_args(tvalues))
        self._tdescriminator = tdescrim

    def write(self, buf, format, value):
        index = self._tvalues.index(type(value))
        write_serializable(buf, self._tdescriminator, index)
        write_serializable(buf, self._tdescriminator, value)

    def read(self, buf, format):
        descriminator = read_serializable(buf, self._tdescriminator)
        assert descriminator >= 0, "Descriminator is outside allowed values"
        assert descriminator < len(
            self._tvalues
        ), "Descriminator is outside allowed values"

        value_type = self._tvalues[descriminator]
        value = read_serializable(buf, value_type)
        return value


type UnionVariant[Prefix, Value] = tuple[t.Never]
type Union[Value, *Args] = t.Annotated[Value, UnionSerializer(Value, Args)]
"""
**Union[TType: uint, TValue: Union]**

A union of possible values

> TType: The storage type for the descriminator
> Value(Union): The literal value

**Example**: `Union[uint8, InfoChunk | DataChunk]`

---
"""
