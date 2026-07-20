import kpl.Lexer.Lexer as Lexer
import kpl.Token.Token as Token


def test_next_token():

    token_input = "Reka five = 5$ Reka ten = 10$ Reka ongerera = fn(x, y) Anjiriria x + y$ Rikia$ Reka result = ongerera(five, ten)$ !-/*5$ 5<10>5$ Akorwo (5 < 10) Anjiriria Chokia Ma$ Rikia Tiguo Anjiriria Chokia Maheni$ Rikia 10 == 10$ 10!=9$"

    tests = [
        (Token.REKA, "Reka"),
        (Token.IDENT, "five"),
        (Token.ASSIGN, "="),
        (Token.INT, "5"),
        (Token.DOLLAR, "$"),
        # part
        (Token.REKA, "Reka"),
        (Token.IDENT, "ten"),
        (Token.ASSIGN, "="),
        (Token.INT, "10"),
        (Token.DOLLAR, "$"),
        # part
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
        # part
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
        # part
        (Token.BANG, "!"),
        (Token.MINUS, "-"),
        (Token.SLASH, "/"),
        (Token.ASTERISK, "*"),
        (Token.INT, "5"),
        (Token.DOLLAR, "$"),
        # part
        (Token.INT, "5"),
        (Token.LT, "<"),
        (Token.INT, "10"),
        (Token.GT, ">"),
        (Token.INT, "5"),
        (Token.DOLLAR, "$"),
        # part
        (Token.AKORWO, "Akorwo"),
        (Token.LPAREN, "("),
        (Token.INT, "5"),
        (Token.LT, "<"),
        (Token.INT, "10"),
        (Token.RPAREN, ")"),
        (Token.ANJIRIRIA, "Anjiriria"),
        (Token.CHOKIA, "Chokia"),
        (Token.MA, "Ma"),
        (Token.DOLLAR, "$"),
        (Token.RIKIA, "Rikia"),
        # part
        (Token.TIGUO, "Tiguo"),
        (Token.ANJIRIRIA, "Anjiriria"),
        (Token.CHOKIA, "Chokia"),
        (Token.MAHENI, "Maheni"),
        (Token.DOLLAR, "$"),
        (Token.RIKIA, "Rikia"),
        # part
        (Token.INT, "10"),
        (Token.EQ, "=="),
        (Token.INT, "10"),
        (Token.DOLLAR, "$"),
        # part
        (Token.INT, "10"),
        (Token.NOT_EQ, "!="),
        (Token.INT, "9"),
        (Token.DOLLAR, "$"),
        # part
        (Token.EOF, "\0"),
    ]

    l = Lexer.New(token_input)

    for expected_type, expected_literal in tests:
        tok = l.next_token()

        print(f"Token [{tok.Literal}] of type [{tok.TokenType}] type")
        print()

        assert tok.TokenType == expected_type
        assert tok.Literal == expected_literal
