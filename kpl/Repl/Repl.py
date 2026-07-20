import kpl.Lexer.Lexer as Lexer
import kpl.Token.Token as Token

PROMPT = ">> "


def start():
    while True:
        try:
            line = input(PROMPT)
        except EOFError:
            return

        l = Lexer.New(line)

        tok = l.next_token()

        while tok.TokenType != Token.EOF:
            print(tok)
            tok = l.next_token()
