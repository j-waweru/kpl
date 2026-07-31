import kpl.Object.Object as Object
import kpl.Evaluator.Evaluator as Evaluator
import kpl.Lexer.Lexer as Lexer
import kpl.Parser.Parser as Parser


def test_eval_integer_expression():
    tests = [
        ("5", 5),
        ("10", 10),
        ("-5", -5),
        ("5 % 3", 2),
        ("-10", -10),
        ("5 + 5 + 5 + 5 - 10", 10),
        ("2 * 2 * 2 * 2 * 2", 32),
        ("-50 + 100 + -50", 0),
        ("5 * 2 + 10", 20),
        ("5 + 2 * 10", 25),
        ("20 + 2 * -10", 0),
        ("50 / 2 * 2 + 10", 60),
        ("2 * (5 + 10)", 30),
        ("3 * 3 * 3 + 10", 37),
        ("3 * (3 * 3) + 10", 37),
        ("(5 + 10 * 2 + 15 / 3) * 2 + -10", 50),
    ]

    for item, expected in tests:
        evaluated = check_eval(item)
        check_integer_object(evaluated, expected)


def check_eval(inputs):
    l = Lexer.New(inputs)
    p = Parser.New(l)
    program = p.parse_program()
    # call the evaluator with the ast
    env = Object.Environment()
    return Evaluator.evals(program, env)


def check_integer_object(obj, expected) -> bool:

    if not isinstance(obj, Object.Integer):
        # Want the return value of the evals fn to be an Integer Object

        raise AssertionError(f"Object is not Integer , got {obj}")
        return False

    if obj.Value != expected:
        raise AssertionError(
            f"Object has the wrong value, got {obj.Value} wanted {expected}"
        )
        return False

    return True


def test_eval_bool_expression():
    tests = [
        # make sure they pass
        ("1 == 1", True),  # always true
        ("1 === 1", True),  # type of a is same as b
        ("1 ==== 1", True),  # a equal b
        ("1 ===== 1", True),  # a is b
        ("1 ====== 1", False),  # always false
        ("1 == 2", True),
        ("1 === 2", True),
        ("1 ==== 2", False),
        ("1 ===== 2", False),
        ("1 ====== 2", False),
        ("Ma", True),
        ("Maheni", False),
        ("1 < 2", True),
        ("1 > 2", False),
        ("1 < 1", False),
        ("1 > 1", False),
        ("1 != 1", False),
        ("1 != 2", True),
        ("Ma == Ma", True),
        ("Maheni == Maheni", True),
        ("Ma == Maheni", False),
        ("Ma != Maheni", True),
        ("Maheni != Ma", True),
        ("(1 < 2) == Ma", True),
        ("(1 < 2) == Maheni", False),
        ("(1 > 2) == Ma", False),
        ("(1 > 2) == Maheni", True),
    ]
    for item, expected in tests:
        evaluated = check_eval(item)
        check_boolean_object(evaluated, expected)


def check_boolean_object(obj, expected) -> bool:

    if obj.Value != expected:
        raise AssertionError(
            f"Object has the wrong value, got {obj.Value} wanted {expected}"
        )
        return False

    if not isinstance(obj, Object.Boolean):
        # Want the return value of the evals fn to be an Boolean Object

        raise AssertionError(f"Object is not Boolean, got {obj}")
        return False

    return True


def test_bang_operator():
    tests = [
        ("!5", False),
        ("!Ma", False),
        ("!Maheni", True),
        ("!!Ma", True),
        ("!!Maheni", False),
        ("!!5", True),
    ]
    for item, expected in tests:
        evaluated = check_eval(item)
        check_boolean_object(evaluated, expected)


def test_akorwo_tiguo_expression():
    tests = [
        ("Akorwo (Ma) Anjiriria 10 Rikia", 10),
        ("Akorwo (Maheni) Anjiriria 10 Rikia", None),
        ("Akorwo (1) Anjiriria 10 Rikia", 10),
        ("Akorwo (1 < 2) Anjiriria 10 Rikia", 10),
        ("Akorwo (1 > 2) Anjiriria 10 Rikia", None),
        ("Akorwo (1 > 2) Anjiriria 10 Rikia Tiguo Anjiriria 20 Rikia", 20),
        ("Akorwo (1 < 2) Anjiriria 10 Rikia Tiguo Anjiriria 20 Rikia", 10),
    ]
    for item, expected in tests:
        evaluated = check_eval(item)

        if isinstance(expected, int):
            check_integer_object(evaluated, expected)

        else:
            check_null_object(evaluated)


def check_null_object(obj):

    if obj != Evaluator.GUTIRI:
        raise AssertionError(f"Object in not GUTIRI. Got {obj} ")
        return False

    return True


def test_chokia_statements():
    tests = [
        (
            "Akorwo (10 > 1) Anjiriria Akorwo ( 10 > 1) Anjiriria Chokia 10$ Rikia Chokia 1$ Rikia",
            10,
        ),
        ("Chokia 10$", 10),
        ("Chokia 10$ 9$", 10),
        ("Chokia 2* 5$ 9$", 10),
        ("9$ Chokia 2* 5$ 9$", 10),
    ]
    for item, expected in tests:
        evaluated = check_eval(item)
        check_integer_object(evaluated, expected)


def test_error_handling():
    tests = [
        ("5 + Ma", "Mithemba ndihainaine: INTEGER + BOOLEAN"),
        ("5 + Ma$ 5$", "Mithemba ndihainaine: INTEGER + BOOLEAN"),
        ("-Ma", "Ndimenyekaine: -BOOLEAN"),
        ("Ma + Maheni", "Ndimenyekaine: BOOLEAN + BOOLEAN"),
        ("3$Ma + Maheni$3", "Ndimenyekaine: BOOLEAN + BOOLEAN"),
        (
            "Akorwo (10 > 1) Anjiriria Ma + Maheni$ Rikia",
            "Ndimenyekaine: BOOLEAN + BOOLEAN",
        ),
        (
            "Akorwo (10 > 1) Anjiriria Akorwo (10 > 1) Anjiriria Chokia Ma + Maheni$ Rikia Chokia 1$ Rikia",
            "Ndimenyekaine: BOOLEAN + BOOLEAN",
        ),
        ("foobar", "Kĩmenyithia gĩtionekire: foobar"),
        (
            "{'name':'Monkey'}[Fn(x) Anjiriria x$ Rikia]",
            "Gĩtigĩkorwo kiĩko kia hash: FUNCTION",
        ),
    ]
    for item, expected in tests:
        evaluated = check_eval(item)
        if not isinstance(evaluated, Object.Error):
            raise AssertionError(f"Not an error object got {evaluated}")

        if evaluated.Message != expected:
            raise AssertionError(
                f"Wrong error Message got {evaluated.Message} expected {expected}"
            )


def test_reka_statements():
    tests = [
        ("Reka a = 5$ a$", 5),
        ("Reka a = 5*5$ a$", 25),
        ("Reka a = 5$ Reka b = a$ b$", 5),
        ("Reka a = 5$ Reka b = a$ Reka c = a + b+ 5 $ c$", 15),
    ]

    for item, expected in tests:
        check_integer_object(check_eval(item), expected)


def test_function_object():
    inputs = "Fn(x) Anjiriria x + 2$ Rikia$"

    l = Lexer.New(inputs)
    p = Parser.New(l)
    program = p.parse_program()

    env = Object.Environment()
    evaluated = Evaluator.evals(program, env)

    if not isinstance(evaluated, Object.Function):
        raise AssertionError(
            f"Object is not Function. Got {type(evaluated)} ({evaluated})"
        )

    if len(evaluated.Parameters) != 1:
        raise AssertionError(
            f"Function has wrong parameters. Parameters={evaluated.Parameters}"
        )

    if str(evaluated.Parameters[0]) != "x":
        raise AssertionError(f"Parameter is not 'x'. Got {evaluated.Parameters[0]}")

    expected_body = "(x + 2)"

    if str(evaluated.Body) != expected_body:
        raise AssertionError(f'Body is not "{expected_body}". Got "{evaluated.Body}"')


def test_function_application():
    tests = [
        ("Reka identity = Fn(x) Anjiriria x$ Rikia$ identity(5)$", 5),
        ("Reka identity = Fn(x) Anjiriria Chokia x$ Rikia$ identity(5)$", 5),
        ("Reka double = Fn(x) Anjiriria x * 2$ Rikia$ double(5)$", 10),
        ("Reka add = Fn(x, y) Anjiriria x + y$ Rikia$ add(5, 5)$", 10),
        (
            "Reka add = Fn(x, y) Anjiriria x + y$ Rikia$ add(5 + 5, add(5, 5))$",
            20,
        ),
        ("Fn(x) Anjiriria x$ Rikia(5)$", 5),
    ]

    for inputs, expected in tests:
        evaluated = check_eval(inputs)
        check_integer_object(evaluated, expected)


def test_string_literal():
    inputs = "'Hello World!'"

    evaluated = check_eval(inputs)

    if not isinstance(evaluated, Object.String):
        raise AssertionError(
            f"Object is not String. Got {type(evaluated)} ({evaluated})"
        )

    if evaluated.Value != "Hello World!":
        raise AssertionError(f'String has wrong value. Got "{evaluated.Value}"')


def test_string_concatenation():
    tests = [
        ("'Hello' + ' ' + 'World!'", "Hello World!"),
        ("'Hello' - 'World!'", "HeWrd!"),
        ("'banana' - 'an'", "b"),
        ("'abcdef' - 'bd'", "acef"),
        ("'abc' - 'xyz'", "abcxyz"),
        ("'abc' - 'abc'", ""),
        ("'Mississippi' - 'is'", "Mpp"),
        ("'Hello' - 'World!' - 'H'", "eWrd!"),
    ]

    for inputs, expected in tests:
        evaluated = check_eval(inputs)

        if not isinstance(evaluated, Object.String):
            raise AssertionError(
                f"Object is not String. Got {type(evaluated)} ({evaluated})"
            )

        if evaluated.Value != expected:
            raise AssertionError(
                f'String has wrong value. Got "{evaluated.Value}", expected "{expected}"'
            )


def test_builtin_functions():
    tests = [
        ("_Uraihu('')", 0),
        ("_Uraihu('four')", 4),
        ("_Uraihu('hello world')", 11),
        ("_Uraihu(1)", "Iyo nditikiritio, Ndona INTEGER, hali uraihu"),
        (
            "_Uraihu('one', 'two')",
            "Namba ndĩkinyanĩte. Ndona=2, ngwendaga=1",
        ),
    ]

    for inputs, expected in tests:
        evaluated = check_eval(inputs)

        if isinstance(expected, int):
            check_integer_object(evaluated, expected)

        elif isinstance(expected, str):
            if not isinstance(evaluated, Object.Error):
                raise AssertionError(
                    f"Object is not Error. Got {type(evaluated)} ({evaluated})"
                )

            if evaluated.Message != expected:
                raise AssertionError(
                    f'Wrong error message. Expected "{expected}", got "{evaluated.Message}"'
                )


def test_array_literals():
    inputs = "[1, 2 * 2, 3 + 3]"

    evaluated = check_eval(inputs)

    if not isinstance(evaluated, Object.Array):
        raise AssertionError(
            f"Object is not Array. Got {type(evaluated)} ({evaluated})"
        )

    if len(evaluated.Elements) != 3:
        raise AssertionError(
            f"Array has wrong number of elements. Got {len(evaluated.Elements)}"
        )

    check_integer_object(evaluated.Elements[0], 1)
    check_integer_object(evaluated.Elements[1], 4)
    check_integer_object(evaluated.Elements[2], 6)


def check_error_object(obj, expected_message):
    if not isinstance(obj, Object.Error):
        raise AssertionError(f"Object is not Error. Got {type(obj)} ({obj})")

    if obj.Message != expected_message:
        raise AssertionError(
            f'Wrong error message.\nExpected: "{expected_message}"\nGot:      "{obj.Message}"'
        )


def test_array_index_expressions():
    tests = [
        ("[1, 2, 3][-1]", 1),
        ("[1, 2, 3][-2]", 2),
        ("[1, 2, 3][-3]", 3),
        ("Reka i = -1$ [1][i]$", 1),
        ("[1, 2, 3][-1 - 1]$", 2),
        ("Reka myArray = [1, 2, 3]$ myArray[-3]$", 3),
        (
            "Reka myArray = [1, 2, 3]$ myArray[-3] + myArray[-1] + myArray[-2]$",
            6,
        ),
        (
            "Reka myArray = [1, 2, 3]$ Reka i = myArray[-1]$ myArray[-i]$",
            1,
        ),
        ("[1, 2, 3][-4]$", None),
        ("[1, 2, 3][0]$", "Array indices chithiaga oo -1,-2,-3. Ndona 0. Gutiri 0,1,2"),
        ("[1, 2, 3][1]$", "Array indices chithiaga oo -1,-2,-3. Ndona 1. Gutiri 0,1,2"),
    ]

    for inputs, expected in tests:
        evaluated = check_eval(inputs)

        if isinstance(expected, int):
            check_integer_object(evaluated, expected)

        elif expected is None:
            check_null_object(evaluated)

        elif isinstance(expected, str):
            check_error_object(evaluated, expected)

        else:
            raise AssertionError(f"Unknown expected value: {expected}")


def test_hash_literals():

    inputs = """
        Reka two = 'two'$

        {
            'one': 10 - 9,
            two: 1 + 1,
            'thr' + 'ee': 6 / 2,
            4: 4,
            Ma: 5,
            Maheni: 6
        }
    """

    evaluated = check_eval(inputs)

    if not isinstance(evaluated, Object.Hash):
        raise AssertionError(f"Eval didn't return Hash. Got {type(evaluated)}")

    expected = {
        Object.String("one").hash_key(): 1,
        Object.String("two").hash_key(): 2,
        Object.String("three").hash_key(): 3,
        Object.Integer(4).hash_key(): 4,
        Evaluator.MA.hash_key(): 5,
        Evaluator.MAHENI.hash_key(): 6,
    }

    assert len(evaluated.Pairs) == len(expected)

    for key, expected_value in expected.items():
        pair = evaluated.Pairs.get(key)

        assert pair is not None

        check_integer_object(pair.Value, expected_value)


def test_hash_index_expressions():

    tests = [
        ("{'foo': 5}['foo']", 5),
        ("{'foo': 5}['bar']", None),
        ("Reka key = 'foo'$ {'foo': 5}[key]", 5),
        ("{}['foo']", None),
        ("{5: 5}[5]", 5),
        ("{Ma: 5}[Ma]", 5),
        ("{Maheni: 5}[Maheni]", 5),
    ]

    for inputs, expected in tests:
        evaluated = check_eval(inputs)

        if isinstance(expected, int):
            check_integer_object(evaluated, expected)
        else:
            check_null_object(evaluated)


# end
