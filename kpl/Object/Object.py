from dataclasses import dataclass, field
import kpl.Ast.Ast as Ast
from typing import Callable

ObjectType = str
BUILTIN_OBJ = "BUILTIN"
INTEGER_OBJ = "INTEGER"
BOOLEAN_OBJ = "BOOLEAN"
GUTIRI_OBJ = "GUTIRI"
RIKIA_VALUE_OBJ = "RIKIA_VALUE"
CHOKIA_VALUE_OBJ = "CHOKIA_VALUE"
ERROR_OBJ = "ERROR"
FUNCTION_OBJ = "FUNCTION"
ARRAY_OBJ = "ARRAY"
STRING_OBJ = "STRING"
HASH_OBJ = "HASH"

# There are three types of data items in the language str, int and bools
# A reference to an invalid data type will return Gutiri


@dataclass
class Object:
    def Type(self) -> ObjectType:
        raise NotImplementedError

    def Inspect(self) -> str:
        raise NotImplementedError


@dataclass
class Integer(Object):
    Value: int

    def Inspect(self):

        return str(self.Value)

    def Type(self):
        return INTEGER_OBJ

    def hash_key(self):
        return HashKey(self.Type(), self.Value)


@dataclass
class Boolean(Object):
    Value: bool

    def Inspect(self):
        return "Ma" if self.Value else "Maheni"

    def Type(self):
        return BOOLEAN_OBJ

    def hash_key(self):
        return HashKey(self.Type(), 1 if self.Value else 0)


@dataclass
class Gutiri(Object):
    def Type(self):
        return GUTIRI_OBJ

    def Inspect(self):
        return "GUTIRI"


@dataclass
class ChokiaValue(Object):
    Value: Object

    def Type(self):
        return CHOKIA_VALUE_OBJ

    def Inspect(self):
        return self.Value.Inspect()


@dataclass
class Error(Object):
    Message: str

    def Type(self):
        return ERROR_OBJ

    def Inspect(self):
        return "🖕🏿: " + self.Message


@dataclass
class Environment:
    store: dict[str, Object] = field(default_factory=dict)
    outer: "Environment | None" = None

    def get(self, name):
        obj = self.store.get(name)

        if obj is None and self.outer is not None:
            return self.outer.get(name)

        return obj

    def set(self, name, value):
        self.store[name] = value
        return value


def new_environment():
    return Environment(store={}, outer=None)


def new_enclosed_environment(outer):
    env = new_environment()
    env.outer = outer
    return env


@dataclass
class Function(Object):
    Parameters: list[Ast.Identifier] = field(default_factory=list)
    Body: Ast.BlockStatement | None = None
    Env: Environment | None = None

    def Type(self):
        return FUNCTION_OBJ

    def Inspect(self):
        params = ", ".join(str(param) for param in self.Parameters)

        return f"fn({params}) {{\n{self.Body}\n}}"


@dataclass
class String(Object):
    Value: str

    def Type(self):
        return STRING_OBJ

    def Inspect(self):
        return self.Value

    def hash_key(self):
        return HashKey(
            self.Type(),
            hash(self.Value),
        )


# A builtin function receives zero or more Objects and returns an Object.
BuiltinFunction = Callable[..., Object]


@dataclass
class Builtin(Object):
    Fn: BuiltinFunction

    def Type(self):
        return BUILTIN_OBJ

    def Inspect(self):
        return "builtin function"


@dataclass
class Array(Object):
    Elements: list[Object] = field(default_factory=list)

    def Type(self):
        return ARRAY_OBJ

    def Inspect(self):
        elements = [element.Inspect() for element in self.Elements]
        return "[" + ", ".join(elements) + "]"


class Hashable:
    def hash_key(self):
        raise NotImplementedError


@dataclass(frozen=True)
class HashKey:
    Type: str
    Value: int


@dataclass
class HashPair:
    Key: Object
    Value: Object


@dataclass
class Hash(Object):
    Pairs: dict[HashKey, HashPair] = field(default_factory=dict)

    def Type(self):
        return HASH_OBJ

    def Inspect(self):
        pairs = []

        for pair in self.Pairs.values():
            pairs.append(f"{pair.Key.Inspect()}: {pair.Value.Inspect()}")

        return "{" + ", ".join(pairs) + "}"
