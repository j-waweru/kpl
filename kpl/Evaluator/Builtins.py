import kpl.Object.Object as Object
import kpl.Evaluator.Evaluator as Evaluator


def new_error(message):
    return Object.Error(Message=message)


def builtin_len(*args):
    if len(args) != 1:
        return new_error(f"wrong number of arguments. got={len(args)}, want=1")

    arg = args[0]

    if isinstance(arg, Object.Array):
        return Object.Integer(Value=len(arg.Elements))

    if isinstance(arg, Object.String):
        return Object.Integer(Value=len(arg.Value))

    return new_error(f"argument to `len` not supported, got {arg.Type()}")


def builtin_first(*args):
    if len(args) != 1:
        return new_error(f"wrong number of arguments. got={len(args)}, want=1")

    if args[0].Type() != Object.ARRAY_OBJ:
        return new_error(f"argument to `first` must be ARRAY, got {args[0].Type()}")

    arr = args[0]

    if len(arr.Elements) > 0:
        return arr.Elements[0]

    return Evaluator.GUTIRI


def builtin_last(*args):
    if len(args) != 1:
        return new_error(f"wrong number of arguments. got={len(args)}, want=1")

    if args[0].Type() != Object.ARRAY_OBJ:
        return new_error(f"argument to `last` must be ARRAY, got {args[0].Type()}")

    arr = args[0]
    length = len(arr.Elements)

    if length > 0:
        return arr.Elements[length - 1]

    return Evaluator.GUTIRI


def builtin_rest(*args):
    if len(args) != 1:
        return new_error(f"wrong number of arguments. got={len(args)}, want=1")

    if args[0].Type() != Object.ARRAY_OBJ:
        return new_error(f"argument to `rest` must be ARRAY, got {args[0].Type()}")

    arr = args[0]
    length = len(arr.Elements)

    if length > 0:
        return Object.Array(Elements=arr.Elements[1:])

    return Evaluator.GUTIRI


def builtin_push(*args):
    if len(args) != 2:
        return new_error(f"wrong number of arguments. got={len(args)}, want=2")

    if args[0].Type() != Object.ARRAY_OBJ:
        return new_error(f"argument to `push` must be ARRAY, got {args[0].Type()}")

    arr = args[0]
    new_elements = arr.Elements.copy()
    new_elements.append(args[1])

    return Object.Array(Elements=new_elements)


def builtin_nyonia(*args):

    for arg in args:
        print(arg.Inspect())

    return Evaluator.GUTIRI


builtins = {
    "len": Object.Builtin(Fn=builtin_len),
    "first": Object.Builtin(Fn=builtin_first),
    "last": Object.Builtin(Fn=builtin_last),
    "rest": Object.Builtin(Fn=builtin_rest),
    "push": Object.Builtin(Fn=builtin_push),
    "nyonia": Object.Builtin(Fn=builtin_nyonia),
}
