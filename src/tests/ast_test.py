import kpl.Ast.Ast as Ast
import kpl.Token.Token as Token


def test_string():

    program = Ast.Program(
        statements=[
            Ast.RekaStatement(
                Token=Token.Token(Token.REKA, "Reka"),
                Name=Ast.Identifier(
                    Token=Token.Token(Token.IDENT, "myVar"),
                    Value="myVar",
                ),
                Value=Ast.Identifier(
                    Token=Token.Token(Token.IDENT, "anotherVar"),
                    Value="anotherVar",
                ),
            )
        ]
    )

    expected = "Reka myVar = anotherVar$"

    if str(program) != expected:
        raise AssertionError(f'program.__str__() wrong. got="{str(program)}"')
