import lpk.Token.Token as Token
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
        tok = Token.New()
        self.skip_whitespace()

        match self.ch:
            case "=":
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

        while self.ch in "\n\t\r" or self.ch == " ":
            self.read_char()

    def is_digit(self, ch):
        if ord(ch) >= ord("0") and ord(ch) <= ord("9"):
            return True
        else:
            return False


# l = lexer ( values)
def New(input_str):
    l = Lexer(input_str, 0, 0)
    l.read_char()
    return l
