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
    return Evaluator.evals(program)


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
        ("1 == 1", True),  # type of a is same as b
        # ("1 === 1", True),  # a equal b
        # ("1 ==== 1", True),  # a is b
        # ("1 ===== 1", False),  # always false
        ("1 == 2", True),
        # ("1 === 2", False),
        # ("1 ==== 2", False),
        # ("1 ===== 2", False),
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
        ("-Ma", "Dioi Operator: -BOOLEAN"),
        ("Ma + Maheni", "Dioi Operator: BOOLEAN + BOOLEAN"),
        ("3$Ma + Maheni$3", "Dioi Operator: BOOLEAN + BOOLEAN"),
        (
            "Akorwo (10 > 1) Anjiriria Ma + Maheni$ Rikia",
            "Dioi Operator: BOOLEAN + BOOLEAN",
        ),
        (
            "Akorwo (10 > 1) Anjiriria Akorwo (10 > 1) Anjiriria Chokia Ma + Maheni$ Rikia Chokia 1$ Rikia",
            "Dioi Operator: BOOLEAN + BOOLEAN",
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


# end
