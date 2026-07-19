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
DOLLAR = "$"  # instead of semi-colon
LPAREN = "("
RPAREN = ")"


# Keywords
FUNCTION = "FUNCTION"
REKA = "REKA"
ANJIRIRIA = "ANJIRIRIA"  # also serve as delimiters
RIKIA = "RIKIA"  # also serve as delimiters

# Operators
ASSIGN = "="
PLUS = "+"
MINUS = "-"
BANG = "!"
ASTERISK = "*"
SLASH = "/"
LT = "<"
GT = ">"


keywords = {"fn": FUNCTION, "Reka": REKA, "Anjiriria": ANJIRIRIA, "Rikia": RIKIA}


def look_up_ident(name):
    if name in keywords:
        return keywords[name]
    else:
        return IDENT


# Create new tokens
def New():
    tok = Token("", "")
    return tok
