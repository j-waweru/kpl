import kpl.Object.Object as Object
import kpl.Evaluator.Evaluator as Evaluator


def new_error(message):
    return Object.Error(Message=message)


def builtin_len(*args):
    if len(args) != 1:
        return new_error(f"Namba ndĩkinyanĩte. Ndona={len(args)}, ngwendaga=1")

    arg = args[0]

    if isinstance(arg, Object.Array):
        return Object.Integer(Value=len(arg.Elements))

    if isinstance(arg, Object.String):
        return Object.Integer(Value=len(arg.Value))

    return new_error(f"Iyo nditikiritio, Ndona {arg.Type()}, hali uraihu")


def builtin_first(*args):
    if len(args) != 1:
        return new_error(f"Namba ndĩkinyanĩte={len(args)}, ngwendaga=1")

    if args[0].Type() != Object.ARRAY_OBJ:
        return new_error(f"Ti muthemba wa ARRAY, Ndona {args[0].Type()}, hari mbere")

    arr = args[0]

    if len(arr.Elements) > 0:
        return arr.Elements[0]

    return Evaluator.GUTIRI


def builtin_last(*args):
    if len(args) != 1:
        return new_error(f"Namba ndĩkinyanĩte={len(args)}, want=1")

    if args[0].Type() != Object.ARRAY_OBJ:
        return new_error(f"Ti muthemba wa ARRAY {args[0].Type()}, hari muico")

    arr = args[0]
    length = len(arr.Elements)

    if length > 0:
        return arr.Elements[length - 1]

    return Evaluator.GUTIRI


def builtin_rest(*args):
    if len(args) != 1:
        return new_error(f"Namba ndĩkinyanĩte={len(args)}, want=1")

    if args[0].Type() != Object.ARRAY_OBJ:
        return new_error(
            f"Ti muthemba wa ARRAY, Ndona {args[0].Type()}, hari `gicigo_kiingi`"
        )

    arr = args[0]
    length = len(arr.Elements)

    if length > 0:
        return Object.Array(Elements=arr.Elements[1:])

    return Evaluator.GUTIRI


def builtin_push(*args):
    if len(args) != 2:
        return new_error(f"Namba ndĩkinyanĩte={len(args)}, want=2")

    if args[0].Type() != Object.ARRAY_OBJ:
        return new_error(f"Ti muthemba wa ARRAY, Ndona {args[0].Type()}, hari `ikia`")

    arr = args[0]
    new_elements = arr.Elements.copy()
    new_elements.append(args[1])

    return Object.Array(Elements=new_elements)


def builtin_puts(*args):

    for arg in args:
        print(arg.Inspect())

    return Evaluator.GUTIRI


builtins = {
    "_Uraihu": Object.Builtin(Fn=builtin_len),
    "_Mbere": Object.Builtin(Fn=builtin_first),
    "_Muico": Object.Builtin(Fn=builtin_last),
    "_HauHangi": Object.Builtin(Fn=builtin_rest),
    "_Ikia": Object.Builtin(Fn=builtin_push),
    "_Nyonia": Object.Builtin(Fn=builtin_puts),
}
