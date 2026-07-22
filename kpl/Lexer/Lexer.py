import kpl.Token.Token as Token
from dataclasses import dataclass


@dataclass
class Lexer:
    t_input: str
    position: int
    readposition: int
    ch: str = ""

    def read_char(self):

        if self.readposition >= len(self.t_input):
            self.ch = "\0"
        else:
            self.ch = self.t_input[self.readposition]

        self.position = self.readposition
        self.readposition = self.readposition + 1
        return self

    def next_token(self):
        # tok: Token.Token
        tok = Token.New()
        self.skip_whitespace()

        match self.ch:
            case "=":
                if self.peek_char() == "=":
                    ch = self.ch
                    self.read_char()
                    tok = self.new_token(Token.EQ, str(self.ch) + str(ch))
                else:
                    tok = self.new_token(Token.ASSIGN, self.ch)
            case "$":
                tok = self.new_token(Token.DOLLAR, self.ch)
            case "(":
                tok = self.new_token(Token.LPAREN, self.ch)
            case ")":
                tok = self.new_token(Token.RPAREN, self.ch)
            case ",":
                tok = self.new_token(Token.COMMA, self.ch)
            case "+":
                tok = self.new_token(Token.PLUS, self.ch)

            case "-":
                tok = self.new_token(Token.MINUS, self.ch)
            case "!":
                if self.peek_char() == "=":
                    ch = self.ch
                    self.read_char()
                    tok = self.new_token(Token.NOT_EQ, str(ch) + str(self.ch))
                else:
                    tok = self.new_token(Token.BANG, self.ch)
            case "*":
                tok = self.new_token(Token.ASTERISK, self.ch)
            case "/":
                tok = self.new_token(Token.SLASH, self.ch)
            case "<":
                tok = self.new_token(Token.LT, self.ch)
            case ">":
                tok = self.new_token(Token.GT, self.ch)
            case ";":
                tok = self.new_token(Token.SEMICOLON, self.ch)
            case ",":
                tok = self.new_token(Token.COMMA, self.ch)

            case "\0":
                tok.TokenType = Token.EOF
                tok.Literal = "\0"

            case _:
                if self.is_char(self.ch):
                    tok.Literal = self.read_identifier()
                    tok.TokenType = Token.look_up_ident(tok.Literal)
                    return tok

                elif self.is_digit(self.ch):
                    tok.Literal = self.read_number()
                    tok.TokenType = Token.INT
                    return tok

                else:
                    tok = self.new_token(Token.ILLEGAL, self.ch)
                    self.read_char()
                    return tok

        self.read_char()
        return tok

    def new_token(self, tokenType, ch) -> Token.Token:

        return Token.Token(tokenType, ch)

    def read_identifier(self):
        position = self.position
        while self.is_char(self.ch):
            self.read_char()

        return self.t_input[position : self.position]

    def read_number(self) -> str:
        position = self.position
        while self.is_digit(self.ch):
            self.read_char()
        return self.t_input[position : self.position]

    def is_char(self, ch) -> bool:
        # ch must be a string
        if (
            ord(ch) >= ord("A")
            and ord(ch) <= ord("Z")
            or ord(ch) >= ord("a")
            and ord(ch) <= ord("z")
            or ch == "_"
        ):
            return True
        else:
            return False

    def skip_whitespace(self):

        while self.ch in " \n\t\r":
            self.read_char()

    def is_digit(self, ch):
        if ord(ch) >= ord("0") and ord(ch) <= ord("9"):
            return True
        else:
            return False

    def peek_char(self):
        if self.readposition >= len(self.t_input):
            return False
        else:
            next = self.t_input[self.readposition]
            return next


# l = lexer ( values)
def New(input_str):
    l = Lexer(input_str, 0, 0)
    l.read_char()
    return l
