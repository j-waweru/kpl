import kpl.Ast.Ast as Ast
import kpl.Lexer.Lexer as Lexer
import kpl.Parser.Parser as Parser


def test_reka_statements():

    tests = [
        ("Reka x = 5$", "x", 5),
        ("Reka y = Ma$", "y", True),
        ("Reka foobar = y$", "foobar", "y"),
    ]

    for inputs, expected_identifier, expected_value in tests:
        l = Lexer.New(inputs)
        p = Parser.New(l)

        program = p.parse_program()

        check_parser_errors(p)

        if len(program.statements) != 1:
            raise AssertionError(
                f"program.statements does not contain 1 statement. got={len(program.statements)}"
            )

        stmt = program.statements[0]

        if not check_reka_statement(stmt, expected_identifier):
            return

        val = stmt.Value

        if not check_literal_expression(val, expected_value):
            return


# s is expected to be some Statement node.
# In Python we can check its runtime type with isinstance().
def check_reka_statement(s: Ast.RekaStatement, name: str) -> bool:

    if s.token_literal() != "Reka":
        print(f"s.token_literal() not 'Reka'. got={s.token_literal()!r}")
        return False

    # Go:
    #
    # letStmt, ok := s.(*ast.LetStatement)
    #
    # Python equivalent:
    if not isinstance(s, Ast.RekaStatement):
        print(f"s is not Ast.RekaStatement. got={type(s)}")
        return False

    reka_stmt = s

    if reka_stmt.Name.Value != name:
        print(f"let_stmt.Name.Value not '{name}'. got={reka_stmt.Name.Value}")
        return False

    if reka_stmt.Name.token_literal() != name:
        print(
            f"let_stmt.Name.token_literal() not '{name}'. "
            f"got={reka_stmt.Name.token_literal()}"
        )
        return False

    return True


def check_parser_errors(p: Parser.Parser):
    assert not p.errors, "\n".join(p.errors)


def test_chokia_statements():

    inputs = """
    Chokia 5$
    Chokia 10$
    Chokia 993322$
    """

    l = Lexer.New(inputs)
    p = Parser.New(l)

    program = p.parse_program()

    check_parser_errors(p)

    if len(program.statements) != 3:
        raise AssertionError(
            f"program.statements does not contain 3 statements. "
            f"got={len(program.statements)}"
        )

    for stmt in program.statements:
        if not isinstance(stmt, Ast.ChokiaStatement):
            raise AssertionError(f"stmt is not Ast.ChokiaStatement. got={type(stmt)}")

        if stmt.token_literal() != "Chokia":
            raise AssertionError(
                f"stmt.token_literal() not 'Chokia'. got={stmt.token_literal()}"
            )


def test_identifier_expression():
    inputs = "foobar$"

    l = Lexer.New(inputs)
    p = Parser.New(l)

    program = p.parse_program()

    check_parser_errors(p)

    if len(program.statements) != 1:
        raise AssertionError(
            f"program has not enough statements. got={len(program.statements)}"
        )

    stmt = program.statements[0]

    if not isinstance(stmt, Ast.ExpressionStatement):
        raise AssertionError(
            f"program.statements[0] is not Ast.ExpressionStatement. got={type(stmt)}"
        )

    ident = stmt.Expression

    if not isinstance(ident, Ast.Identifier):
        raise AssertionError(f"exp not Ast.Identifier. got={type(ident)}")

    if ident.Value != "foobar":
        raise AssertionError(f'ident.Value not "foobar". got={ident.Value}')

    if ident.token_literal() != "foobar":
        raise AssertionError(
            f'ident.token_literal() not "foobar". got={ident.token_literal()}'
        )


def test_integer_literal_expression():

    inputs = "5$"

    l = Lexer.New(inputs)
    p = Parser.New(l)

    program = p.parse_program()

    check_parser_errors(p)

    if len(program.statements) != 1:
        raise AssertionError(
            f"program has not enough statements. got={len(program.statements)}"
        )

    stmt = program.statements[0]

    if not isinstance(stmt, Ast.ExpressionStatement):
        raise AssertionError(
            f"program.statements[0] is not Ast.ExpressionStatement. got={type(stmt)}"
        )

    literal = stmt.Expression

    if not isinstance(literal, Ast.IntegerLiteral):
        raise AssertionError(f"exp not Ast.IntegerLiteral. got={type(literal)}")

    if literal.Value != 5:
        raise AssertionError(f"literal.Value not 5. got={literal.Value}")

    if literal.token_literal() != "5":
        raise AssertionError(
            f'literal.token_literal() not "5". got={literal.token_literal()}'
        )


def test_parsing_prefix_expressions():

    prefix_tests = [
        ("!5$", "!", 5),
        ("-15$", "-", 15),
        ("!Ma$", "!", True),
        ("!Maheni$", "!", False),
    ]

    for inputs, operator, value in prefix_tests:
        l = Lexer.New(inputs)
        p = Parser.New(l)

        program = p.parse_program()

        check_parser_errors(p)

        if len(program.statements) != 1:
            raise AssertionError(
                f"program.statements does not contain 1 statement. "
                f"got={len(program.statements)}"
            )

        stmt = program.statements[0]

        if not isinstance(stmt, Ast.ExpressionStatement):
            raise AssertionError(
                f"program.statements[0] is not Ast.ExpressionStatement. "
                f"got={type(stmt)}"
            )

        exp = stmt.Expression

        if not isinstance(exp, Ast.PrefixExpression):
            raise AssertionError(
                f"stmt.Expression is not Ast.PrefixExpression. got={type(exp)}"
            )

        if exp.Operator != operator:
            raise AssertionError(
                f"exp.Operator is not '{operator}'. got={exp.Operator}"
            )

        if not check_literal_expression(exp.Right, value):
            return


def check_integer_literal(exp: Ast.Expression, value: int) -> bool:

    if not isinstance(exp, Ast.IntegerLiteral):
        print(f"exp is not Ast.IntegerLiteral. got={type(exp)}")
        return False

    if exp.Value != value:
        print(f"exp.Value not {value}. got={exp.Value}")
        return False

    if exp.token_literal() != str(value):
        print(f'exp.token_literal() not "{value}". got={exp.token_literal()}')
        return False

    return True


def test_parsing_infix_expressions():

    infix_tests = [
        ("5 + 5$", 5, "+", 5),
        ("5 - 5$", 5, "-", 5),
        ("5 * 5$", 5, "*", 5),
        ("5 / 5$", 5, "/", 5),
        ("5 > 5$", 5, ">", 5),
        ("5 < 5$", 5, "<", 5),
        ("5 == 5$", 5, "==", 5),
        ("5 != 5$", 5, "!=", 5),
        ("Ma == Ma$", True, "==", True),
        ("Ma != Maheni$", True, "!=", False),
        ("Maheni == Maheni$", False, "==", False),
    ]

    for inputs, left_value, operator, right_value in infix_tests:
        l = Lexer.New(inputs)
        p = Parser.New(l)

        program = p.parse_program()

        check_parser_errors(p)

        if len(program.statements) != 1:
            raise AssertionError(
                f"program.statements does not contain 1 statement. "
                f"got={len(program.statements)}"
            )

        stmt = program.statements[0]

        if not isinstance(stmt, Ast.ExpressionStatement):
            raise AssertionError(
                f"program.statements[0] is not Ast.ExpressionStatement. "
                f"got={type(stmt)}"
            )

        exp = stmt.Expression

        if not isinstance(exp, Ast.InfixExpression):
            raise AssertionError(f"exp is not Ast.InfixExpression. got={type(exp)}")

        if not check_literal_expression(exp.Left, left_value):
            return

        if exp.Operator != operator:
            raise AssertionError(
                f"exp.Operator is not '{operator}'. got={exp.Operator}"
            )

        if not check_literal_expression(exp.Right, right_value):
            return


def test_operator_precedence_parsing():

    tests = [
        ("-a", "(-a)"),
        ("!-a", "(!(-a))"),
        ("a + b + c", "((a + b) + c)"),
        ("a + b - c", "((a + b) - c)"),
        ("a * b * c", "((a * b) * c)"),
        ("a * b / c", "((a * b) / c)"),
        ("a + b / c", "(a + (b / c))"),
        ("a + b * c + d / e - f", "(((a + (b * c)) + (d / e)) - f)"),
        ("3 + 4$ -5 * 5", "(3 + 4)((-5) * 5)"),
        ("5 > 4 == 3 < 4", "((5 > 4) == (3 < 4))"),
        ("5 < 4 != 3 > 4", "((5 < 4) != (3 > 4))"),
        (
            "3 + 4 * 5 == 3 * 1 + 4 * 5",
            "((3 + (4 * 5)) == ((3 * 1) + (4 * 5)))",
        ),
        ("Ma", "Ma"),
        ("Maheni", "Maheni"),
        ("3 > 5 == Maheni", "((3 > 5) == Maheni)"),
        (
            "1 + (2 + 3) + 4",
            "((1 + (2 + 3)) + 4)",
        ),
        ("(5 + 5) * 2", "((5 + 5) * 2)"),
        ("2 / (5 + 5)", "(2 / (5 + 5))"),
        ("-(5 + 5)", "(-(5 + 5))"),
        ("!(Ma == Ma)", "(!(Ma == Ma))"),
        (
            "a + add(b * c) + d",
            "((a + add((b * c))) + d)",
        ),
        (
            "add(a, b, 1, 2 * 3, 4 + 5, add(6, 7 * 8))",
            "add(a, b, 1, (2 * 3), (4 + 5), add(6, (7 * 8)))",
        ),
        (
            "add(a + b + c * d / f + g)",
            "add((((a + b) + ((c * d) / f)) + g))",
        ),
    ]

    for inputs, expected in tests:
        l = Lexer.New(inputs)
        p = Parser.New(l)

        program = p.parse_program()

        check_parser_errors(p)

        actual = str(program)

        if actual != expected:
            raise AssertionError(f'expected="{expected}", got="{actual}"')


def check_identifier(exp: Ast.Expression, value: str) -> bool:

    if not isinstance(exp, Ast.Identifier):
        print(f"exp not Ast.Identifier. got={type(exp)}")
        return False

    if exp.Value != value:
        print(f"ident.Value not {value}. got={exp.Value}")
        return False

    if exp.token_literal() != value:
        print(f"ident.token_literal() not {value}. got={exp.token_literal()}")
        return False

    return True


def check_boolean_literal(exp: Ast.Expression, value: bool) -> bool:

    if not isinstance(exp, Ast.Boolean):
        print(f"exp not Ast.Boolean. got={type(exp)}")
        return False

    if exp.Value != value:
        print(f"bo.Value not {value}. got={exp.Value}")
        return False

    expected = "Ma" if value else "Maheni"

    if exp.token_literal() != expected:
        print(f"bo.token_literal() not {expected}. got={exp.token_literal()}")
        return False

    return True


def check_literal_expression(
    exp: Ast.Expression,
    expected: int | str | bool,
) -> bool:

    # bool before int because bool is a subclass of int in Python
    if isinstance(expected, bool):
        return check_boolean_literal(exp, expected)

    if isinstance(expected, int):
        return check_integer_literal(exp, expected)

    if isinstance(expected, str):
        return check_identifier(exp, expected)

    print(f"type of expected not handled. got={type(expected)}")
    return False


def check_infix_expression(
    exp: Ast.Expression,
    left: int | str,
    operator: str,
    right: int | str,
) -> bool:

    if not isinstance(exp, Ast.InfixExpression):
        print(f"exp is not Ast.InfixExpression. got={type(exp)}")
        return False

    if not check_literal_expression(exp.Left, left):
        return False

    if exp.Operator != operator:
        print(f"exp.Operator is not '{operator}'. got={exp.Operator}")
        return False

    if not check_literal_expression(exp.Right, right):
        return False

    return True


def test_boolean_expression():

    tests = [
        ("Ma$", True),
        ("Maheni$", False),
    ]

    for inputs, expected in tests:
        l = Lexer.New(inputs)
        p = Parser.New(l)

        program = p.parse_program()

        check_parser_errors(p)

        stmt = program.statements[0]

        if not isinstance(stmt, Ast.ExpressionStatement):
            raise AssertionError(f"stmt not Ast.ExpressionStatement. got={type(stmt)}")

        if not check_boolean_literal(stmt.Expression, expected):
            return


def test_if_expression():

    inputs = "Akorwo (x < y) Anjiriria x Rikia"

    l = Lexer.New(inputs)
    p = Parser.New(l)

    program = p.parse_program()

    check_parser_errors(p)

    if len(program.statements) != 1:
        raise AssertionError(
            f"program.statements does not contain 1 statement. got={len(program.statements)}"
        )

    stmt = program.statements[0]

    if not isinstance(stmt, Ast.ExpressionStatement):
        raise AssertionError(
            f"program.statements[0] is not Ast.ExpressionStatement. got={type(stmt)}"
        )

    exp = stmt.Expression

    if not isinstance(exp, Ast.AkorwoExpression):
        raise AssertionError(
            f"stmt.Expression is not Ast.IfExpression. got={type(exp)}"
        )

    if not check_infix_expression(exp.Condition, "x", "<", "y"):
        return

    if len(exp.Consequence.Statements) != 1:
        raise AssertionError(
            f"consequence does not contain 1 statement. got={len(exp.Consequence.Statements)}"
        )

    consequence = exp.Consequence.Statements[0]

    if not isinstance(consequence, Ast.ExpressionStatement):
        raise AssertionError(
            f"Consequence statement is not Ast.ExpressionStatement. got={type(consequence)}"
        )

    if not check_identifier(consequence.Expression, "x"):
        return

    if exp.Alternative is not None:
        raise AssertionError(f"Alternative was not None. got={exp.Alternative}")


def test_if_else_expression():

    inputs = "Akorwo (x < y) Anjiriria x Rikia Tiguo Anjiriria y Rikia"

    l = Lexer.New(inputs)
    p = Parser.New(l)

    program = p.parse_program()

    check_parser_errors(p)

    stmt = program.statements[0]

    if not isinstance(stmt, Ast.ExpressionStatement):
        raise AssertionError(f"stmt is not Ast.ExpressionStatement. got={type(stmt)}")

    exp = stmt.Expression

    if not isinstance(exp, Ast.AkorwoExpression):
        raise AssertionError(f"exp is not Ast.AkorwoExpression. got={type(exp)}")

    if not check_infix_expression(exp.Condition, "x", "<", "y"):
        return

    if len(exp.Consequence.Statements) != 1:
        raise AssertionError(
            f"consequence does not contain 1 statement. got={len(exp.Consequence.Statements)}"
        )

    consequence = exp.Consequence.Statements[0]

    if not check_identifier(consequence.Expression, "x"):
        return

    if exp.Alternative is None:
        raise AssertionError("Alternative is None")

    if len(exp.Alternative.Statements) != 1:
        raise AssertionError(
            f"alternative does not contain 1 statement. got={len(exp.Alternative.Statements)}"
        )

    alternative = exp.Alternative.Statements[0]

    if not isinstance(alternative, Ast.ExpressionStatement):
        raise AssertionError(
            f"alternative statement is not Ast.ExpressionStatement. got={type(alternative)}"
        )

    if not check_identifier(alternative.Expression, "y"):
        return


def test_function_literal_parsing():

    inputs = "fn(x, y) Anjiriria x + y$ Rikia"

    l = Lexer.New(inputs)
    p = Parser.New(l)

    program = p.parse_program()

    check_parser_errors(p)

    if len(program.statements) != 1:
        raise AssertionError(
            f"program.statements does not contain 1 statement. got={len(program.statements)}"
        )

    stmt = program.statements[0]

    if not isinstance(stmt, Ast.ExpressionStatement):
        raise AssertionError(
            f"program.statements[0] is not Ast.ExpressionStatement. got={type(stmt)}"
        )

    function = stmt.Expression

    if not isinstance(function, Ast.FunctionLiteral):
        raise AssertionError(
            f"stmt.Expression is not Ast.FunctionLiteral. got={type(function)}"
        )

    if len(function.Parameters) != 2:
        raise AssertionError(
            f"function literal parameters wrong. want=2 got={len(function.Parameters)}"
        )

    check_literal_expression(function.Parameters[0], "x")
    check_literal_expression(function.Parameters[1], "y")

    if len(function.Body.Statements) != 1:
        raise AssertionError(
            f"function.Body.Statements has not 1 statement. got={len(function.Body.Statements)}"
        )

    body_stmt = function.Body.Statements[0]

    if not isinstance(body_stmt, Ast.ExpressionStatement):
        raise AssertionError(
            f"function body stmt is not Ast.ExpressionStatement. got={type(body_stmt)}"
        )

    check_infix_expression(body_stmt.Expression, "x", "+", "y")


def test_function_parameter_parsing():

    tests = [
        ("fn() Anjiriria Rikia", []),
        ("fn(x) Anjiriria Rikia", ["x"]),
        ("fn(x, y, z) Anjiriria Rikia", ["x", "y", "z"]),
    ]

    for inputs, expected_params in tests:
        l = Lexer.New(inputs)
        p = Parser.New(l)

        program = p.parse_program()

        check_parser_errors(p)

        stmt = program.statements[0]

        if not isinstance(stmt, Ast.ExpressionStatement):
            raise AssertionError(f"Expected ExpressionStatement, got {type(stmt)}")

        function = stmt.Expression

        if not isinstance(function, Ast.FunctionLiteral):
            raise AssertionError(f"Expected FunctionLiteral, got {type(function)}")

        if len(function.Parameters) != len(expected_params):
            raise AssertionError(
                f"length parameters wrong. want={len(expected_params)} got={len(function.Parameters)}"
            )

        for i, ident in enumerate(expected_params):
            check_literal_expression(function.Parameters[i], ident)


def test_call_expression_parsing():

    inputs = "add(1, 2 * 3, 4 + 5)$"

    l = Lexer.New(inputs)
    p = Parser.New(l)

    program = p.parse_program()

    check_parser_errors(p)

    if len(program.statements) != 1:
        raise AssertionError(
            f"program.statements does not contain 1 statement. got={len(program.statements)}"
        )

    stmt = program.statements[0]

    if not isinstance(stmt, Ast.ExpressionStatement):
        raise AssertionError(f"stmt is not Ast.ExpressionStatement. got={type(stmt)}")

    exp = stmt.Expression

    if not isinstance(exp, Ast.CallExpression):
        raise AssertionError(
            f"stmt.Expression is not Ast.CallExpression. got={type(exp)}"
        )

    check_identifier(exp.Function, "add")

    if len(exp.Arguments) != 3:
        raise AssertionError(f"wrong length of arguments. got={len(exp.Arguments)}")

    check_literal_expression(exp.Arguments[0], 1)
    check_infix_expression(exp.Arguments[1], 2, "*", 3)
    check_infix_expression(exp.Arguments[2], 4, "+", 5)


# han
