import lpk.Lexer.Lexer as Lexer
import lpk.Token.Token as Token


def test_next_token():

    token_input = "Reka five = 5$ Reka ten = 10$ Reka ongerera = fn(x, y) Anjiriria x + y$ Rikia$ Reka result = ongerera(five, ten)$"

    tests = [
        (Token.REKA, "Reka"),
        (Token.IDENT, "five"),
        (Token.ASSIGN, "="),
        (Token.INT, "5"),
        (Token.DOLLAR, "$"),
        (Token.REKA, "Reka"),
        (Token.IDENT, "ten"),
        (Token.ASSIGN, "="),
        (Token.INT, "10"),
        (Token.DOLLAR, "$"),
        (Token.REKA, "Reka"),
        (Token.IDENT, "ongerera"),
        (Token.ASSIGN, "="),
        (Token.FUNCTION, "fn"),
        (Token.LPAREN, "("),
        (Token.IDENT, "x"),
        (Token.COMMA, ","),
        (Token.IDENT, "y"),
        (Token.RPAREN, ")"),
        (Token.ANJIRIRIA, "Anjiriria"),
        (Token.IDENT, "x"),
        (Token.PLUS, "+"),
        (Token.IDENT, "y"),
        (Token.DOLLAR, "$"),
        (Token.RIKIA, "Rikia"),
        (Token.DOLLAR, "$"),
        (Token.REKA, "Reka"),
        (Token.IDENT, "result"),
        (Token.ASSIGN, "="),
        (Token.IDENT, "ongerera"),
        (Token.LPAREN, "("),
        (Token.IDENT, "five"),
        (Token.COMMA, ","),
        (Token.IDENT, "ten"),
        (Token.RPAREN, ")"),
        (Token.DOLLAR, "$"),
        (Token.EOF, "\0"),
    ]

    l = Lexer.New(token_input)

    for expected_type, expected_literal in tests:
        tok = l.next_token()

        print(f"Token 'tok.Literal' of type [{tok.TokenType}] type")
        print()

        assert tok.TokenType == expected_type
        assert tok.Literal == expected_literal
