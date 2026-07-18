import lpk.Lexer.Lexer as Lexer
import lpk.Token.Token as Token


def test_next_token():

    token_input = "let five = 5; let ten = 10; let add = fn(x, y) { x + y; }; let result = add(five, ten);"

    tests = [
        (Token.LET, "let"),
        (Token.IDENT, "five"),
        (Token.ASSIGN, "="),
        (Token.INT, "5"),
        (Token.SEMICOLON, ";"),
        (Token.LET, "let"),
        (Token.IDENT, "ten"),
        (Token.ASSIGN, "="),
        (Token.INT, "10"),
        (Token.SEMICOLON, ";"),
        (Token.LET, "let"),
        (Token.IDENT, "add"),
        (Token.ASSIGN, "="),
        (Token.FUNCTION, "fn"),
        (Token.LPAREN, "("),
        (Token.IDENT, "x"),
        (Token.COMMA, ","),
        (Token.IDENT, "y"),
        (Token.RPAREN, ")"),
        (Token.LBRACE, "{"),
        (Token.IDENT, "x"),
        (Token.PLUS, "+"),
        (Token.IDENT, "y"),
        (Token.SEMICOLON, ";"),
        (Token.RBRACE, "}"),
        (Token.SEMICOLON, ";"),
        (Token.LET, "let"),
        (Token.IDENT, "result"),
        (Token.ASSIGN, "="),
        (Token.IDENT, "add"),
        (Token.LPAREN, "("),
        (Token.IDENT, "five"),
        (Token.COMMA, ","),
        (Token.IDENT, "ten"),
        (Token.RPAREN, ")"),
        (Token.SEMICOLON, ";"),
        (Token.EOF, "\0"),
    ]

    l = Lexer.New(token_input)

    for expected_type, expected_literal in tests:
        tok = l.next_token()

        print(f"Token '{tok.Literal}' of type [{tok.TokenType}] type")
        print()

        assert tok.TokenType == expected_type
        assert tok.Literal == expected_literal
