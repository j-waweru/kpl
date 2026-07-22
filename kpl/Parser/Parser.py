import kpl.Token.Token as Token
import kpl.Lexer.Lexer as Lexer
import kpl.Ast.Ast as Ast
from dataclasses import dataclass, field

from typing import Callable
from enum import IntEnum

PrefixParseFn = Callable[[], Ast.Expression]
InfixParseFn = Callable[[Ast.Expression], Ast.Expression]


class Precedence(IntEnum):
    LOWEST = 1
    EQUALS = 2  # ==, !=
    LESSGREATER = 3  # <, >
    SUM = 4  # +, -
    PRODUCT = 5  # *, /
    PREFIX = 6  # -X, !X
    CALL = 7  # function(X)


PRECEDENCES = {
    Token.EQ: Precedence.EQUALS,
    Token.NOT_EQ: Precedence.EQUALS,
    Token.LT: Precedence.LESSGREATER,
    Token.GT: Precedence.LESSGREATER,
    Token.PLUS: Precedence.SUM,
    Token.MINUS: Precedence.SUM,
    Token.SLASH: Precedence.PRODUCT,
    Token.ASTERISK: Precedence.PRODUCT,
    Token.LPAREN: Precedence.CALL,
}


@dataclass
class Parser:
    l: Lexer.Lexer
    curToken: Token.Token = field(default_factory=Token.New)
    peekToken: Token.Token = field(default_factory=Token.New)
    errors: list[str] = field(default_factory=list)

    prefix_parse_fns: dict[Token.TokenType, PrefixParseFn] = field(default_factory=dict)
    infix_parse_fns: dict[Token.TokenType, InfixParseFn] = field(default_factory=dict)

    def parse_program(self) -> Ast.Program:
        # Entry point and creates the root node of the AST
        # Then build child nodes by calling other functions recursively and append their nodes to the AST
        program = Ast.Program()

        while self.curToken.TokenType != Token.EOF:
            stmt = self.parse_statement()
            if stmt is not None:
                program.statements.append(stmt)

            self.next_token()

        return program

    def next_token(self):
        self.curToken = self.peekToken
        self.peekToken = self.l.next_token()

    def parse_statement(self):
        match self.curToken.TokenType:
            case Token.REKA:
                return self.parse_reka_statement()
            case Token.CHOKIA:
                return self.parse_chokia_statement()

            case _:
                return self.parse_expression_statement()

    def parse_reka_statement(self):
        # Go:
        # stmt := &ast.LetStatement{Token: p.curToken}

        stmt = Ast.RekaStatement(Token=self.curToken)

        if not self.expect_peek(Token.IDENT):
            return None

        stmt.Name = Ast.Identifier(
            Token=self.curToken,
            Value=self.curToken.Literal,
        )

        if not self.expect_peek(Token.ASSIGN):
            return None

        self.next_token()

        stmt.Value = self.parse_expression(Precedence.LOWEST)

        if self.peek_token_is(Token.DOLLAR):
            self.next_token()

        return stmt

    def parse_chokia_statement(self):

        stmt = Ast.ChokiaStatement(Token=self.curToken)

        self.next_token()

        stmt.ReturnValue = self.parse_expression(Precedence.LOWEST)

        if self.peek_token_is(Token.DOLLAR):
            self.next_token()

        return stmt

    def cur_token_is(self, token_type):
        # Compare current token type.
        return self.curToken.TokenType == token_type

    def peek_token_is(self, token_type):
        # Compare next token type.
        return self.peekToken.TokenType == token_type

    def expect_peek(self, token_type):
        # If next token matches, consume it.
        if self.peek_token_is(token_type):
            self.next_token()
            return True

        return False

    def get_errors(self) -> list[str]:
        return self.errors

    def peek_error(self, token_type):
        msg = (
            f"expected next token to be {token_type}, "
            f"got {self.peekToken.TokenType} instead"
        )
        self.errors.append(msg)

    def register_prefix(self, token_type: Token.TokenType, fn: PrefixParseFn):
        self.prefix_parse_fns[token_type] = fn

    def register_infix(self, token_type: Token.TokenType, fn: InfixParseFn):
        self.infix_parse_fns[token_type] = fn

    def parse_expression_statement(self) -> Ast.ExpressionStatement:
        stmt = Ast.ExpressionStatement(self.curToken)
        stmt.Expression = self.parse_expression(Precedence.LOWEST)
        if self.peek_token_is(Token.DOLLAR):
            self.next_token()
        return stmt

    def no_prefix_parse_fn_error(self, token_type: str):
        msg = f"no prefix parse function for {token_type} found"
        self.errors.append(msg)

    def parse_expression(self, precedence: Precedence) -> Ast.Expression | None:

        prefix = self.prefix_parse_fns.get(self.curToken.TokenType)

        if prefix is None:
            self.no_prefix_parse_fn_error(self.curToken.TokenType)
            return None

        left_exp = prefix()

        while (
            not self.peek_token_is(Token.DOLLAR) and precedence < self.peek_precedence()
        ):
            infix = self.infix_parse_fns.get(self.peekToken.TokenType)

            if infix is None:
                return left_exp

            self.next_token()

            left_exp = infix(left_exp)

        return left_exp

    def parse_identifier(self) -> Ast.Expression:
        return Ast.Identifier(
            Token=self.curToken,
            Value=self.curToken.Literal,
        )

    def parse_integer_literal(self):

        try:
            value = int(self.curToken.Literal)
        except ValueError:
            self.errors.append(f'could not parse "{self.curToken.Literal}" as integer')
            return None

        return Ast.IntegerLiteral(
            Token=self.curToken,
            Value=value,
        )

    def parse_prefix_expression(self) -> Ast.Expression:

        expression = Ast.PrefixExpression(
            Token=self.curToken,
            Operator=self.curToken.Literal,
        )

        self.next_token()

        expression.Right = self.parse_expression(Precedence.PREFIX)

        return expression

    def peek_precedence(self) -> Precedence:
        return PRECEDENCES.get(
            self.peekToken.TokenType,
            Precedence.LOWEST,
        )

    def cur_precedence(self) -> Precedence:
        return PRECEDENCES.get(
            self.curToken.TokenType,
            Precedence.LOWEST,
        )

    def parse_infix_expression(self, left: Ast.Expression) -> Ast.Expression:

        expression = Ast.InfixExpression(
            Token=self.curToken,
            Operator=self.curToken.Literal,
            Left=left,
        )

        precedence = self.cur_precedence()

        self.next_token()

        expression.Right = self.parse_expression(precedence)

        return expression

    def parse_boolean(self) -> Ast.Expression:

        return Ast.Boolean(
            Token=self.curToken,
            Value=self.cur_token_is(Token.MA),
        )

    def parse_grouped_expression(self):
        self.next_token()
        exp = self.parse_expression(Precedence.LOWEST)
        if self.expect_peek(Token.RPAREN):
            return exp
        else:
            return None

    def parse_akorwo_statement(self) -> Ast.Expression | None:

        expression = Ast.AkorwoExpression(Token=self.curToken)

        if not self.expect_peek(Token.LPAREN):
            return None

        self.next_token()

        expression.Condition = self.parse_expression(Precedence.LOWEST)

        if not self.expect_peek(Token.RPAREN):
            return None

        if not self.expect_peek(Token.ANJIRIRIA):
            return None

        expression.Consequence = self.parse_block_statement()

        if self.peek_token_is(Token.TIGUO):
            self.next_token()

            if not self.expect_peek(Token.ANJIRIRIA):
                return None

            expression.Alternative = self.parse_block_statement()

        return expression

    def parse_block_statement(self) -> Ast.BlockStatement:

        block = Ast.BlockStatement(Token=self.curToken)
        block.Statements = []

        self.next_token()

        while not self.cur_token_is(Token.RIKIA) and not self.cur_token_is(Token.EOF):
            stmt = self.parse_statement()

            if stmt is not None:
                block.Statements.append(stmt)

            self.next_token()

        return block

    def parse_function_parameters(self) -> list[Ast.Identifier] | None:

        identifiers: list[Ast.Identifier] = []

        if self.peek_token_is(Token.RPAREN):
            self.next_token()
            return identifiers

        self.next_token()

        identifiers.append(
            Ast.Identifier(
                Token=self.curToken,
                Value=self.curToken.Literal,
            )
        )

        while self.peek_token_is(Token.COMMA):
            self.next_token()
            self.next_token()

            identifiers.append(
                Ast.Identifier(
                    Token=self.curToken,
                    Value=self.curToken.Literal,
                )
            )

        if not self.expect_peek(Token.RPAREN):
            return None

        return identifiers

    def parse_function_literal(self) -> Ast.Expression | None:

        lit = Ast.FunctionLiteral(Token=self.curToken)

        if not self.expect_peek(Token.LPAREN):
            return None

        lit.Parameters = self.parse_function_parameters()

        if not self.expect_peek(Token.ANJIRIRIA):
            return None

        lit.Body = self.parse_block_statement()

        return lit

    def parse_call_expression(self, function: Ast.Expression) -> Ast.Expression:

        exp = Ast.CallExpression(
            Token=self.curToken,
            Function=function,
        )

        exp.Arguments = self.parse_call_arguments()

        return exp

    def parse_call_arguments(self) -> list[Ast.Expression] | None:

        args: list[Ast.Expression] = []

        if self.peek_token_is(Token.RPAREN):
            self.next_token()
            return args

        self.next_token()

        args.append(self.parse_expression(Precedence.LOWEST))

        while self.peek_token_is(Token.COMMA):
            self.next_token()
            self.next_token()

            args.append(self.parse_expression(Precedence.LOWEST))

        if not self.expect_peek(Token.RPAREN):
            return None

        return args


def New(lexer) -> Parser:
    p = Parser(lexer)

    p.next_token()
    p.next_token()

    p.prefix_parse_fns = {}
    p.register_prefix(Token.IDENT, p.parse_identifier)
    p.register_prefix(Token.INT, p.parse_integer_literal)
    p.register_prefix(Token.BANG, p.parse_prefix_expression)
    p.register_prefix(Token.MINUS, p.parse_prefix_expression)

    p.register_infix(Token.PLUS, p.parse_infix_expression)
    p.register_infix(Token.MINUS, p.parse_infix_expression)
    p.register_infix(Token.SLASH, p.parse_infix_expression)
    p.register_infix(Token.ASTERISK, p.parse_infix_expression)
    p.register_infix(Token.EQ, p.parse_infix_expression)
    p.register_infix(Token.NOT_EQ, p.parse_infix_expression)
    p.register_infix(Token.LT, p.parse_infix_expression)
    p.register_infix(Token.GT, p.parse_infix_expression)
    p.register_prefix(Token.MA, p.parse_boolean)
    p.register_prefix(Token.MAHENI, p.parse_boolean)
    p.register_prefix(Token.LPAREN, p.parse_grouped_expression)
    p.register_prefix(Token.AKORWO, p.parse_akorwo_statement)
    p.register_prefix(Token.FUNCTION, p.parse_function_literal)
    p.register_infix(Token.LPAREN, p.parse_call_expression)
    return p


# huna
