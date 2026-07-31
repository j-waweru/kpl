from dataclasses import dataclass

TokenType = str


@dataclass(eq=True, unsafe_hash=True)
class Token:
    TokenType: TokenType
    Literal: str


ILLEGAL = "ILLEGAL"
EOF = "EOF"

# Identifiers + literals
IDENT = "IDENT"  # add, foobar, x, y, ...
INT = "INT"  # 1343456
STRING = "STRING"  # "foobar"

# Operators
ASSIGN = "="
PLUS = "+"

# Delimiters
COMMA = ","
DOLLAR = "$"  # instead of semi-colon
LPAREN = "("
RPAREN = ")"
SEMICOLON = ";"
LBRACKET = "["
RBRACKET = "]"
LBRACE = "{"
RBRACE = "}"
COLON = ":"

# Keywords
FUNCTION = "FUNCTION"
REKA = "REKA"
ANJIRIRIA = "ANJIRIRIA"  # also serve as delimiters
RIKIA = "RIKIA"  # also serve as delimiters
MA = "MA"
MAHENI = "MAHENI"
AKORWO = "AKORWO"
TIGUO = "TIGUO"
CHOKIA = "CHOKIA"

# Operators
AMPERSAND = "%"
ASSIGN = "="
PLUS = "+"
MINUS = "-"
BANG = "!"
ASTERISK = "*"
SLASH = "/"
LT = "<"
GT = ">"
EQ = "=="
EQ2 = "=="
EQ3 = "==="
EQ4 = "===="
EQ5 = "====="
EQ6 = "======"
NOT_EQ = "!="

keywords = {
    "Fn": FUNCTION,
    "Reka": REKA,
    "Anjiriria": ANJIRIRIA,
    "Anj": ANJIRIRIA,
    "Rik": RIKIA,
    "Rikia": RIKIA,
    "Ma": MA,
    "Maheni": MAHENI,
    "Akorwo": AKORWO,
    "Tiguo": TIGUO,
    "Chokia": CHOKIA,
}


def look_up_ident(name):
    if name in keywords:
        return keywords[name]
    else:
        return IDENT


# Create new tokens
def New():
    tok = Token("", "")
    return tok
