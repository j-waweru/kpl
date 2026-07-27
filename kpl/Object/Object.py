from dataclasses import dataclass

ObjectType = str

INTEGER_OBJ = "INTEGER"
BOOLEAN_OBJ = "BOOLEAN"
GUTIRI_OBJ = "GUTIRI"
RIKIA_VALUE_OBJ = "RIKIA_VALUE"

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


@dataclass
class Boolean(Object):
    Value: bool

    def Inspect(self):
        return str(self.Value)

    def Type(self):
        return BOOLEAN_OBJ


@dataclass
class Gutiri(Object):
    def Type(self):
        return GUTIRI_OBJ

    def Inspect(self):
        return "GUTIRI"


@dataclass
class ReturnValue:
    Value: Object

    def Type(self):
        return RIKIA_VALUE_OBJ

    def Inspect(self):
        return self.Value.Inspect()


# end
