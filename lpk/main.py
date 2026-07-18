import lpk.Lexer.Lexer as Lexer
import lpk.Token.Token as Token


def main():
    source = "let five = 5;"
    lexer = Lexer.New(source)

    while True:
        tok = lexer.next_token()
        print(tok)

        if tok.TokenType == Token.EOF:
            break


if __name__ == "__main__":
    main()
