from dataclasses import dataclass

# TokenType = str


@dataclass
class Token:
    TokenType: str
    Literal: str


ILLEGAL = "ILLEGAL"
EOF = "EOF"

# Identifiers + literals
IDENT = "IDENT"  # add, foobar, x, y, ...
INT = "INT"  # 1343456

# Operators
ASSIGN = "="
PLUS = "+"

# Delimiters
COMMA = ","
SEMICOLON = ";"
LPAREN = "("
RPAREN = ")"
LBRACE = "{"
RBRACE = "}"

# Keywords
FUNCTION = "FUNCTION"
LET = "LET"

# Operators
ASSIGN = "="
PLUS = "+"
MINUS = "-"
BANG = "!"
ASTERISK = "*"
SLASH = "/"
LT = "<"
GT = ">"


keywords = {"fn": FUNCTION, "let": LET}


def look_up_indent(name):
    if name in keywords:
        return keywords[name]
    else:
        return IDENT


# Create new tokens
def New():
    tok = Token("", "")
    return tok



